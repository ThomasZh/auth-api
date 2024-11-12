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
from foo.dao.auth_account_dao import *
from foo.dao.auth_login_dao import *
from foo.dao.auth_account_group_dao import *
from foo.dao.sys_profile_dao import *
from foo.svc_config import GlobalConfig
from base_handler import *
from global_const import *
from comm import *


# /api/sys/profiles/mine
class SysMyProfileXHR(AuthorizationHandler):
    @tornado.web.authenticated  # if no session, redirect to login page
    def get(self):
        operId = self.get_account_id()

        account = AuthAccountDao().select(operId)
        if not account:
            response = {"errCode": 404, "errMsg": "Not Found"}
            self.write_response(response, logger=False)
            return

        profile = SysProfileDao().select(operId)
        if profile:
            profile['username'] = account['username']
            profile['avatar'] = account['avatar']
        else:
            profile = {
                "id": account['accountId'],
                "username": account['username'],
                "avatar": account['avatar'],
                "title": "",
                "description": "",
            }
            group = AuthAccountGroupDao().select_by_account(account['accountId'])
            if group:
                profile['groupId'] = group['id']
                profile['groupName'] = group['title']

        logins = AuthLoginDao().select_pagination(operId, 0, 10) # 尽可能多
        profile['loginName'] = logins[0]['loginName']

        response = {"errCode": 200, "errMsg": "Success", "data": profile}
        self.write_response(response, logger=False)
        return


    @tornado.web.authenticated  # if no session, redirect to login page
    def put(self):
        try:
            payload = CyJson.loads(self.request.body)
            username = payload['username']
            avatar = payload['avatar']
            title = payload['title']
            description = payload['description'][:255] # 最大255个字符
        except:
            response = {"errCode":400, "errMsg":"Bad Request"}
            self.write_response(response, logger=False)
            return

        operId = self.get_account_id()
        AuthAccountDao().update(operId, username, avatar)
        profile = SysProfileDao().select(operId)
        if profile:
            SysProfileDao().update(operId, title, description)
        else:
            SysProfileDao().insert(operId, title, description)

        response = {"errCode": 200, "errMsg": "Success"}
        self.write_response(response, logger=True)
        return


# /api/sys/profiles/{id}
class SysProfileXHR(AuthorizationHandler):
    # @tornado.web.authenticated  # if no session, redirect to login page
    def get(self, id):
        account = AuthAccountDao().select(id)
        if not account:
            # 返回一个假的
            dummy = {
                "id": id,
                "username": "guest",
                "avatar": DEFAULT_AVATAR,
                "title": "",
                "description": "",
            }
            response = {"errCode": 200, "errMsg": "Success", "data": dummy}
            self.write_response(response, logger=False)
            return


        profile = SysProfileDao().select(id)
        if profile:
            profile['username'] = account['username']
            profile['avatar'] = account['avatar']
        else:
            profile = {
                "id": account['id'],
                "username": account['username'],
                "avatar": account['avatar'],
                "title": "",
                "description": "",
            }

        response = {"errCode": 200, "errMsg": "Success", "data": profile}
        self.write_response(response, logger=False)
        return
