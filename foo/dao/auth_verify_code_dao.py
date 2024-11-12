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
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "./"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
from foo.comm import *
from foo.dao.mysql_util import *


class AuthVerifyCodeDao():

    def insert(self, loginName,code,expiresAt):
        _dt = timestamp_to_datetime(current_timestamp())
        status = 0
        sql = """INSERT INTO auth_verify_code (loginName,code,ctime,mtime,expiresAt)
                 VALUES(%s, %s, %s, %s, %s)"""
        params = (loginName,code,_dt,_dt,expiresAt)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().insert_one(sql, params)
        return rowcount


    def select(self, loginName):
        sql = """SELECT loginName,code,ctime,mtime,expiresAt
                 FROM auth_verify_code
                 WHERE loginName=%s"""
        params = (loginName,)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data


    def update(self, loginName,code,expiresAt):
        _dt = timestamp_to_datetime(current_timestamp())
        sql = """UPDATE auth_verify_code
                 SET code=%s,mtime=%s,expiresAt=%s
                 WHERE loginName=%s"""
        params = (code, _dt, expiresAt, loginName)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data
