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
from foo.dao.auth_role_dao import *
from foo.dao.auth_menu_dao import *
from foo.dao.auth_account_dao import *
from foo.dao.auth_account_role_dao import *
from foo.dao.auth_role_menu_dao import *
from foo.dao.sys_log_dao import *
from foo.dao.auth_login_dao import *
from foo.dao.auth_account_group_dao import *


# /api/auth/v5/roles
class AuthRolesXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            name = payload['name']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        uuid = generate_uuid_str()
        AuthRoleDao().insert(uuid, name)

        response = {
            "errCode": 200,
            "errMsg": "Success",
            "data": uuid,
        }
        self.write_response(response, logger=True)
        return


# /api/auth/v5/roles/{roleId}
class AuthRoleXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, roleId):
        try:
            payload = CyJson.loads(self.request.body)
            name = payload['name']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        AuthRoleDao().update(roleId, name)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, roleId):
        data = AuthRoleDao().select(roleId)
        if data:
            response = {"errCode": 200, "errMsg": "Success", "data": data}
            self.write_response(response, logger=False)
            return
        else:
            response = {"errCode": 404, "errMsg": "Not Found"}
            self.write_response(response, logger=False)
            return


    @tornado.web.authenticated  # if no session, redirect to login page
    def delete(self, roleId):
        data = AuthRoleDao().delete(roleId)
        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /api/auth/v5/roles/{roleId}/menus
class AuthRoleMenusXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, roleId):
        # 查询所有的菜单
        menu = AuthMenuDao().select(AUTH_ROOT_MENU_ID)
        if menu:
            datas = AuthMenuDao().select_tree(menu['lft'], menu['rgt'])
            for data in datas:
                count = AuthRoleMenuDao().count(roleId, data['id'])
                if count == 0:
                    data['checked'] = 0
                else:
                    data['checked'] = 1 #此菜单与此角色绑定
            # 去除根节点，客户端不需要
            del(datas[0])
        else:
            datas = []

        response = {
            "errCode": 200,
            "errMsg": "Success",
            "datas": datas
        }
        self.write_response(response, logger=False)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, roleId):
        menuIds = []

        try:
            payload = CyJson.loads(self.request.body)
            if "menuIds" in payload:
                menuIds = payload["menuIds"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        for menuId in menuIds:
            num = AuthRoleMenuDao().count(roleId, menuId)
            if num == 0:
                AuthRoleMenuDao().insert(roleId, menuId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def delete(self, roleId):
        menuIds = []
        try:
            payload = CyJson.loads(self.request.body)
            if "menuIds" in payload:
                menuIds = payload["menuIds"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        for menuId in menuIds:
            num = AuthRoleMenuDao().count(roleId, menuId)
            if num > 0:
                AuthRoleMenuDao().delete(roleId, menuId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /api/auth/v5/roles/{roleId}/accounts
class AuthRoleAccountsXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, roleId):
        currPage = int(self.get_argument('currPage', 1))
        pageSize = int(self.get_argument('pageSize', 20))

        limit = pageSize
        idx = (currPage - 1) * limit
        totalNum = 0
        totalPage = 0

        # 查询所有的账号
        datas = AuthAccountDao().select_pagination(idx, pageSize)
        if datas and len(datas) > 0:
            for data in datas:
                count = AuthAccountRoleDao().count(data['accountId'], roleId)
                if count == 0:
                    data['checked'] = 0
                else:
                    data['checked'] = 1 #此账号与此角色绑定

                arr = []
                logins = AuthLoginDao().select_pagination(data['accountId'], 0, 100)
                for login in logins:
                    arr.append(login['loginName'])
                data['logins'] = arr

                arr = []
                groups = AuthAccountGroupDao().select_groups_pagination(data['accountId'], 0, 100)
                for group in groups:
                    arr.append(group['title'])
                data['groups'] = arr
        else:
            datas = []

        totalNum = AuthAccountDao().count()
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


    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, roleId):
        accountIds = []
        try:
            payload = CyJson.loads(self.request.body)
            if "accountIds" in payload:
                accountIds = payload["accountIds"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        for accountId in accountIds:
            num = AuthAccountRoleDao().count(accountId, roleId)
            if num == 0:
                AuthAccountRoleDao().insert(accountId, roleId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def delete(self, roleId):
        accountIds = []
        try:
            payload = CyJson.loads(self.request.body)
            if "accountIds" in payload:
                accountIds = payload["accountIds"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        for accountId in accountIds:
            num = AuthAccountRoleDao().count(accountId, roleId)
            if num > 0:
                AuthAccountRoleDao().delete(accountId, roleId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /api/auth/v5/roles/{roleId}/in-accounts
class AuthRoleInAccountsXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, roleId):
        currPage = int(self.get_argument('currPage', 1))
        pageSize = int(self.get_argument('pageSize', 20))

        limit = pageSize
        idx = (currPage - 1) * limit
        totalNum = 0
        totalPage = 0

        # 查询所有的账号
        datas = AuthAccountDao().select_pagination_by_role(roleId, idx, pageSize)
        if datas and len(datas) > 0:
            for data in datas:
                data['checked'] = 1 #此账号与此角色绑定

                arr = []
                logins = AuthLoginDao().select_pagination(data['accountId'], 0, 100)
                for login in logins:
                    arr.append(login['loginName'])
                data['logins'] = arr

                arr = []
                groups = AuthAccountGroupDao().select_groups_pagination(data['accountId'], 0, 100)
                for group in groups:
                    arr.append(group['title'])
                data['groups'] = arr
        else:
            datas = []

        totalNum = AuthAccountDao().count_by_role(roleId)
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


# /api/auth/v5/roles/{roleId}/menus/{menuId}
class AuthRoleMenuXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self, roleId, menuId):
        AuthRoleMenuDao().insert(roleId, menuId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def delete(self, roleId, menuId):
        AuthRoleMenuDao().delete(roleId, menuId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /api/auth/v5/roles/{roleId}/lock
class AuthRoleLockXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, roleId):
        AuthRoleDao().updateStatus(roleId, "1")

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /api/auth/v5/roles/{roleId}/unlock
class AuthRoleUnlockXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, roleId):
        AuthRoleDao().updateStatus(roleId, "0")

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /api/auth/v5/roles/filter
class AuthRolesFilterXHR(AuthorizationHandler):
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
        datas = AuthRoleDao().selectPaginationByFilters(searchs, orders, idx, pageSize)

        totalNum = AuthRoleDao().countPaginationByFilters(searchs)
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
