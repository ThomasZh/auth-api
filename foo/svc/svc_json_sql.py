#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2022 cyber-life.cn
# thomas@cyber-life.cn


import logging
import sys
import os
import requests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from global_const import *
from foo.svc_config import GlobalConfig
from comm import *
import json as JSON # 启用别名，不会跟方法里的局部变量混淆
from foo.dao.mysql_util import *


# 把字典数据转化为元祖数据
def dict_to_tuple(dict):
    arr = []
    # print(u"总字段数:"+str(len(dict)))
    for i in dict.keys():
        obj = dict[i]
        if isinstance(obj, bool):
            arr.append(obj)
        elif isinstance(obj, int):
            arr.append(obj)
        elif isinstance(obj, float):
            arr.append(obj)
        elif isinstance(obj, str):
            arr.append(obj)
        else:
            arr.append(JSON.dumps(obj))

    map = tuple(arr)
    return map


#根据元祖数据生成mysql语句
def make_create_sql(tablename, dict):
    str1 = "CREATE TABLE IF NOT EXISTS `%s`\n" %(tablename)
    arr1 = []
    for i in dict:
        obj = dict[i]
        if isinstance(obj, bool):
            str3 = "`" + i + "` TINYINT(1) DEFAULT '0'"
        elif isinstance(obj, int):
            str3 = "`" + i + "` varchar(255) DEFAULT NULL"
        elif isinstance(obj, float):
            str3 = "`" + i + "` varchar(255) DEFAULT NULL"
        elif isinstance(obj, str):
            if i == "id":
                str3 = "`" + i + "` varchar(255) NOT NULL"
            else:
                str3 = "`" + i + "` varchar(255) DEFAULT NULL"
        else:
            str3 = "`" + i + "` json DEFAULT NULL"
        arr1.append(str3)

    str3 = "`ctime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP"
    arr1.append(str3)
    if "id" not in dict:
        str3 = "`id` varchar(45) NOT NULL"
        arr1.append(str3)
    # str5 = "(" + str4.rstrip(",") + ",\n"
    str4 = "PRIMARY KEY (`id`)"
    arr1.append(str4)
    str5 = ",\n".join(arr1)
    str6 = "(" + str5.rstrip(",") + ")\n"
    str2 = "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
    str8 = str1 + " " + str6 + str2
    return str8


# dictionary object to mysql create statement
def build_create_stmt(tablename, dict):
    # tuple = dict_to_tuple(dict)
    # print(tuple)
    sql = make_create_sql(tablename, dict)
    return sql


# dictionary object to mysql insert statement
def build_insert_stmt(tablename, dict):
    str1 = "INSERT INTO `%s` (" %(tablename)
    arr1 = []
    arr2 = []
    for i in dict:
        arr1.append("`" + i + "`")
        arr2.append("%s")
    # if "id" not in dict:
    #     arr1.append("`id`")
    #     arr2.append(generate_uuid_str())
    str4 = ",".join(arr1)
    str5 = ",".join(arr2)
    sql = str1 + str4 + ") \n VALUES (" + str5 +")"
    return sql


# dictionary object to mysql update statement
def build_update_stmt(tablename, dict, pk):
    # 删除 pk
    if pk in dict:
        del dict[pk]

    str1 = "UPDATE `%s` \nSET " %(tablename)
    arr1 = []
    for i in dict:
        arr1.append(i + "=%s")
    str4 = ",".join(arr1)
    arr2 = []
    str5 = "\nWHERE " + pk + "=%s"
    sql = str1 + str4 + str5
    return sql


# dictionary object to mysql update params
def build_update_params(dict, pk, pk_value):
    # 删除 pk
    if pk in dict:
        del dict[pk]

    arr = []
    # print(u"总字段数:"+str(len(dict)))
    for i in dict.keys():
        obj = dict[i]
        if isinstance(obj, bool):
            arr.append(obj)
        elif isinstance(obj, int):
            arr.append(obj)
        elif isinstance(obj, float):
            arr.append(obj)
        elif isinstance(obj, str):
            arr.append(obj)
        else:
            arr.append(JSON.dumps(obj))

    # 将 pk 加到最后的位置
    arr.append(pk_value)
    map = tuple(arr)
    return map


# dictionary object to mysql delete statement
def build_delete_stmt(tablename, pk):
    str1 = "DELETE FROM `%s`" %(tablename)
    str5 = "\nWHERE " + pk + "=%s"
    sql = str1 + str5
    return sql


def diff_column_name(dict, columns):
    arr = []
    # print(u"总字段数:"+str(len(dict)))
    for i in dict.keys():
        arr.append(i)
    # 获得两个数组差集
    return list(set(arr).difference(set(columns))) # b中有而a中没有的


# dictionary object to mysql create statement
def build_alter_stmt(tablename, diffs, dict):
    arr = []
    for diff in diffs:
        str1 = "ALTER TABLE `%s`\n" %(tablename)
        obj = dict[diff]
        if isinstance(obj, bool):
            str2 = "ADD COLUMN `%s` TINYINT(1) DEFAULT '0'" %(diff)
        elif isinstance(obj, int):
            str2 = "ADD COLUMN `%s` VARCHAR(255) NULL" %(diff)
        elif isinstance(obj, float):
            str2 = "ADD COLUMN `%s` VARCHAR(255) NULL" %(diff)
        elif isinstance(obj, str):
            str2 = "ADD COLUMN `%s` VARCHAR(255) NULL" %(diff)
        else:
            str2 = "ADD COLUMN `%s` json NULL" %(diff)
        sql = str1 + str2
        # print(sql)
        arr.append(sql)
    return arr


# 1.如果表不存在, 创建数据表
def mysql_create_table(tablename, dict):
    sql = build_create_stmt(tablename, dict)
    params = ()
    MysqlUtil().update(sql, params)


# 2.判断数据库表结构是否有变化
def mysql_alter_table(tablename, dict):
    columns = MysqlUtil().getColumnNames(tablename)
    if columns:
        diffs = diff_column_name(dict, columns)
        sqls = build_alter_stmt(tablename, diffs, dict)
        for sql in sqls:
            params = ()
            MysqlUtil().update(sql, params)


# 3.插入数据
def mysql_insert_table(tablename, dict):
    sql = build_insert_stmt(tablename, dict)
    params = dict_to_tuple(dict)
    MysqlUtil().update(sql, params)


# 4.修改数据
def mysql_update_table(tablename, dict, pk, pk_value):
    sql = build_update_stmt(tablename, dict, pk)
    params = build_update_params(dict, pk, pk_value)
    MysqlUtil().update(sql, params)


# 5.删除数据
def mysql_delete_table(tablename, pk, pk_value):
    sql = "DELETE FROM " + tablename + " WHERE " + pk + "=%s"
    params = (pk_value)
    MysqlUtil().update(sql, params)


if __name__ == '__main__':
    #这里设置表名
    tablename = "cyber_test12"
    #这里设置需要的字典数据
    dict = {
        "id": "971",
        "payout_id": "10602",
        "payin_id": "0",
        "pay_nums": 500.00,
        "pay_state": True,
        "pay_time": 1536829856,
        "pay_no": "PAY2018091348534951",
        "card_id": "664",
        "trade_notes": "null",
        "trans_type": "0",
        "trans_img": "null",
        "get_moneytime": "null",
        "fee_nums": 100.00,
        "out_card": "null",
        "datas": [
			{
				"date": "2022-03-27",
				"value": 0,
				"tasks": []
			},
			{
				"date": "2022-03-28",
				"value": 0,
				"tasks": []
			},
        ]
    }
    columns = [
        "id",
        "payout_id",
        "payin_id",
        "pay_nums",
        "pay_state",
        "pay_time",
        "pay_no",
        "card_id",
    ]

    sql = build_create_stmt(tablename, dict)
    print(sql)
    sql = build_insert_stmt(tablename, dict)
    params = dict_to_tuple(dict)
    print(sql)
    print(params)

    pk = "id"
    pk_value = dict[pk]
    sql = build_update_stmt(tablename, dict, pk)
    params = build_update_params(dict, pk, pk_value)
    print(sql)
    print(params)

    diffs = diff_column_name(dict, columns)
    sql = build_alter_stmt(tablename, diffs, dict)
    print(sql)

    sql = build_delete_stmt(tablename, pk)
    print(sql)
