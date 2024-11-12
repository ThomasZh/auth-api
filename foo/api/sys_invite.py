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
from foo.dao.sys_invite_dao import *
from foo.dao.auth_account_dao import *
from foo.dao.auth_login_dao import *


# /api/sys/invites
class SysInvitesXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            fromId = payload['fromId']
            fromName = payload['fromName']
            fromAvatar = payload['fromAvatar']
            toId = payload['toId']
            toName = payload['toName']
            toAvatar = payload['toAvatar']
            type = payload['type']
            objId = payload['objId']
            objName = payload['objName']
            content = payload['content']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        operId = self.get_account_id()
        operName = self.get_username()

        uuid = generate_uuid_str()
        SysInviteDao().insert(uuid, fromId, fromName, fromAvatar, toId, toName, toAvatar, type, objId, objName, content)

        response = {"errCode": 200, "errMsg": "Success", "data": uuid}
        self.write_response(response, logger=True)
        return


# /api/sys/invites/filter
class SysInvitesFilterXHR(AuthorizationHandler):
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
        datas = SysInviteDao().selectPaginationByFilters(searchs, orders, idx, pageSize)

        totalNum = SysInviteDao().countPaginationByFilters(searchs)
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


# /api/sys/invites/accounts/search
class SysInvitesAccountsSearchXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        currPage = 1
        pageSize = 1
        try:
            payload = CyJson.loads(self.request.body)
            if "currPage" in payload:
                currPage = int(payload["currPage"])
            if "pageSize" in payload:
                pageSize = int(payload["pageSize"])
            loginName = payload["loginName"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        if not loginName:
            response = {
                "errCode": 200,
                "errMsg": "Success",
                "currPage": currPage,
                "pageSize": pageSize,
                "totalNum": 0,
                "totalPage": 0,
                "datas": []
            }
            self.write_response(response, logger=False)
            return

        idx = (currPage - 1) * pageSize
        datas = AuthLoginDao().fuzzy_search(loginName, idx, pageSize)
        if not datas or len(datas) == 0:
            response = {
                "errCode": 200,
                "errMsg": "Success",
                "currPage": currPage,
                "pageSize": pageSize,
                "totalNum": 0,
                "totalPage": 0,
                "datas": []
            }
            self.write_response(response, logger=False)
            return

        arr = []
        for data in datas:
            account = AuthAccountDao().select(data['accountId'])
            strlogins = []
            logins = AuthLoginDao().select_pagination(data['accountId'], 0, 10)
            for login in logins:
                strlogins.append(login['loginName'])
            account['logins'] = strlogins
            arr.append(account)

        totalNum = AuthLoginDao().count_fuzzy_search(loginName)
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
            "datas": arr
        }
        self.write_response(response, logger=False)
        return


# /api/sys/invites/{id}
class SysInviteXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, id):
        try:
            payload = CyJson.loads(self.request.body)
            fromId = payload['fromId']
            fromName = payload['fromName']
            fromAvatar = payload['fromAvatar']
            toId = payload['toId']
            toName = payload['toName']
            toAvatar = payload['toAvatar']
            type = payload['type']
            objId = payload['objId']
            objName = payload['objName']
            content = payload['content']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        SysInviteDao().update(id, fromId, fromName, fromAvatar, toId, toName, toAvatar, type, objId, objName, content)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def delete(self, id):
        SysInviteDao().delete(id)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, id):
        data = SysInviteDao().select(id)

        response = {"errCode": 200, "errMsg": "Success", "data":data}
        self.write_response(response, logger=False)
        return


# /api/sys/invites/{id}/status
class SysInvitesStatusXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, id):
        try:
            payload = CyJson.loads(self.request.body)
            status = payload["status"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        SysInviteDao().updateStatus(id, status)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return
