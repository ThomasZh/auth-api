#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2022 cyber-life.cn
# thomas@cyber-life.cn


import bcrypt


def generate_pwd(str):
    return bcrypt.hashpw(str.encode("utf-8"), bcrypt.gensalt(10)).decode("utf-8")


def compare_pwd(str, pwd):
    return bcrypt.hashpw(str.encode("utf-8"), pwd.encode("utf-8")) == pwd.encode("utf-8")


if __name__ == '__main__':
    data = "https://www.cyber-life.cn"
    password = generate_pwd(data)
    print(password)

    if compare_pwd(data, password):
        print("equle")
    else:
        print("not equle")
