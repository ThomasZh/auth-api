#!/usr/bin/env python
# _*_ coding: utf-8_*_
# from .cy_json import CyJson

class CyColumnUtil:
    def convert_rowdata_to_column_names(row):
        """
        从一行数据获取列名称数组
        :param row: 给出一行数据，类型为字典
        :return: 数组
        """
        return list(row.keys())

    def convert_rowdata_to_column_types(row):
        """
        从一行数据获取列类型数组
        :param row: 给出一行数据，类型为字典
        :return: 数组
        示例: [{"id": "syzk", "key": "syzk", "title": "使用状况", "dataIndex": "syzk"}]
        """
        arr = []
        for k, v in row.items():
            item = {"id": k, "key": k, "title": k, "dataIndex": k}
            arr.append(item)
        return arr

    def convert_rowdata_to_datatype(row):
        """
        从一行数据获取列名称及类型的字典
        :param row: 给出一行数据，类型为字典
        :return: 字典
        """
        data_dict = {}
        for k, v in row.items():
            if isinstance(v, int):
                data_dict[k] = "int(11)"
            elif isinstance(v, float):
                data_dict[k] = "varchar(45)"
            elif isinstance(v, list):
                data_dict[k] = "json"
            else:
                if len(v) < 255:
                    data_dict[k] = "varchar(255)"
                else:
                    data_dict[k] = "text"
            if k == "id":
                data_dict[k] = "varchar(45)"
        return data_dict
