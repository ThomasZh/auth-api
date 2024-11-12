#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2016 7x24hs.com
# thomas@7x24hs.com

import logging
import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "./"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
from comm import *
from global_const import *
from mysql_util import *


class AuthAccountDao():

    def insert(self, accountId, username, avatar):
        _dt = timestamp_to_datetime(current_timestamp())
        sql = """INSERT INTO auth_account (id,username, avatar,ctime)
                 VALUES(%s, %s, %s, %s)"""
        params = (accountId, username, avatar, _dt)
        logging.debug(sql, *params)
        rowNum = MysqlUtil().insert_one(sql, params)
        return rowNum


    def select(self, accountId):
        sql = """SELECT id AS accountId,username,avatar,status,ctime
                 FROM auth_account
                 WHERE id=%s"""
        params = (accountId,)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data


    def update_status(self, accountId, status):
        sql = """UPDATE auth_account
                 SET status=%s
                 WHERE id=%s"""
        params = (status, accountId)
        logging.debug(sql, *params)
        rowNum = MysqlUtil().update(sql, params)
        return rowNum


    def update(self, accountId, username, avatar):
        sql = """UPDATE auth_account
                 SET username=%s,avatar=%s
                 WHERE id=%s"""
        params = (username, avatar, accountId)
        logging.debug(sql, *params)
        rowNum = MysqlUtil().update(sql, params)
        return rowNum


    def select_pagination(self, start, limit):
        sql = """SELECT id AS accountId,username,avatar,status,ctime
                 FROM auth_account
                 WHERE 1=1
                 ORDER BY ctime DESC
                 LIMIT %s,%s"""
        params = (start,limit)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        return datas


    def count(self):
        sql = """SELECT count(1) AS count
                 FROM auth_account"""
        params = ()
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data['count']


    def select_pagination_by_role(self, roleId, start, limit):
        sql = """SELECT id AS accountId,username,avatar,status,ctime
                 FROM auth_account a, auth_account_role b
                 WHERE a.id=b.accountId
                 AND b.roleId=%s
                 ORDER BY ctime DESC
                 LIMIT %s,%s"""
        params = (roleId, start,limit)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        return datas


    def count_by_role(self, roleId):
        sql = """SELECT count(1) AS count
                 FROM auth_account a, auth_account_role b
                 WHERE a.id=b.accountId
                 AND b.roleId=%s"""
        params = (roleId)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data['count']


    def select_pagination_by_group(self, groupId, start, limit):
        sql = """SELECT id AS accountId,username,avatar,status,ctime
                 FROM auth_account a, auth_account_group b
                 WHERE a.id=b.accountId
                 AND b.groupId=%s
                 ORDER BY ctime DESC
                 LIMIT %s,%s"""
        params = (groupId, start,limit)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        return datas


    def count_by_group(self, groupId):
        sql = """SELECT count(1) AS count
                 FROM auth_account a, auth_account_group b
                 WHERE a.id=b.accountId
                 AND b.groupId=%s"""
        params = (groupId)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data['count']


    def selectPaginationByFilters(self, searchs, orders, idx, limit):
        sql = """SELECT id AS accountId,username,avatar,status,ctime
                 FROM auth_account
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
                 FROM auth_account
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
