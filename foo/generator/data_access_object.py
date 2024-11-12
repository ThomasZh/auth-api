#!/usr/bin/env python
# _*_ coding: utf-8_*_
from fetch_data import fetch_testdata, fetch_db_data

# 必须保留的函数
# 读取数据: 从测试文件中获取数据, 从数据库中读取数据; 二者任选其一
def fetch_data(reportId, parad):
	resultset = fetch_testdata(reportId, parad) # 从测试文件中获取数据
	#resultset = {"sheet_name": "report"}
	#rsParam = "post"
	#parad = {"method": ["POST"]}
	#data = fetch_db_data(reportId, rsParam, parad) # 从数据库中读取数据
	#resultset[rsParam] = data[rsParam]

	return resultset

# 必须保留的函数
# 写入excel文件
def write_excel(data, writer_cls, tpl_fname, result_fname):
	writer = writer_cls(tpl_fname)
	writer.render_sheet(data)
	writer.save(result_fname)
