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


'''
预排序遍历树算法(modified preorder tree traversal algorithm)

参考：https://www.cnblogs.com/analyzer/articles/1029395.html

注意：由于"left"和"right"在 SQL中有特殊的意义，所以我们需要用"lft"和"rgt"来表示左右字段。
另外这种结构中不再需要"parent"字段来表示树状结构。也就是说下面这样的表结构就足够了。

+------------+-----+-----+
| name | lft | rgt |
+------------+-----+-----+
| Food | 1 | 18 |
| Fruit | 2 | 11 |
| Red | 3 | 6 |
| Cherry | 4 | 5 |
| Yellow | 7 | 10 |
| Banana | 8 | 9 |
| Meat | 12 | 17 |
| Beef | 13 | 14 |
| Pork | 15 | 16 |
+------------+-----+-----+

但是，我们仍然保留"parent"字段。
从数据库拿出数组后，通过python函数将其转换为为树状结构。
然后，提供给界面程序使用
+-----------------------+-----+-----+
| parent | title | lft | rgt |
+-----------------------+-----+-----+
| | Food | 1 | 18 |
| Food | Fruit | 2 | 11 |
| Fruit | Red | 3 | 6 |
| Red | Cherry | 4 | 5 |
| Fruit | Yellow | 7 | 10 |
| Yellow | Banana | 8 | 9 |
| Food | Meat | 12 | 17 |
| Meat | Beef | 13 | 14 |
| Meat | Pork | 15 | 16 |
+-----------------------+-----+-----+
'''
class AuthGroupDao():

    def insert(self, id,pid,title,lft,rgt,depth):
        sql = """INSERT INTO auth_group (id,pid,title,lft,rgt,depth)
                 VALUES(%s, %s, %s, %s, %s, %s)"""
        params = (id,pid,title,lft,rgt,depth)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().insert_one(sql, params)
        return rowcount


    def update_title(self, id, title):
        sql = """UPDATE auth_group
                 SET title=%s
                 WHERE id=%s"""
        params = (title, id)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def increase_lft(self, lft):
        sql = """UPDATE auth_group
                 SET lft=lft+2
                 WHERE lft>%s"""
        params = (lft,)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def increase_lft_num(self,lft,num):
        sql = """UPDATE auth_group
                 SET lft=lft+%s
                 WHERE lft>%s"""
        params = (num,lft)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def increase_lft_num_between(self,lft,rgt,num):
        sql = """UPDATE auth_group
                 SET lft=lft+%s
                 WHERE lft>=%s
                 AND rgt<=%s"""
        params = (num,lft,rgt)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def increase_rgt(self, rgt):
        sql = """UPDATE auth_group
                 SET rgt=rgt+2
                 WHERE rgt>%s"""
        params = (rgt,)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def increase_rgt_num(self,rgt,num):
        sql = """UPDATE auth_group
                 SET rgt=rgt+%s
                 WHERE rgt>%s"""
        params = (num,rgt)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def increase_rgt_num_between(self,lft,rgt,num):
        sql = """UPDATE auth_group
                 SET rgt=rgt+%s
                 WHERE lft>=%s
                 AND rgt<=%s"""
        params = (num,lft,rgt)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def decrease_lft(self, lft):
        sql = """UPDATE auth_group
                 SET lft=lft-2
                 WHERE lft>%s"""
        params = (lft,)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def decrease_lft_num(self,lft,num):
        sql = """UPDATE auth_group
                 SET lft=lft-%s
                 WHERE lft>%s"""
        params = (num,lft)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def decrease_lft_num_between(self,lft,rgt,num):
        sql = """UPDATE auth_group
                 SET lft=lft-%s
                 WHERE lft>=%s
                 AND rgt<=%s"""
        params = (num,lft,rgt)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def decrease_rgt(self, rgt):
        sql = """UPDATE auth_group
                 SET rgt=rgt-2
                 WHERE rgt>%s"""
        params = (rgt,)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def decrease_rgt_num(self,rgt,num):
        sql = """UPDATE auth_group
                 SET rgt=rgt-%s
                 WHERE rgt>%s"""
        params = (num,rgt)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def decrease_rgt_num_between(self,lft,rgt,num):
        sql = """UPDATE auth_group
                 SET rgt=rgt-%s
                 WHERE lft>=%s
                 AND rgt<=%s"""
        params = (num,lft,rgt)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def update_rgt(self, id, rgt):
        sql = """UPDATE auth_group
                 SET rgt=%s
                 WHERE id=%s"""
        params = (rgt,id)
        logging.debug(sql, *params)
        data = MysqlUtil().update(sql, params)
        return data


    def select(self, id):
        sql = """SELECT id,pid,title,lft,rgt,depth
                 FROM auth_group
                 WHERE id=%s"""
        params = (id,)
        logging.debug(sql, *params)
        data = MysqlUtil().query_one(sql, params)
        return data


    def select_tree(self, lft, rgt):
        sql = """SELECT id,pid,title,lft,rgt,depth
                 FROM auth_group
                 WHERE lft BETWEEN %s AND %s
                 ORDER BY lft ASC"""
        params = (lft, rgt)
        logging.debug(sql, *params)
        datas = MysqlUtil().query_all(sql, params)
        return datas


    def delete(self, id):
        sql = """DELETE FROM auth_group
                 WHERE id=%s"""
        params = (id,)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().delete(sql, params)
        return rowcount


    def delete_by_lft_rgt(self, lft, rgt):
        sql = """DELETE FROM auth_group
                 WHERE lft>=%s
                 AND rgt<=%s"""
        params = (lft, rgt)
        logging.debug(sql, *params)
        rowcount = MysqlUtil().delete(sql, params)
        return rowcount
