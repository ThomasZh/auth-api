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
from base_handler import *
from foo.svc.svc_permission import assert_permission


# /api/auth/v5/assert/permission
# 系统内部使用，校验是否有权限调用此 http 请求
class AuthAssertPermissionXHR(BaseHandler):
    def post(self):
        try:
            payload = CyJson.loads(self.request.body)
            accountId = payload['accountId']
            path = payload['path']
            method = payload['method']
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        response = assert_permission(accountId, path, method)
        self.write_response(response, logger=False)
        return
