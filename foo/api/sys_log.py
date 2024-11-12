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
from foo.dao.sys_log_dao import *
from foo.svc_config import GlobalConfig
from base_handler import *
from global_const import *
from comm import *


# /api/auth/v5/sys/logs
# 系统内部使用，用户操作写入系统日志
class SysLogsXHR(BaseHandler):
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            accountId = payload['accountId']
            username = payload['username']
            method = payload['method']
            path = payload['path']
            params = payload['params']
            body = payload['body']
            respCode = payload['respCode']
            respMsg = payload['respMsg']
            ipAddr = payload['ipAddr']
            userAgent = payload['userAgent']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        SysLogDao().insert(accountId, username, method, path, params, body, respCode, respMsg, ipAddr, userAgent)

        response = {"errCode":200, "errMsg":"Success"}
        self.write_response(response, logger=False)
        return


# /api/auth/v5/sys/logs/filter
class SysLogsFilterXHR(AuthorizationHandler):
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
        datas = SysLogDao().selectPaginationByFilters(searchs, orders, idx, pageSize)

        totalNum = SysLogDao().countPaginationByFilters(searchs)
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
