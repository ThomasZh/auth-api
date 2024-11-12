#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2021 cyber-life.cn
# thomas@cyber-life.cn
# @2021/06/21

import os.path
import ssl
import signal
import sys
import logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "./"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from foo.comm import *
from foo.dao.mysql_util import *


# 前置条件：数据库表中必须有一条记录
def main(tableName):
    # tableName = "client"
    className = tableName.title()
    className = className.replace("_", "")
    columnNames = MysqlUtil().query_columns(tableName)

    updateColumnNames = []
    for columnName in columnNames:
        if columnName == "id":
            continue
        if columnName == "ctime":
            continue
        elif columnName == "mtime":
            continue
        elif columnName == "status":
            continue
        else:
            updateColumnNames.append(columnName)

    strColumnNames = ', '.join(updateColumnNames)
    print("columnNames", strColumnNames)
    payload = ""
    for columnName in updateColumnNames:
        if columnName == "data":
            payload = payload + "            "+ columnName + " = JSON.dumps(payload['"+columnName+"'])\n"
        else:
            payload = payload + "            "+ columnName + " = payload['"+columnName+"']\n"
    print("payload", payload)

    # Reading the file as one file stream
    read_file = open('template_api.txt', 'r')
    # Reads the entire file at once and places the contents in memory.
    read_content = read_file.read()
    read_content = read_content.replace("__class_name__", className)
    read_content = read_content.replace("__table_name__", tableName)
    read_content = read_content.replace("__column_names__", strColumnNames)
    # read_content = read_content.replace("__params__", strParams)
    read_content = read_content.replace("__update_column_names__", strColumnNames)
    read_content = read_content.replace("__payload__", payload)
    # print(read_content)

    # Open the file for appending (a) and begin reading each line
    with open(tableName+'.py', 'w') as write_file:
         write_file.write(read_content)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ("usage: python3 api_generator.py table_name")
    else:
        tableName = sys.argv[1]
        print(tableName)
        main(tableName)
