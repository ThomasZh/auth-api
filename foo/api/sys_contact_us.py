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
from foo.dao.sys_contact_us_dao import *


# /api/sys_contact_uss
class SysContactUssXHR(BaseHandler):
    # @tornado.web.authenticated  # if no session, redirect to login page
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            username = payload['username']
            contactInfo = payload['contactInfo']
            content = payload['content']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        SysContactUsDao().insert(username, contactInfo, content)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /api/sys_contact_uss/filter
class SysContactUssFilterXHR(AuthorizationHandler):
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
        datas = SysContactUsDao().selectPaginationByFilters(searchs, orders, idx, pageSize)

        totalNum = SysContactUsDao().countPaginationByFilters(searchs)
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


# /api/sys_contact_uss/{id}/status
class SysContactUssStatusXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self, id):
        try:
            payload = CyJson.loads(self.request.body)
            status = payload["status"]
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        SysContactUsDao().updateStatus(id, status)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return
