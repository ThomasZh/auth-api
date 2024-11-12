#!/usr/bin/python3
# _*_ coding: utf-8_*_
#
# Copyright 2022 cyber-life.cn
# thomas@cyber-life.cn

import logging
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "./"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
from foo.comm import *
from foo.dao.mysql_util import *


class AuthAppRoleDao():
    def insert(self, appId, roleId):
        sql = """INSERT INTO auth_app_role
                 (appId, roleId)
                 VALUES (%s, %s)"""
        params = (appId, roleId)
        logging.debug(sql, *params)
        rowNum = MysqlUtil().insert_one(sql, params)
        return rowNum


    def select_roles_pagination(self, appId, idx, limit):
        params = (appId, idx, limit)
        sql = """SELECT appId, roleId AS id
                 FROM auth_app_role
                 WHERE appId=%s
                 LIMIT %s,%s"""
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        if datas:
            return datas
        else:
            return []


    def count_roles_pagination(self, appId):
        sql = """SELECT count(1) AS count
                 FROM auth_app_role
                 WHERE appId=%s """
        params = (appId,)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        if data and "count" in data:
            return int(data['count'])
        else:
            return 0
