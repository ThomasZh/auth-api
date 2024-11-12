#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2022 cyber-life.cn
# thomas@cyber-life.cn


import base64


def bytes_to_base64(input_bytes):     # base64加密
    output_bytes = base64.b64encode(input_bytes)
    return output_bytes.decode('utf-8') # bytes转回str


def str_to_base64(input_str):
	return bytes_to_base64(input_str.encode('utf-8')) # 先将str转成bytes


def base64_to_str(input_str):     # base64解密
    input_bytes = input_str.encode('utf-8')
    output_bytes = base64.b64decode(input_bytes)
    # output_str = output_bytes.decode("utf-8")
    return output_bytes


if __name__ == '__main__':
    data = "https://www.cyber-life.cn"
    base64_str = str_to_base64(data)
    print(base64_str)

    _str = base64_to_str(base64_str)
    print(_str)
