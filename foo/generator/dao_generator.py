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


'''
    前置条件：数据库表中必须有一条记录
    每一个数据库表都有几个字段：id,ctime,mtime,status
'''
def main(tableName):
    # tableName = "client"
    className = tableName.title()
    className = className.replace("_", "")
    columnNames = MysqlUtil().query_columns(tableName)
    strSelColumnNames = ', '.join(columnNames)
    print("select", strSelColumnNames)

    insertColumnNames = []
    for columnName in columnNames:
        if columnName == "ctime":
            continue
        elif columnName == "mtime":
            continue
        elif columnName == "status":
            continue
        else:
            insertColumnNames.append(columnName)

    strInsertColumnNames = ', '.join(insertColumnNames)
    print("insert", strInsertColumnNames)
    strInsertParams = ""
    for i in range(1, len(insertColumnNames)):
        strInsertParams = strInsertParams + "%s, "
    strInsertParams = strInsertParams + "%s"
    print("insertParams", strInsertParams)

    updateColumnNames = []
    for columnName in columnNames:
        if columnName == "id":
            continue
        if columnName == "ctime":
            continue
        elif columnName == "mtime":
            continue
        elif columnName == "companyId":
            continue
        elif columnName == "status":
            continue
        else:
            updateColumnNames.append(columnName)

    strUpdateColumnNames = ', '.join(updateColumnNames)
    print("update", strUpdateColumnNames)
    strUpdateColumnNamesVars = '=%s, '.join(updateColumnNames)
    strUpdateColumnNamesVars = strUpdateColumnNamesVars + "=%s"
    print("update", strUpdateColumnNamesVars)

    # Reading the file as one file stream
    read_file = open('template_dao.txt', 'r')
    # Reads the entire file at once and places the contents in memory.
    read_content = read_file.read()
    read_content = read_content.replace("__class_name__", className)
    read_content = read_content.replace("__table_name__", tableName)
    read_content = read_content.replace("__select_column_names__", strSelColumnNames)
    read_content = read_content.replace("__insert_column_names__", strInsertColumnNames)
    read_content = read_content.replace("__insert_params__", strInsertParams)
    read_content = read_content.replace("__update_column_names__", strUpdateColumnNames)
    read_content = read_content.replace("__update_column_names_and_vars__", strUpdateColumnNamesVars)
    # print(read_content)

    # Open the file for appending (a) and begin reading each line
    with open(tableName+'_dao.py', 'w') as write_file:
         write_file.write(read_content)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ("usage: python3 dao_generator.py table_name")
    else:
        tableName = sys.argv[1]
        print(tableName)
        main(tableName)
