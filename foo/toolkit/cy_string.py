#!/usr/bin/env python
# _*_ coding: utf-8_*_
import string

def erase_all_whitespace(s: str) -> str:
    for c in string.whitespace:
        s = s.replace(c, '')
    return s
