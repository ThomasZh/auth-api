#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2021 cyber-life.cn
# thomas@cyber-life.cn
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
import logging
from foo.toolkit.cy_json import CyJson
from foo.svc_config import GlobalConfig
from base_handler import *
from global_const import *
from comm import *
from foo.dao.sys_notify_dao import *
from foo.svc.svc_profile import *


# /api/sys/notices
class SysNoticesXHR(AuthorizationHandler):
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
            else:
                searchs = []
            if "orders" in payload:
                orders = payload["orders"]
            else:
                orders = []
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        operId = self.get_account_id()
        searchs.append({"column": "toAccountId", "op": "eq", "value": operId})

        idx = (currPage - 1) * pageSize
        datas = SysNotifyDao().selectPaginationByFilters(searchs, orders, idx, pageSize)

        totalNum = SysNotifyDao().countPaginationByFilters(searchs)
        if totalNum % pageSize == 0:
            totalPage = int(totalNum / pageSize)
        else:
            totalPage = int(totalNum / pageSize) + 1

        for data in datas:
            profile = svc_get_profile(data['fromAccountId'])
            if profile:
                data['fromUsername'] = profile['username']
                data['fromAvatar'] = profile['avatar']

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


# /api/sys/notices/count
class SysNoticesCountXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        operId = self.get_account_id()
        searchs = [
            {"column": "toAccountId", "op": "eq", "value": operId},
            {"column": "status", "op": "eq", "value": 0},
        ]
        totalNum = SysNotifyDao().countPaginationByFilters(searchs)
        response = {
            "errCode": 200,
            "errMsg": "Success",
            "data": totalNum
        }
        self.write_response(response, logger=False)
        return


# /api/sys/notices/{id}/status
class SysNoticesStatusXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, id):
        try:
            payload = CyJson.loads(self.request.body)
            status = payload["status"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        SysNotifyDao().updateStatus(id, status)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return
