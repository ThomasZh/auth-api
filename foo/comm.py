# coding=utf-8

import time
# from datetime import datetime
# from datetime import *
import datetime
import pytz
import random
import string
import os
import uuid
import hashlib
import re
import locale
import decimal
import jwt


class Singleton(object):
    __singleton = None;
    def __new__(cls):
        if cls.__singleton is None:
            cls.__singleton = object.__new__(cls);
        return cls.__singleton;

# currency
def splitUpper(str):
    arr = re.findall('[A-Z][a-z]*', str)
    return " ".join(arr)


# currency
def currency(num):
    # locale.setlocale( locale.LC_ALL, '' )
    # locale.setlocale( locale.LC_ALL, 'en_CA.UTF-8' )
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    return locale.currency(float(num), grouping=True )

# string
def generate_uuid_str():
    return str(uuid.uuid1()).replace('-', '')


# string
def generate_nonce_str(num):
    if not num:
        num = 6
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(num))


# number
def generate_nonce_number(num):
    return ''.join(random.choice(string.digits) for _ in range(num))


# string
def generate_random_str(num):
    return ''.join(random.choice(string.digits) for _ in range(num))


def generate_md5(fp):
    m = hashlib.md5()
    m.update(fp)
    return m.hexdigest()


def md5_pwd(pwd):
    b = pwd.encode("utf-8")
    md5pwd = hashlib.md5(b).hexdigest()
    return md5pwd


def hash_pwd(md5pwd, salt):
    md5salt = hashlib.md5(salt).hexdigest()
    ecrypted_pwd = hashlib.md5(md5pwd + md5salt).hexdigest()
    return ecrypted_pwd


# string
def hidden_phone(phone):
    try:
        phone = phone.strip()
        phone = phone.replace(" ","")
        lst = list(str(phone))
        lst[-5] = '*'
        lst[-6] = '*'
        lst[-7] = '*'
        lst[-8] = '*'
        phone = ''.join(lst)
        return phone
    except:
        return phone


# python直接在脚本中去执行cmd命令
def execute_cmd(cmd):
    handler = os.popen(cmd)   #此时打开的a是一个对象，如果直接打印的话是对象内存地址
    text = handler.read()     #要用read（）方法读取后才是文本对象
    handler.close()           #还需将对象关闭
    return text


# UTCS时间转换为时间戳 2016-07-31T16:00:00Z
# string => timestamp
def utc_to_local(utc_time_str, utc_format='%Y-%m-%d %H:%M:%S'):
    # local_tz = pytz.timezone('Asia/Chongqing')
    local_tz = pytz.timezone('US/Pacific')
    local_format = "%Y-%m-%d %H:%M"
    utc_dt = datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    return int(time.mktime(time.strptime(time_str, local_format)))


# 本地时间转换为UTC
# timestamp => string
def local_to_utc(local_ts, utc_format='%Y-%m-%d %H:%M:%S'):
    # local_tz = pytz.timezone('Asia/Chongqing')
    local_tz = pytz.timezone('US/Pacific')
    local_format = "%Y-%m-%d %H:%M"
    time_str = time.strftime(local_format, time.localtime(local_ts))
    dt = datetime.datetime.strptime(time_str, local_format)
    local_dt = local_tz.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt.strftime(utc_format)


# 本地时间转换为UTC
# timestamp => string
def local_to_date(local_ts, utc_format='%Y/%m/%d'):
    # local_tz = pytz.timezone('Asia/Chongqing')
    local_tz = pytz.timezone('US/Pacific')
    local_format = "%Y/%m/%d"
    time_str = time.strftime(local_format, time.localtime(local_ts))
    dt = datetime.datetime.strptime(time_str, local_format)
    local_dt = local_tz.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt.strftime(utc_format)


# UTC time
def current_timestamp():
    return int(time.time())
    # current_time = int(time.mktime(datetime.datetime.now().timetuple()))
    # return current_time


def current_datetime():
    return datetime.datetime.now()


def timestamp_to_datetime(t):
    _format = '%Y-%m-%d %H:%M:%S'
    # value is timestamp(int), eg: 1332888820
    _t = time.localtime(t)
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    _dt = time.strftime(_format, _t)
    return _dt


def timestamp_to_date(t):
    _format = '%Y/%m/%d'
    # value is timestamp(int), eg: 1332888820
    _t = time.localtime(t)
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    _dt = time.strftime(_format, _t)
    return _dt


# 把字符串转成datetime
def string_to_datetime(st, utc_format='%Y-%m-%d %H:%M:%S'):
    _dt = datetime.datetime.strptime(st, utc_format)
    return _dt


# 把datetime转成字符串
def datetime_to_string(dt, utc_format='%Y-%m-%d %H:%M:%S'):
    if isinstance(dt, str):
        return dt
    else:
        return dt.strftime(utc_format)


def datetime_string_us_to_iso(st):
    _dt = string_to_datetime(st, "%m/%d/%Y")
    return datetime_to_string(_dt)


def datetime_ios_to_us_string(dt, utc_format="%m/%d/%Y"):
    return datetime_to_string(dt, utc_format)


def date_duration(sd1, sd2, utc_format="%m/%d/%Y"):
    if not sd1:
        return 1
    if not sd2:
        return 0
    d1 = string_to_datetime(sd1, utc_format)
    d2 = string_to_datetime(sd2, utc_format)
    return (d1 - d2).days


# 把字符串转成timestamp(int)
def string_to_timestamp(s, utc_format="%Y-%m-%d %H:%M:%S"):
    _dt = time.strptime(s, utc_format)
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
    # "2012-03-28 06:53:40" to timestamp(int)
    _timestamp = time.mktime(_dt)
    return int(_timestamp)


# 把字符串转成timestamp(int)
def ios_string_to_timestamp(s, utc_format="%m/%d/%Y"):
    _dt = time.strptime(s, utc_format)
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
    # "2012-03-28 06:53:40" to timestamp(int)
    _timestamp = time.mktime(_dt)
    return int(_timestamp)


# %Y-%m-%dT%H:%M:%S.%fZ 2022-01-31T16:00:00.000Z
# %m/%d/%Y 02/14/2022
def timestamp_to_ios_str(t):
    year = t[0:4]
    month = t[5:7]
    day = t[8:10]
    return month + "/" + day + "/" + year


#  获取当前周的 周一及周日 时间
def get_current_week_days():
    monday = datetime.date.today()
    tuesday = datetime.date.today()
    wednesday = datetime.date.today()
    thursday = datetime.date.today()
    friday = datetime.date.today()
    saturday = datetime.date.today()
    sunday = datetime.date.today()

    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday += one_day
    while tuesday.weekday() != 1:
        tuesday += one_day
    while wednesday.weekday() != 2:
        wednesday += one_day
    while thursday.weekday() != 3:
        thursday += one_day
    while friday.weekday() != 4:
        friday += one_day
    while saturday.weekday() != 5:
        saturday += one_day
    while sunday.weekday() != 6:
        sunday += one_day
    # 返回当前的星期一和星期天的日期
    return monday, tuesday, wednesday, thursday, friday, saturday, sunday


#  获取当前周的 周一及周日 时间
def get_current_week():
    monday, sunday = datetime.date.today(), datetime.date.today()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day
    # 返回当前的星期一和星期天的日期
    return monday, sunday


#  获取上周的 周一及周日 时间
def get_prov_week():
    monday, sunday = datetime.date.today(), datetime.date.today()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day
    # 返回上周的星期一和星期天的日期
    for num in range(0,7):
        monday -= one_day
    for num in range(0,7):
        sunday -= one_day
    return monday, sunday


def validate_email(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0


def validate_phone(num):
    if len(num)==11 and num.isdigit() and num[0].isdigit():
        return True
    else:
        return False


# string
def name_to_uuid(name):
    if isinstance(name, str):
        b = name
    else:
        b = name.encode('utf-8')
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, b)).replace('-', '')


import numpy as np
import json as JSON # 启用别名，不会跟方法里的局部变量混淆

class MyEncoder(JSON.JSONEncoder):
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


def make_rs(rs):
    # return JSON.dumps(rs, ensure_ascii=False, cls=MyEncoder, indent=0)
    return JSON.dumps(rs , cls=MyEncoder)
    # return MyEncoder().default(rs)


def jwt_decode(secret_key, jwt_token):
    info = jwt.decode(jwt_token, secret_key, True, algorithm='HS256')
    return info


def jwt_encode(secret_key, payload):
    headers = {"alg": "HS256", "typ": "JWT"}
    jwt_token = jwt.encode(payload=payload, key=secret_key, algorithm='HS256', headers=headers).decode('utf-8')
    return jwt_token
