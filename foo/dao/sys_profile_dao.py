#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2022 cyber-life.cn
# thomas@cyber-life.cn

import logging
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "./"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
from foo.comm import *
from foo.dao.mysql_util import *


class SysProfileDao():
    def insert(self, id, title, description):
        sql = """INSERT INTO sys_profile
                 (id, title, description)
                 VALUES (%s, %s, %s)"""
        params = (id, title, description)
        logging.debug(sql, *params)
        rowNum = MysqlUtil().insert_one(sql, params)
        return rowNum


    def select(self,id):
        sql = """SELECT id, title, description
                 FROM sys_profile
                 WHERE id=%s"""
        params = (id,)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data


    def update(self, id, title, description):
        sql = """UPDATE sys_profile
                 SET title=%s, description=%s
                 WHERE id=%s"""
        params = (title, description, id)
        logging.debug(sql, *params)
        rowNum = MysqlUtil().update(sql, params)
        return rowNum
