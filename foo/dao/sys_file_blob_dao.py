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


class SysFileBlobDao():
    def count(self, fileId, bizid):
        sql = """SELECT count(1) AS count
                 FROM sys_file_blob
                 WHERE id=%s
                 AND bizid=%s"""
        params = (fileId,bizid)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data['count']


    def insert(self, id,bizid,blobCurrNum,blobTotalNum,accountId):
        sql = """INSERT INTO sys_file_blob
                 (id,bizid,blobCurrNum,blobTotalNum,accountId)
                 VALUES(%s, %s, %s, %s, %s)"""
        params = (id,bizid,blobCurrNum,blobTotalNum,accountId)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().insert_one(sql, params)
        return rowcount


    def delete(self, id):
        sql = """DELETE FROM sys_file_blob
                 WHERE id=%s"""
        params = (id,)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().delete(sql, params)
        return rowcount


    def delete_exclude(self, id, bizid):
        sql = """DELETE FROM sys_file_blob
                 WHERE id=%s
                 AND bizid != %s"""
        params = (id,bizid)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().delete(sql, params)
        return rowcount
