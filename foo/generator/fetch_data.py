#!/usr/bin/env python
# _*_ coding: utf-8_*_
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "../.."))
from function.json_transform_excel import read_from_json
from svc.svc_datasource import exec_report_sql_schema

# 从测试文件中获取数据
def fetch_testdata(reportId, parad):
	WORK_DIR = os.path.dirname(__file__) # 当前文件所在的目录
	testdata_fname = WORK_DIR + "/../" + reportId + "/testdata.json"
	return read_from_json(testdata_fname)

# 从数据库中读取数据
def fetch_db_data(reportId, rsParam, parad):
	response = exec_report_sql_schema(reportId, rsParam, parad)
	if response['errCode'] != 200:
		print(response['errMsg'])
	return response['data']
