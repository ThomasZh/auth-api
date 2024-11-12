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


class SysLogDao():
    def insert(self, accountId, username, method, path, params, body, respCode, respMsg, ipAddr, userAgent):
        sql = """INSERT INTO sys_log
                 (accountId, username, method, path, params, body, respCode, respMsg, ipAddr, userAgent)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (accountId, username, method, path, params, body, respCode, respMsg, ipAddr, userAgent)
        logging.debug(sql, *params)
        rowNum = MysqlUtil().insert_one(sql, params)
        return rowNum


    def selectPaginationByFilters(self, searchs, orders, idx, limit):
        sql = """SELECT id, accountId, username, path, method, params, body, respCode, respMsg, ctime, ipAddr, userAgent
                 FROM sys_log
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
                 FROM sys_log
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
        return data['count']
