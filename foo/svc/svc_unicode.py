#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2023 cyber-life.cn
# thomas@cyber-life.cn


import os
import sys
import logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))

unicode_text = r"\u65e0\u6548\u81ea\u5b9a\u4e49\u51fd\u6570"
text = bytes(unicode_text, 'utf-8').decode('unicode_escape')
print(text)

unicode_text = r"\u5f53\u524d\u533a\u57df\u4e0d\u80fd\u548c\u5df2\u5b58\u5728\u7684\u533a\u57df\u76f8\u4ea4\u3002"
text = bytes(unicode_text, 'utf-8').decode('unicode_escape')
print(text)

unicode_text = r"\u4f60\u9700\u8981\u4e00\u4e2a\u5b8c\u5168\u652f\u6301HTML5 Canvas\u7684\u6d4f\u89c8\u5668\u6765\u8fd0\u884cSpreadJS"
text = bytes(unicode_text, 'utf-8').decode('unicode_escape')
print(text)

# 中文转Unicode编码
text = "未找到授权信息"
res = text.encode("unicode_escape")
# 输出结果
# \u672a\u627e\u5230\u6388\u6743\u4fe1\u606f
print(res)
