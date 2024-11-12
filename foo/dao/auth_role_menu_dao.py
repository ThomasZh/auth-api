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


class AuthRoleMenuDao():
    def select_menus_pagination(self, roleId, start, limit):
        sql = """SELECT a.id,a.seq,a.type,a.name,a.icon,a.url
                 FROM auth_menu a,auth_role_menu b
                 WHERE a.id=b.menuId
                 AND b.roleId=%s
                 ORDER BY a.seq DESC
                 LIMIT %s,%s"""
        params = (roleId,start,limit)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        return datas


    def count_menus(self, roleId):
        sql = """SELECT count(1) AS count
                 FROM auth_menu a,auth_role_menu b
                 WHERE a.id=b.menuId
                 AND b.roleId=%s"""
        params = (roleId,)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data['count']


    def insert(self, roleId,menuId):
        sql = """INSERT INTO auth_role_menu (menuId,roleId)
                 VALUES(%s, %s)"""
        params = (menuId,roleId)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().insert_one(sql, params)
        return rowcount


    def delete(self, roleId,menuId):
        sql = """DELETE FROM auth_role_menu
                 WHERE menuId=%s
                 AND roleId=%s"""
        params = (menuId,roleId)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().delete(sql, params)
        return rowcount


    def count(self, roleId, menuId):
        sql = """SELECT count(1) AS count
                 FROM auth_role_menu
                 WHERE roleId=%s
                 AND menuId=%s"""
        params = (roleId,menuId)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data['count']
