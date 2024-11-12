#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2022 cyber-life.cn
# thomas@cyber-life.cn

import hashlib

"""
MD5 Message-Digest Algorithm，一种被广泛使用的密码散列函数，可以产生出一个128位(16字节)的散列值(hash value)，
用于确保信息传输完整一致。MD5是最常见的摘要算法，速度很快，生成结果是固定的128 bit字节，通常用一个32位的16进制字符串表示。
update() 方法内传参为二进制数据  所以需要将字符串数据 encode()
作用：加密用户密码；保证数据唯一性（MD5可以保证唯一性）;比较文件是否被篡改等
"""


def generate_md5(str):
    hash_md5 = hashlib.md5()
    hash_md5.update(str.encode("utf-8"))
    return hash_md5.hexdigest()


def hash_pwd(md5pwd, salt):
    md5salt = generate_md5(salt)
    ecrypted_pwd = generate_md5(md5pwd + md5salt)
    return ecrypted_pwd


"""
SHA1的全称是Secure Hash Algorithm(安全哈希算法) 。SHA1基于MD5，加密后的数据长度更长，
它对长度小于264的输入，产生长度为160bit的散列值。比MD5多32位,因此，比MD5更加安全，但SHA1的运算速度就比MD5要慢
"""
def generate_sha1(str):
    hash_sha1 = hashlib.sha1()
    hash_sha1.update(str.encode("utf-8"))
    return hash_sha1.hexdigest()


if __name__ == '__main__':
    data = "https://www.cyber-life.cn"
    md5pwd = generate_md5(data)
    print(md5pwd)

    hashpwd = hash_pwd(md5pwd, "123456")
    print(hashpwd)

    sha1 = generate_sha1(data)
    print(sha1)
