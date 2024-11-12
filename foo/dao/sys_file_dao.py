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


class SysFileDao():
    def selectPagination(self, start, limit):
        sql = """SELECT id,localUrl,cloudUrl,filetype,filename,blobTotalNum,size,ctime,ext,accountId,bizid
                 FROM sys_file
                 ORDER BY ctime DESC
                 LIMIT %s,%s"""
        params = (start,limit)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        return datas


    def count(self):
        params = ()
        sql = """SELECT count(1) AS count
                 FROM sys_file"""
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        if data and 'count' in data:
            return data['count']
        else:
            return 0


    def selectPaginationByFilters(self, searchs, orders, idx, limit):
        sql = """SELECT id,localUrl,cloudUrl,filetype,filename,blobTotalNum,size,ctime,ext,accountId,bizid
                 FROM sys_file
                 WHERE 1=1 """
        params = ()

        if searchs and len(searchs) > 0:
            for i in range(len(searchs)):
                search = searchs[i]
                # 当X为None,  False, 空字符串"", 0, 空列表[], 空字典{}, 空元组()这些时，not X为真，即无法分辨出他们之间的不同。
                if "value" in search and (not search['value'] is None):
                    if search['op'] == "like":
                        sql = sql + " AND " + search['column'] + " LIKE %s "
                        params = params + ("%"+search['value']+"%",)
                    elif search['op'] == "eq":
                        sql = sql + " AND " + search['column'] + " = %s "
                        params = params + (search['value'],)
                    elif search['op'] == "gt":
                        sql = sql + " AND " + search['column'] + " > %s "
                        params = params + (search['value'],)
                    elif search['op'] == "lt":
                        sql = sql + " AND " + search['column'] + " < %s "
                        params = params + (search['value'],)
                    elif search['op'] == "ge":
                        sql = sql + " AND " + search['column'] + " >= %s "
                        params = params + (search['value'],)
                    elif search['op'] == "le":
                        sql = sql + " AND " + search['column'] + " <= %s "
                        params = params + (search['value'],)
                    elif search['op'] == "ne":
                        sql = sql + " AND " + search['column'] + " <> %s "
                        params = params + (search['value'],)
                    elif search['op'] == "in":
                        arr = []
                        # 当X为None,  False, 空字符串"", 0, 空列表[], 空字典{}, 空元组()这些时，not X为真，即无法分辨出他们之间的不同。
                        if "value" in search and (not search['value'] is None):
                            arr = search['value']
                        if arr and len(arr) > 0:
                            sql = sql + " AND " + search['column'] + " IN( "
                            for i in range(len(arr)):
                                item = arr[i]
                                if i == len(arr) -1:
                                    sql = sql + " %s"
                                else:
                                    sql = sql + " %s,"
                                params = params + (item,)
                            sql = sql + " ) "

        if orders and len(orders) > 0:
            sql = sql + " ORDER BY "
            for i in range(len(orders)):
                order = orders[i]
                if i == len(orders) -1:
                    sql = sql + order['column'] + " " + order['dir']
                else:
                    sql = sql + order['column'] + " " + order['dir'] + ","

        sql = sql + " LIMIT %s,%s"
        params = params + (idx, limit)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        if datas:
            return datas
        else:
            return []


    def countPaginationByFilters(self, searchs):
        sql = """SELECT count(1) AS count
                 FROM sys_file
                 WHERE 1=1 """
        params = ()

        if searchs and len(searchs) > 0:
            for i in range(len(searchs)):
                search = searchs[i]
                # 当X为None,  False, 空字符串"", 0, 空列表[], 空字典{}, 空元组()这些时，not X为真，即无法分辨出他们之间的不同。
                if "value" in search and (not search['value'] is None):
                    if search['op'] == "like":
                        sql = sql + " AND " + search['column'] + " LIKE %s "
                        params = params + ("%"+search['value']+"%",)
                    elif search['op'] == "eq":
                        sql = sql + " AND " + search['column'] + " = %s "
                        params = params + (search['value'],)
                    elif search['op'] == "gt":
                        sql = sql + " AND " + search['column'] + " > %s "
                        params = params + (search['value'],)
                    elif search['op'] == "lt":
                        sql = sql + " AND " + search['column'] + " < %s "
                        params = params + (search['value'],)
                    elif search['op'] == "ge":
                        sql = sql + " AND " + search['column'] + " >= %s "
                        params = params + (search['value'],)
                    elif search['op'] == "le":
                        sql = sql + " AND " + search['column'] + " <= %s "
                        params = params + (search['value'],)
                    elif search['op'] == "ne":
                        sql = sql + " AND " + search['column'] + " <> %s "
                        params = params + (search['value'],)
                    elif search['op'] == "in":
                        arr = []
                        # 当X为None,  False, 空字符串"", 0, 空列表[], 空字典{}, 空元组()这些时，not X为真，即无法分辨出他们之间的不同。
                        if "value" in search and (not search['value'] is None):
                            arr = search['value']
                        if arr and len(arr) > 0:
                            sql = sql + " AND " + search['column'] + " IN( "
                            for i in range(len(arr)):
                                item = arr[i]
                                if i == len(arr) -1:
                                    sql = sql + " %s"
                                else:
                                    sql = sql + " %s,"
                                params = params + (item,)
                            sql = sql + " ) "

        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        if data and 'count' in data:
            return data['count']
        else:
            return 0


    def select(self, id):
        sql = """SELECT id,localUrl,cloudUrl,filetype,filename,blobTotalNum,size,ctime,ext,accountId,bizid
                 FROM sys_file
                 WHERE id=%s"""
        params = (id,)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data


    def selectByLocalUrl(self, localUrl):
        sql = """SELECT id,localUrl,cloudUrl,filetype,filename,blobTotalNum,size,ctime,ext,accountId,bizid
                 FROM sys_file
                 WHERE localUrl=%s"""
        params = (localUrl,)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data


    def insert(self, id,localUrl,filetype,filename,blobTotalNum,size,ext,accountId,bizid):
        sql = """INSERT INTO sys_file
                 (id,localUrl,filetype,filename,blobTotalNum,size,ext,accountId,bizid)
                 VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (id,localUrl,filetype,filename,blobTotalNum,size,ext,accountId,bizid)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().insert_one(sql, params)
        return rowcount


    def updateFilename(self, id, filename):
        sql = """UPDATE sys_file
                 SET filename=%s
                 WHERE id=%s"""
        params = (filename, id)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def updateCloudUrl(self, id, cloudUrl):
        sql = """UPDATE sys_file
                 SET cloudUrl=%s
                 WHERE id=%s"""
        params = (cloudUrl, id)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def update(self, id,localUrl,filetype,filename,blobTotalNum,size,ext,accountId,bizid):
        sql = """UPDATE sys_file
                 SET localUrl=%s,filetype=%s,filename=%s,blobTotalNum=%s,size=%s,ext=%s,accountId=%s,bizid=%s
                 WHERE id=%s"""
        params = (localUrl,filetype,filename,blobTotalNum,size,ext,accountId,bizid, id)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def delete(self, id):
        sql = """DELETE FROM sys_file
                 WHERE id=%s"""
        params = (id,)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().delete(sql, params)
        return rowcount
