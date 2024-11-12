#!/usr/bin/env python
# _*_ coding: utf-8_*_
import datetime
import numpy as np
import json as JSON # 启用别名，不会跟方法里的局部变量混淆
from collections import OrderedDict
# from .cy_string import *
import decimal


class CyJson:
    def dumps(dict_obj, ordered=False):
        if ordered:
            json_str = JSON.dumps(dict_obj, cls=CyEncoder, sort_keys=False)
            print(json_str)
            return json_str
        else:
            return JSON.dumps(dict_obj, cls=CyEncoder)
            # return JSON.dumps(dict_obj, ensure_ascii=False, cls=CyEncoder, indent=2)

    def loads(json_str, defaulttype=dict, escape=False, ordered=False):
        """
        返回安全的json类型
        :param json_str: 要被loads的字符串
        :param defaulttype: 若load失败希望得到的对象类型
        :param escape: 是否将单引号变成双引号
        :return:
        """
        if not json_str:
            return defaulttype()

        if isinstance(json_str, bytes):
            json_str = json_str.decode("utf-8")
        if escape:
            json_str = replace_quote(json_str)
        if ordered:
            return JSON.loads(json_str, object_pairs_hook=OrderedDict)
        else:
            return JSON.loads(json_str)


class CyEncoder(JSON.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8');
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, decimal.Decimal):
            return obj.to_eng_string()
            # return float(obj)
            # return str(obj.quantize(decimal.Decimal('0.00000000')))
        else:
            print(type(obj))

        return JSON.JSONEncoder.default(self, obj)


def remove_quote(s):
    # return s.replace('"', '')
    return ''.join(c for c in s if c not in '"')


def replace_quote(s):
    return s.replace("'", '"')
