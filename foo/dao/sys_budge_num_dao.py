#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016 7x24hs.com
# thomas@7x24hs.com

import logging
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "./"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
from foo.comm import *
from foo.dao.mysql_util import *


class SysBudgeNumDao():
    def insert(self, objType,objId,budgeName,num):
        _dt = timestamp_to_datetime(current_timestamp())
        sql = """INSERT INTO sys_budge_num
                 (objType,objId,budgeName,num)
                 VALUES(%s, %s, %s, %s)"""
        params = (objType,objId,budgeName,num)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().insert_one(sql, params)
        return rowcount


    def select(self, objType,objId,budgeName):
        sql = """SELECT objType,objId,budgeName,num
                 FROM sys_budge_num
                 WHERE objType=%s
                 AND objId=%s
                 AND budgeName=%s"""
        params = (objType,objId,budgeName)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data


    def select_all(self, objType,objId):
        sql = """SELECT objType,objId,budgeName,num
                 FROM sys_budge_num
                 WHERE objType=%s
                 AND objId=%s"""
        params = (objType,objId,budgeName)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        return datas


    def update_num(self, objType,objId,budgeName,num):
        sql = """UPDATE sys_budge_num
                 SET num=%s
                 WHERE objType=%s
                 AND objId=%s
                 AND budgeName=%s"""
        params = (num,objType,objId,budgeName)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def increase_num(self, objType,objId,budgeName,num):
        obj = self.select(objType,objId,budgeName)
        if obj:
            sql = """UPDATE sys_budge_num
                     SET num=num+%s
                     WHERE objType=%s
                     AND objId=%s
                     AND budgeName=%s"""
            params = (num,objType,objId,budgeName)
            logging.debug(sql, *params)
            data = MysqlUtil().update(sql, params)
            return data
        else:
            self.insert(objType,objId,budgeName,num)


    def decrease_num(self, objType,objId,budgeName,num):
        obj = self.select(objType,objId,budgeName)
        if obj:
            if obj['num'] > num:
                sql = """UPDATE sys_budge_num
                         SET num=num-%s
                         WHERE objType=%s
                         AND objId=%s
                         AND budgeName=%s"""
                params = (num,objType,objId,budgeName)
                logging.debug(sql, *params)
                rowcount = MysqlUtil().update(sql, params)
                return rowcount
            else:
                sql = """UPDATE sys_budge_num
                         SET num=0
                         WHERE objType=%s
                         AND objId=%s
                         AND budgeName=%s"""
                params = (objType,objId,budgeName)
                logging.debug(sql, *params)
                rowcount = MysqlUtil().update(sql, params)
                return rowcount
