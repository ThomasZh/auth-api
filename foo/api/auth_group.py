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
from foo.dao.auth_group_dao import *
from foo.dao.auth_account_dao import *
from foo.dao.auth_account_group_dao import *
from foo.dao.auth_account_role_dao import *
from foo.svc.svc_tree import *
from foo.svc.svc_group import *
from foo.dao.auth_login_dao import *
from foo.toolkit.cy_tree import *


# /api/auth/v5/groups
class AuthGroupsXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            pid = payload['pid']
            title = payload['title']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        group = {
            "id": generate_uuid_str(),
            "title": title,
        }
        insert_group_as_last_child(pid, group)

        response = {
            "errCode": 200,
            "errMsg": "Success",
            "data": group['id'],
        }
        self.write_response(response, logger=True)
        return


# /auth/api/v5/groups/{groupId}
class AuthGroupXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def delete(self, groupId):
        delete_group_and_children(groupId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, groupId):
        try:
            payload = CyJson.loads(self.request.body)
            title = payload['title']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        AuthGroupDao().update_title(groupId, title)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, groupId):
        data = AuthGroupDao().select(groupId)
        if data:
            response = {"errCode": 200, "errMsg": "Success", "data": data}
            self.write_response(response, logger=False)
            return
        else:
            response = {"errCode": 404, "errMsg": "Not Found"}
            self.write_response(response, logger=False)
            return


# /auth/api/v5/groups/{groupId}/table
class AuthGroupTableXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, groupId):
        group = AuthGroupDao().select(groupId)
        if group:
            datas = AuthGroupDao().select_tree(group['lft'], group['rgt'])

            response = {"errCode": 200, "errMsg": "Success", "datas":datas}
        else:
            response = {"errCode": 200, "errMsg": "Success", "datas":[]}

        self.write_response(response, logger=False)
        return


# /auth/api/v5/groups/{groupId}/tree
class AuthGroupTreeXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, groupId):
        group = AuthGroupDao().select(groupId)
        if group:
            datas = AuthGroupDao().select_tree(group['lft'], group['rgt'])

            rs = make_tree(datas, group['pid'], 'pid', 'id')

            response = {"errCode": 200, "errMsg": "Success", "datas":rs['tree'], "expandedKeys":rs['expandedKeys']}
        else:
            response = {"errCode": 200, "errMsg": "Success", "datas":[], "expandedKeys":[]}

        self.write_response(response, logger=False)
        return


# /api/auth/v5/groups/{groupId}/accounts
class AuthGroupAccountsXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, groupId):
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
                arr = []
                logins = AuthLoginDao().select_pagination(data['accountId'], 0, 10)
                for login in logins:
                    arr.append(login['loginName'])
                data['logins'] = arr

                arr = []
                roles = AuthAccountRoleDao().select_roles_pagination(data['accountId'], 0, 100)
                for role in roles:
                    arr.append(role['name'])
                data['roles'] = arr

                count = AuthAccountGroupDao().count(data['accountId'], groupId)
                if count == 0:
                    data['checked'] = 0
                else:
                    data['checked'] = 1 #此账号与此组织绑定
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
    def put(self, groupId):
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
            num = AuthAccountGroupDao().count(accountId, groupId)
            if num == 0:
                AuthAccountGroupDao().insert(accountId, groupId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def delete(self, groupId):
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
            num = AuthAccountGroupDao().count(accountId, groupId)
            if num > 0:
                AuthAccountGroupDao().delete(accountId, groupId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /api/auth/v5/groups/{groupId}/in-accounts
class AuthGroupInAccountsXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, groupId):
        currPage = int(self.get_argument('currPage', 1))
        pageSize = int(self.get_argument('pageSize', 20))

        limit = pageSize
        idx = (currPage - 1) * limit
        totalNum = 0
        totalPage = 0

        # 查询所有的账号
        datas = AuthAccountDao().select_pagination_by_group(groupId, idx, pageSize)
        if datas and len(datas) > 0:
            for data in datas:
                data['checked'] = 1 #此账号与此组织绑定

                arr = []
                logins = AuthLoginDao().select_pagination(data['accountId'], 0, 10)
                for login in logins:
                    arr.append(login['loginName'])
                data['logins'] = arr

                arr = []
                roles = AuthAccountRoleDao().select_roles_pagination(data['accountId'], 0, 100)
                for role in roles:
                    arr.append(role['name'])
                data['roles'] = arr
        else:
            datas = []

        totalNum = AuthAccountDao().count_by_group(groupId)
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


# /api/auth/v5/groups/{groupId}/move
class AuthGroupMoveXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, groupId):
        try:
            payload = CyJson.loads(self.request.body)
            objId = payload["objId"]
            place = payload["place"]
            relation = payload["relation"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        # 0. 获取原始 task 与子 task 信息
        group = AuthGroupDao().select(groupId)
        datas = AuthGroupDao().select_tree(group['lft'], group['rgt'])

        # 1. 删除任务以及其子任务
        delete_group_and_children(groupId)

        # 2. 插入原始 task 与子 task 到新位置
        for data in datas:
            if groupId == data['id']: # 原始task, 第一条记录
                if relation == "brother":
                    if place == "after":
                        insert_group_after_brother(objId, data)
                    elif place == "before":
                        insert_group_before_brother(objId, data)
                elif relation == "child":
                    insert_group_as_first_child(objId, data)
            else:
                insert_group_as_last_child(data['pid'], data)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /auth/api/v5/groups/{groupId}/accounts/tree
class AuthGroupsAccountsTreeXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, groupId):
        arr = []
        group = AuthGroupDao().select(groupId)
        if group:
            datas = AuthGroupDao().select_tree(group['lft'], group['rgt'])
            for data in datas:
                data['type'] = 'systree'
                data['label'] = data['title']
                data['value'] = data['id']
                data['key'] = data['id']
                data['disable'] = True
                arr.append(data)
                # 查询所有的账号
                accounts = AuthAccountDao().select_pagination_by_group(data['id'], 0, 1000)
                if accounts and len(accounts) > 0:
                    for account in accounts:
                        account['type'] = 'leaf'
                        account['id'] = account['accountId']
                        account['pid'] = data['id']
                        account['title'] = account['username']
                        account['label'] = account['username']
                        account['value'] = account['accountId']
                        account['key'] = account['accountId']
                        account['disable'] = False
                        account['depth'] = data['depth'] + 1
                        arr.append(account)
            # TODO 递归的方式, 删除没有子节点的树型结构数据
            tree = build_group_account_tree(arr, groupId)

            # 删除第一条记录
            tree = tree[0]['children']

            response = {"errCode": 200, "errMsg": "Success", "datas":tree}
        else:
            response = {"errCode": 200, "errMsg": "Success", "datas":arr}

        self.write_response(response, logger=False)
        return
