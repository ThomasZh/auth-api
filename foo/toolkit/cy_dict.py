#!/usr/bin/env python
# _*_ coding: utf-8_*_

class CyDict:
    def replace_values(original_dict, replacement_dict):
        """
        字典替换值
        :原始字典:
            original_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
        :替换字典:
            replacement_dict = {'key2': 'new_value2', 'key3': 'new_value3'}
        :输出结果将是:
            {'key1': 'value1', 'key2': 'new_value2', 'key3': 'new_value3'}。
        """
        # 使用字典推导式和update()方法进行值替换
        updated_dict = {k: replacement_dict.get(k, v) for k, v in original_dict.items()}
        return updated_dict

    def list_to_dict(arr):
        """
        [{'param': 'a', 'value': '1'},
        {'param': 'b', 'value': ''},
        {'param': 'S1', 'value': 'AND student_id in ({a})'},
        {'param': 'S2', 'value': 'AND student_id = {b}'}]
        """
        dict = {}
        for item in arr:
            if "param" in item and "value" in item and item['param']:
                k = item['param']
                v = item['value']
                dict[k] = v
        return dict
