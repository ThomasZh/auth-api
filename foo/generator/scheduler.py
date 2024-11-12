#!/usr/bin/env python
# _*_ coding: utf-8_*_
import datetime
from urllib.parse import urlencode

def generator_args():
	# 获取当前日期和时间
	now = datetime.datetime.now()
	params = {
		"year":now.year,
		"month":now.month,
		"day":now.day
	}
	query_string = urlencode(params)
	return query_string

if __name__ == '__main__':
	query_string = generator_args()
	# 打印结果
	print(query_string)
