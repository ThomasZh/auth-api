#!/usr/bin/env python
# _*_ coding: utf-8_*_
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "../.."))
from urllib import parse
from xltpl.writerx import BookWriter as BookWriterx
from data_access_object import fetch_data, write_excel


def main(reportId, query, templateId, templatePath, outputId, outputPath):
	if query != "None":
		parad = parse.parse_qs(query)
	else:
		parad = None
	data = fetch_data(reportId, parad)

	tpl_name = templatePath + '/' + templateId + '.xlsx'
	result_fname = outputPath + '/' + outputId + '.xlsx'
	write_excel(data, BookWriterx, tpl_name, result_fname)

	# 文件转换格式为 html, 提供给报表界面使用
	# command = "/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to html --outdir " + outputPath + " " + result_fname
	# ubuntu
	command = "/usr/bin/soffice --headless --convert-to html --outdir " + outputPath + " " + result_fname
	os.system(command)
	# 文件转换格式为 pdf, 提供给打印使用
	# command = "/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf --outdir " + outputPath + " " + result_fname
	# ubuntu
	command = "/usr/bin/soffice --headless --convert-to pdf --outdir " + outputPath + " " + result_fname
	os.system(command)


if __name__ == '__main__':
	if len(sys.argv) < 6:
		print ("usage: python3 REPORT_ID.py reportId query templateId templatePath outputId outputPath")
	else:
		reportId = sys.argv[1]
		query = sys.argv[2]
		templateId = sys.argv[3]
		templatePath = sys.argv[4]
		outputId = sys.argv[5]
		outputPath = sys.argv[6]
		main(reportId, query, templateId, templatePath, outputId, outputPath)
