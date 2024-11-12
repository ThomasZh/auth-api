#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016 7x24hs.com
# thomas@7x24hs.com
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
import logging
from foo.toolkit.cy_json import CyJson
from comm import *
from global_const import *
from base_handler import *
from foo.svc_config import GlobalConfig
from foo.dao.auth_account_dao import *
from foo.dao.auth_login_dao import *
from foo.dao.auth_account_role_dao import *
from foo.dao.auth_verify_code_dao import *
# from foo.svc.svc_aliyun_sms import *
from foo.svc.crypt_bcrypt import *


# /api/auth/v5/login
class AuthLoginXHR(BaseHandler):
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            loginName = payload['loginName']
            md5pwd = payload['md5pwd']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=True)
            return

        login = AuthLoginDao().select(loginName)
        if not login: # 用户不存在
            response = {"errCode":404, "errMsg":"LoginName or password is wrong!"}
            self.write_response(response, logger=True)
            return
        else:
            if login['status'] == 1:
                response = {"errCode":403, "errMsg":"This loginName is locked. Please connect to Administrator!"}
                self.write_response(response, logger=True)
                return

        account = AuthAccountDao().select(login['accountId'])
        if account['status'] == 1:
            response = {"errCode":403, "errMsg":"This loginName is locked. Please connect to Administrator!"}
            self.write_response(response, logger=True)
            return

        # Check that an unencrypted password matches one that has
        # previously been hashed
        if not compare_pwd(md5pwd, login['password']):
            response = {"errCode":404, "errMsg":"LoginName or password is wrong!"}
            self.write_response(response, logger=True)
            return

        roles = AuthAccountRoleDao().select_roles_pagination(login['accountId'], 0, 1000) # 尽可能多
        roleNames = ""
        length = len(roles)
        if roles and length>0:
            for i in range(length):
                role = roles[i]
                if i == length-1:
                    roleNames = roleNames + role['name']
                else:
                    roleNames = roleNames + role['name'] + ","

        jwtPayload = {
            "sub": login['accountId'],                       # 用户id
            "name": account['username'],                     # 用户名
            "avatar": account['avatar'],                     # 头像
            "exp": current_timestamp() + TOKEN_EXPIRES_IN,   # token过期时间，7days
            # "jti": generate_uuid_str(),                    # 该jwt的唯一ID编号
            "roles": roleNames,
        }
        jwtToken = jwt_encode(GlobalConfig().jwt_secret, jwtPayload)

        self.set_secure_cookie("accessToken", jwtToken)
        self.set_secure_cookie("expiresAt", str(jwtPayload['exp']))

        response = {"errCode":200, "errMsg":"Success", "data":jwtToken}
        self.write_response(response, logger=True)
        return


# /api/auth/v5/logout
class AuthLogoutXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def delete(self):
        # 清除cookie
        self.set_secure_cookie("accessToken", "")
        self.set_secure_cookie("expiresAt", "")
        self.set_secure_cookie("loginNext", "")

        response = {"errCode":200, "errMsg":"Success"}
        self.write_response(response, logger=True)
        return


# /api/auth/v5/signup/verify-code
class AuthSignupVerifyCodeXHR(BaseHandler):
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            loginName = payload['loginName']
            type = payload['type']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=True)
            return

        login = AuthLoginDao().select(loginName)
        if login:
            response = {"errCode":409, "errMsg":"登录名已经存在"}
            self.write_response(response, logger=True)
            return

        code = generate_nonce_number(4)
        expiresAt = timestamp_to_datetime(current_timestamp() + 300) # 5分钟
        verifyCode = AuthVerifyCodeDao().select(loginName)
        if verifyCode:
            AuthVerifyCodeDao().update(loginName,code,expiresAt)
        else:
            AuthVerifyCodeDao().insert(loginName,code,expiresAt)

        # 发送短信
        if validate_phone(loginName):
            pass
            # send_sms_register(loginName, str(code))
        else:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=True)
            return

        response = {"errCode":200, "errMsg":"Success"}
        self.write_response(response, logger=True)
        return


# /api/auth/v5/signup
class AuthSignupXHR(BaseHandler):
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            loginName = payload['loginName']
            md5pwd = payload['md5pwd']
            code = payload['code']
            type = payload['type']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=True)
            return

        login = AuthLoginDao().select(loginName)
        if login:
            response = {"errCode":409, "errMsg":"登录名已经存在"}
            self.write_response(response, logger=True)
            return

        if type == 'account':
            # 生成新登录号
            uuid = generate_uuid_str()
            password = generate_pwd(md5pwd)
            AuthLoginDao().insert(loginName, password, type, uuid)

            # 生成新账号
            AuthAccountDao().insert(uuid, loginName, DEFAULT_AVATAR)

            # 添加一个基本角色 customer
            AuthAccountRoleDao().insert(uuid, DEFAULT_ROLE_ID)

            response = {"errCode":200, "errMsg":"Success"}
            self.write_response(response, logger=True)
            return
        else:
            verifyCode = AuthVerifyCodeDao().select(loginName)
            if not verifyCode:
                response = {"errCode":412, "errMsg":"校验码错误"}
                self.write_response(response, logger=True)
                return
            else:
                date = verifyCode['expiresAt'].strftime('%Y-%m-%d %H:%M:%S')
                expiresAt = string_to_timestamp(date)
                if expiresAt < current_timestamp():
                    response = {"errCode":408, "errMsg":"校验码过期"}
                    self.write_response(response, logger=True)
                    return
                else:
                    if code == verifyCode['code']:
                        # 生成新登录号
                        uuid = generate_uuid_str()
                        password = generate_pwd(md5pwd)
                        AuthLoginDao().insert(loginName, password, type, uuid)

                        # 生成新账号
                        AuthAccountDao().insert(uuid, loginName, DEFAULT_AVATAR)

                        # 添加一个基本角色 customer
                        AuthAccountRoleDao().insert(uuid, DEFAULT_ROLE_ID)

                        response = {"errCode":200, "errMsg":"Success"}
                        self.write_response(response, logger=True)
                        return
                    else:
                        response = {"errCode":412, "errMsg":"校验码错误"}
                        self.write_response(response, logger=True)
                        return


# /api/auth/v5/lostpwd/verify-code
class AuthLostpwdVerifyCodeXHR(BaseHandler):
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            loginName = payload['loginName']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=True)
            return

        login = AuthLoginDao().select(loginName)
        if not login:
            response = {"errCode":409, "errMsg":"登录名不存在"}
            self.write_response(response, logger=True)
            return

        code = generate_nonce_number(4)
        expiresAt = timestamp_to_datetime(current_timestamp() + 300) # 5分钟
        verifyCode = AuthVerifyCodeDao().select(loginName)
        if verifyCode:
            AuthVerifyCodeDao().update(loginName,code,expiresAt)
        else:
            AuthVerifyCodeDao().insert(loginName,code,expiresAt)

        # 发送短信
        if validate_phone(loginName):
            pass
            # send_sms_lostpwd(loginName, str(code))
        else:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=True)
            return

        response = {"errCode":200, "errMsg":"Success"}
        self.write_response(response, logger=True)
        return


# /api/auth/v5/lostpwd
class AuthLostPwdXHR(BaseHandler):
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            loginName = payload['loginName']
            md5pwd = payload['md5pwd']
            code = payload['code']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=True)
            return

        login = AuthLoginDao().select(loginName)
        if not login:
            response = {"errCode":409, "errMsg":"登录名不存在"}
            self.write_response(response, logger=True)
            return

        verifyCode = AuthVerifyCodeDao().select(loginName)
        if not verifyCode:
            response = {"errCode":412, "errMsg":"校验码错误"}
            self.write_response(response, logger=True)
            return
        else:
            date = verifyCode['expiresAt'].strftime('%Y-%m-%d %H:%M:%S')
            expiresAt = string_to_timestamp(date)
            if expiresAt < current_timestamp():
                response = {"errCode":408, "errMsg":"校验码过期"}
                self.write_response(response, logger=True)
                return
            else:
                if code == verifyCode['code']:
                    password = generate_pwd(md5pwd)
                    AuthLoginDao().update_pwd(loginName, password)

                    response = {"errCode":200, "errMsg":"Success"}
                    self.write_response(response, logger=True)
                    return
                else:
                    response = {"errCode":412, "errMsg":"校验码错误"}
                    self.write_response(response, logger=True)
                    return


# /api/auth/v5/change-pwd
class AuthChangePwdXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            oldPwd = payload['oldPwd']
            newPwd = payload['newPwd']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=True)
            return

        operId = self.get_account_id()
        login = AuthLoginDao().selectById(operId)
        if not login:
            response = {"errCode":409, "errMsg":"登录名不存在"}
            self.write_response(response, logger=True)
            return

        # Check that an unencrypted password matches one that has
        # previously been hashed
        if not compare_pwd(oldPwd, login['password']):
            response = {"errCode":412, "errMsg":"old password is wrong!"}
            self.write_response(response, logger=True)
            return

        password = generate_pwd(newPwd)
        AuthLoginDao().update_pwd(login['loginName'], password)

        response = {"errCode":200, "errMsg":"Success"}
        self.write_response(response, logger=True)
