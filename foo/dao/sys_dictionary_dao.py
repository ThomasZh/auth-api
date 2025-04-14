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


class SysDictionaryDao():
    def insert(self, id, category, sequence, label, value):
        sql = """INSERT INTO sys_dictionary
                 (id, category, sequence, label, value)
                 VALUES (%s, %s, %s, %s, %s)"""
        params = (id, category, sequence, label, value)
        logging.debug(sql, *params)
        rowNum = MysqlUtil().insert_one(sql, params)
        return rowNum


    def select(self,id):
        sql = """SELECT id, category, sequence, label, value
                 FROM sys_dictionary
                 WHERE id=%s"""
        params = (id,)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data


    def selectPagination(self, idx, limit):
        params = (idx, limit)
        sql = """SELECT id, category, sequence, label, value
                 FROM sys_dictionary
                 WHERE 1=1
                 LIMIT %s,%s"""
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        if datas:
            return datas
        else:
            return []


    def countPagination(self):
        sql = """SELECT count(1) AS count
                 FROM sys_dictionary
                 WHERE 1=1 """
        params = ()
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        if data and "count" in data:
            return int(data['count'])
        else:
            return 0


    def selectPaginationByFilters(self, searchs, orders, idx, limit):
        sql = """SELECT id, category, sequence, label, value
                 FROM sys_dictionary
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
                 FROM sys_dictionary
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
        if data and "count" in data:
            return int(data['count'])
        else:
            return 0


    def delete(self, id):
        sql = """DELETE FROM sys_dictionary
                 WHERE id=%s"""
        params = (id,)
        logging.debug(sql, *params)
        rowNum = MysqlUtil().delete(sql, params)
        return  rowNum


    def update(self, id, category, sequence, label, value):
        sql = """UPDATE sys_dictionary
                 SET category=%s, sequence=%s, label=%s, value=%s
                 WHERE id=%s"""
        params = (category, sequence, label, value, id)
        logging.debug(sql, *params)
        rowNum = MysqlUtil().update(sql, params)
        return rowNum
