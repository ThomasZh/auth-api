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
from foo.dao.auth_role_dao import *
from foo.dao.auth_group_dao import *
from foo.dao.auth_account_role_dao import *
from foo.dao.auth_account_group_dao import *
from foo.dao.sys_log_dao import *
from foo.svc.svc_tree import *
from foo.svc.crypt_bcrypt import *


# /api/auth/v5/accounts
class AuthAccountsXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            loginName = payload["loginName"]
            username = payload["username"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        type = "username"
        md5pwd = "e10adc3949ba59abbe56e057f20f883e" # default password = 123456

        login = AuthLoginDao().select(loginName)
        if login:
            response = {"errCode":409, "errMsg":"登录名已经存在"}
            self.write_response(response, logger=True)
            return

        # 生成新登录号
        uuid = generate_uuid_str()
        password = generate_pwd(md5pwd)
        AuthLoginDao().insert(loginName, password, type, uuid)

        # 生成新账号
        AuthAccountDao().insert(uuid, username, DEFAULT_AVATAR)

        # 添加一个基本角色 customer
        AuthAccountRoleDao().insert(uuid, DEFAULT_ROLE_ID)

        response = {"errCode":200, "errMsg":"Success", "data": uuid}
        self.write_response(response, logger=True)
        return


# /api/auth/v5/accounts/filter
class AuthAccountsFilterXHR(AuthorizationHandler):
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
        datas = AuthAccountDao().selectPaginationByFilters(searchs, orders, idx, pageSize)
        for data in datas:
            arr = []
            logins = AuthLoginDao().select_pagination(data['accountId'], 0, 100)
            for login in logins:
                arr.append(login['loginName'])
            data['logins'] = arr

            arr = []
            roles = AuthAccountRoleDao().select_roles_pagination(data['accountId'], 0, 100)
            for role in roles:
                arr.append(role['name'])
            data['roles'] = arr

            arr = []
            groups = AuthAccountGroupDao().select_groups_pagination(data['accountId'], 0, 100)
            for group in groups:
                arr.append(group['title'])
            data['groups'] = arr

        totalNum = AuthAccountDao().countPaginationByFilters(searchs)
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


# /auth/api/v5/accounts/{accountId}
class AuthAccountXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, accountId):
        data = AuthAccountDao().select(accountId)

        response = {
            "errCode": 200,
            "errMsg": "Success",
            "data": data
        }
        self.write_response(response, logger=False)
        return


# /api/auth/v5/accounts/{accountId}/lock
class AuthAccountLockXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, accountId):
        AuthAccountDao().update_status(accountId, "1")

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /api/auth/v5/accounts/{accountId}/unlock
class AuthAccountUnlockXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, accountId):
        AuthAccountDao().update_status(accountId, "0")

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /auth/api/v5/accounts/{accountId}/logins
class AuthAccountLoginsXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, accountId):
        currPage = int(self.get_argument('currPage', 1))
        pageSize = int(self.get_argument('pageSize', 20))

        limit = pageSize
        idx = (currPage - 1) * limit
        totalNum = 0
        totalPage = 0

        datas = AuthLoginDao().select_pagination(accountId, idx, limit)

        totalNum = AuthLoginDao().count(accountId)
        if totalNum % limit == 0:
            totalPage = int(totalNum / limit)
        else:
            totalPage = int(totalNum / limit) + 1

        response = {
            "errCode": 200,
            "errMsg": "Success",
            "currPage": currPage,
            "pageSize": limit,
            "totalPage": totalPage,
            "totalNum": totalNum,
            "datas": datas
        }
        self.write_response(response, logger=False)
        return


# /auth/api/v5/accounts/{accountId}/roles
class AuthAccountRolesXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, accountId):
        currPage = int(self.get_argument('currPage', 1))
        pageSize = int(self.get_argument('pageSize', 20))

        limit = pageSize
        idx = (currPage - 1) * limit
        totalNum = 0
        totalPage = 0

        # 查询所有角色
        datas = AuthRoleDao().select_pagination(idx, limit)
        if datas and len(datas) > 0:
            for data in datas:
                count = AuthAccountRoleDao().count(accountId, data['id'])
                if count == 0:
                    data['checked'] = 0
                else:
                    data['checked'] = 1 #此菜单与此角色绑定
        else:
            datas = []

        totalNum = AuthRoleDao().count()
        if totalNum % limit == 0:
            totalPage = int(totalNum / limit)
        else:
            totalPage = int(totalNum / limit) + 1

        response = {
            "errCode": 200,
            "errMsg": "Success",
            "currPage": currPage,
            "pageSize": limit,
            "totalPage": totalPage,
            "totalNum": totalNum,
            "datas": datas
        }
        self.write_response(response, logger=False)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, accountId):
        roleIds = []
        try:
            payload = CyJson.loads(self.request.body)
            if "roleIds" in payload:
                roleIds = payload["roleIds"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        for roleId in roleIds:
            num = AuthAccountRoleDao().count(accountId, roleId)
            if num == 0:
                AuthAccountRoleDao().insert(accountId, roleId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def delete(self, accountId):
        roleIds = []
        try:
            payload = CyJson.loads(self.request.body)
            if "roleIds" in payload:
                roleIds = payload["roleIds"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        for roleId in roleIds:
            num = AuthAccountRoleDao().count(accountId, roleId)
            if num > 0:
                AuthAccountRoleDao().delete(accountId, roleId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /auth/api/v5/accounts/{accountId}/roles/{roleId}
class AuthAccountRoleXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self, accountId, roleId):
        AuthAccountRoleDao().insert(accountId, roleId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def delete(self, accountId, roleId):
        AuthAccountRoleDao().delete(accountId, roleId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /auth/api/v5/accounts/{accountId}/groups
class AuthAccountGroupsXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, accountId):
        response = None

        # 查询所有组织
        root_group = AuthGroupDao().select(AUTH_ROOT_GROUP_ID)
        if root_group:
            datas = AuthGroupDao().select_tree(root_group['lft'], root_group['rgt'])

            arr = []
            # 计算此账号绑定了哪些组织
            if datas and len(datas) > 0:
                for data in datas:
                    count = AuthAccountGroupDao().count(accountId, data['id'])
                    if count > 0:
                        arr.append(data['id'])

            rs = make_tree(datas, root_group['pid'], 'pid', 'id')
            response = {
                "errCode": 200,
                "errMsg": "Success",
                "datas":rs['tree'],
                "expandedKeys":rs['expandedKeys'],
                "checkedKeys":arr,
            }
        else:
            response = {"errCode": 200, "errMsg": "Success", "datas":[], "expandedKeys":[]}

        self.write_response(response, logger=False)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, accountId):
        groupIds = []
        try:
            payload = CyJson.loads(self.request.body)
            if "groupIds" in payload:
                groupIds = payload["groupIds"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        # 首先删除原有的绑定
        AuthAccountGroupDao().delete_by_account(accountId)
        # 绑定新增
        for groupId in groupIds:
            num = AuthAccountGroupDao().count(accountId, groupId)
            if num == 0:
                AuthAccountGroupDao().insert(accountId, groupId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /auth/api/v5/accounts/{accountId}/groups/{groupId}
class AuthAccountGroupXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self, accountId, groupId):
        AuthAccountGroupDao().insert(accountId, groupId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def delete(self, accountId, groupId):
        AuthAccountGroupDao().delete(accountId, groupId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return
