#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016 7x24hs.com
# thomas@7x24hs.com
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../rpc"))
import logging
from foo.toolkit.cy_json import CyJson
from comm import *
from global_const import *
from base_handler import *
from foo.svc_config import GlobalConfig
from foo.dao.auth_policy_dao import *
from foo.dao.auth_role_dao import *
from foo.dao.auth_account_dao import *
from foo.dao.sys_log_dao import *

from tornado.escape import json_encode, json_decode
from tornado.httpclient import *
from tornado.httputil import url_concat


# /api/auth/v5/policies/filter
class PoliciesFilterXHR(AuthorizationHandler):
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
            if "searchs" in payload:
                searchs = payload["searchs"]
            if "orders" in payload:
                orders = payload["orders"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        idx = (currPage - 1) * pageSize
        datas = AuthPolicyDao().selectPaginationByFilters(searchs, orders, idx, pageSize)

        totalNum = AuthPolicyDao().countPaginationByFilters(searchs)
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


# /auth/api/v5/policies
class PoliciesXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        priority = 0
        try:
            payload = CyJson.loads(self.request.body)
            if 'type' in payload:
                type = payload['type']
            if 'objId' in payload:
                objId = payload['objId']
            if 'resPath' in payload:
                resPath = payload['resPath']
            if 'action' in payload:
                action = payload['action']
            if 'access' in payload:
                access = payload['access']
            if 'priority' in payload:
                priority = payload['priority']
        except Exception as e:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        uuid = generate_uuid_str()
        if type == "role":
            role = AuthRoleDao().select(objId)
            if role:
                objName = role['name']
            else:
                objName = objId
        elif type == "account":
            user = AuthAccountDao().select(objId)
            if user:
                objName = user['username']
            else:
                objName = objId

        AuthPolicyDao().insert(uuid,type,objId,objName,resPath,action,access,priority)

        response = {"errCode": 200, "errMsg": "Success", "data": uuid}
        self.write_response(response, logger=True)
        return


# /auth/api/v5/policies/{policyId}
class PolicyXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, policyId):
        priority = 0
        try:
            payload = CyJson.loads(self.request.body)
            if 'type' in payload:
                type = payload['type']
            if 'objId' in payload:
                objId = payload['objId']
            if 'resPath' in payload:
                resPath = payload['resPath']
            if 'action' in payload:
                action = payload['action']
            if 'access' in payload:
                access = payload['access']
            if 'priority' in payload:
                priority = payload['priority']
        except Exception as e:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        if type == "role":
            role = AuthRoleDao().select(objId)
            if role:
                objName = role['name']
            else:
                objName = objId
        elif type == "account":
            user = AuthAccountDao().select(objId)
            if user:
                objName = user['username']
            else:
                objName = objId

        AuthPolicyDao().update(policyId,type,objId,objName,resPath,action,access,priority)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def delete(self, policyId):
        AuthPolicyDao().delete(policyId)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return
