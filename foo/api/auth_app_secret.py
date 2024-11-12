#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2021 cyber-life.cn
# thomas@cyber-life.cn
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
import logging
from foo.toolkit.cy_json import CyJson
from base_handler import *
from foo.dao.auth_app_secret_dao import *
from foo.dao.auth_app_role_dao import *
import string
import secrets


# /api/auth_app_secrets/login
class AuthAppSecretsLoginXHR(BaseHandler):
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            appkey = payload['appkey']
            appsecret = payload['appsecret']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        data = AuthAppSecretDao().selectByKey(appkey, appsecret)
        if not data:
            response = {"errCode": 404, "errMsg": "Not Found"}
            self.write_response(response, logger=True)
            return

        jwtPayload = {
            "sub": data['id'],                               # 用户id
            "name": data['appname'],                         # 用户名
            # "avatar": data['avatar'],                      # 头像
            "exp": current_timestamp() + TOKEN_EXPIRES_IN,   # token过期时间，7days
            # "jti": generate_uuid_str(),                    # 该jwt的唯一ID编号
            "roles": "user",                                 # 默认为 user 角色
        }
        jwtToken = jwt_encode(GlobalConfig().jwt_secret, jwtPayload)

        self.set_secure_cookie("accessToken", jwtToken)
        self.set_secure_cookie("expiresAt", str(jwtPayload['exp']))

        response = {"errCode": 200, "errMsg": "Success", "data": jwtToken}
        self.write_response(response, logger=True)
        return


# /api/auth_app_secrets
class AuthAppSecretsXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            appname = payload['appname']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        operId = self.get_account_id()
        operName = self.get_username()

        uuid = generate_uuid_str()
        alphabet = string.ascii_letters + string.digits
        appkey = ''.join(secrets.choice(alphabet) for i in range(8))
        appsecret = secrets.token_hex(16)
        AuthAppSecretDao().insert(uuid, appname, appkey, appsecret)

        AuthAppRoleDao().insert(uuid, AUTH_ROLE_USER_ID) # 赋予一个默认的角色 user

        response = {"errCode": 200, "errMsg": "Success", "data": uuid}
        self.write_response(response, logger=True)
        return


# /api/auth_app_secrets/filter
class AuthAppSecretsFilterXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        currPage = 1
        pageSize = 20
        orders = []
        searchs = []

        try:
            payload = CyJson.loads(self.request.body)
            if "currPage" in payload:
                currPage = int(payload["currPage"])
            if "pageSize" in payload:
                pageSize = int(payload["pageSize"])
            if "orders" in payload:
                orders = payload["orders"]
            if "searchs" in payload:
                searchs = payload["searchs"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        idx = (currPage - 1) * pageSize
        datas = AuthAppSecretDao().selectPaginationByFilters(searchs, orders, idx, pageSize)

        totalNum = AuthAppSecretDao().countPaginationByFilters(searchs)
        if totalNum % pageSize == 0:
            totalPage = int(totalNum / pageSize)
        else:
            totalPage = int(totalNum / pageSize) + 1

        response = {
            "errCode": 200,
            "errMsg": "Success",
            "currPage": currPage,
            "pageSize": pageSize,
            "totalNum": totalNum,
            "totalPage": totalPage,
            "datas": datas
        }
        self.write_response(response, logger=False)
        return


# /api/auth_app_secrets/{id}
class AuthAppSecretXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, id):
        try:
            payload = CyJson.loads(self.request.body)
            appname = payload['appname']
            appkey = payload['appkey']
            appsecret = payload['appsecret']

        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        AuthAppSecretDao().update(id, appname, appkey, appsecret)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def delete(self, id):
        AuthAppSecretDao().delete(id)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, id):
        data = AuthAppSecretDao().select(id)

        response = {"errCode": 200, "errMsg": "Success", "data":data}
        self.write_response(response, logger=False)
        return


# /api/auth_app_secrets/{id}/status
class AuthAppSecretsStatusXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, id):
        try:
            payload = CyJson.loads(self.request.body)
            status = payload["status"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        AuthAppSecretDao().updateStatus(id, status)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return
