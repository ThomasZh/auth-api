#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016 7x24hs.com
# thomas@7x24hs.com
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
from comm import *
from global_const import *
from mysql_util import *


class AuthLoginDao():

    def insert(self, loginName,password,type,accountId):
        _dt = timestamp_to_datetime(current_timestamp())
        sql = """INSERT INTO auth_login (loginName,password,type,accountId,ctime)
                 VALUES(%s, %s, %s, %s, %s)"""
        params = (loginName,password,type,accountId,_dt)
        logging.debug(sql, *params)
        rowNum = MysqlUtil().insert_one(sql, params)
        return rowNum


    def selectById(self, accountId):
        sql = """SELECT loginName,password,type,accountId,status
                 FROM auth_login
                 WHERE accountId=%s"""
        params = (accountId,)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data


    def select(self, loginName):
        sql = """SELECT loginName,password,type,accountId,status
                 FROM auth_login
                 WHERE loginName=%s"""
        params = (loginName,)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data


    def fuzzy_search(self, loginName, start, limit):
        sql = """SELECT l.loginName,l.accountId
                 FROM auth_login l, auth_account a
                 WHERE l.accountId = a.id
                 AND a.status = 0
                 AND l.loginName like %s
                 ORDER BY l.ctime DESC
                 LIMIT %s,%s"""
        params = ("%"+loginName+"%",start, limit)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        return datas


    def count_fuzzy_search(self, loginName):
        sql = """SELECT count(1) AS count
                 FROM auth_login l, auth_account a
                 WHERE l.accountId = a.id
                 AND a.status = 0
                 AND l.loginName like %s"""
        params = ("%"+loginName+"%",)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data['count']


    def update_pwd(self, loginName, password):
        sql = """UPDATE auth_login
                 SET password=%s
                 WHERE loginName=%s"""
        params = (password, loginName)
        logging.debug(sql, *params)
        rowNum = MysqlUtil().update(sql, params)
        return rowNum


    def select_pagination(self, accountId, start, limit):
        sql = """SELECT loginName,type,status,ctime
                 FROM auth_login
                 WHERE accountId=%s
                 ORDER BY ctime DESC
                 LIMIT %s,%s"""
        params = (accountId, start, limit)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        return datas


    def count(self, accountId):
        params = (accountId,)
        sql = """SELECT count(1) AS count
                 FROM auth_login
                 WHERE accountId=%s"""
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data['count']
