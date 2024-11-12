#!/usr/bin/env python
# _*_ coding: utf-8_*_
#
# Copyright 2023 cyber-life.cn
# thomas@cyber-life.cn
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "./"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
import logging
import pymysql
from mysql_pool import pool


class MysqlUtil():
    """
    @summary: 执行查询，并取出所有结果集
    @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    @param param: 可选参数，条件列表值（元组/列表）
    @param cursorclass: 可选参数(tuple|dict),
                        tuple: cursor 对象返回的结果集类型为默认的元组，
                        dict: 使用 pymysql.cursors.DictCursor 类指定字典数组为结果集类型。
    @return: result list(字典对象)/boolean 查询到的结果集
    """
    def query_all(self, sql, param=None, cursorclass="dict"):
        # 从连接池中获取一个连接
        conn = pool.connection()
        if cursorclass == "tuple":
            cursor = conn.cursor()
        elif cursorclass == "dict":
            cursor = conn.cursor(pymysql.cursors.DictCursor)

        try:
            if param is None:
                rowcount = cursor.execute(sql)
            else:
                rowcount = cursor.execute(sql, param)
            if rowcount>0:
                return cursor.fetchall()
            else:
                if cursorclass == "tuple":
                    return ()
                elif cursorclass == "dict":
                    return []
        except BaseException as e:
            logging.error('数据库查询错误: %r', str(e))
        finally:
            cursor.close()
            # 将连接归还到连接池中，以便让其他程序使用它。
            conn.close()


    """
    @summary: 执行查询，并取出第一条
    @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    @param param: 可选参数，条件列表值（元组/列表）
    @param cursorclass: 可选参数(tuple|dict),
                        tuple: cursor 对象返回的结果集类型为默认的元组，
                        dict: 使用 pymysql.cursors.DictCursor 类指定字典数组为结果集类型。
    @return: result list/boolean 查询到的结果集
    """
    def query_one(self, sql, param=None, cursorclass="dict"):
        # 从连接池中获取一个连接
        conn = pool.connection()
        if cursorclass == "tuple":
            cursor = conn.cursor()
        elif cursorclass == "dict":
            cursor = conn.cursor(pymysql.cursors.DictCursor)

        try:
            if param is None:
                rowcount = cursor.execute(sql)
            else:
                rowcount = cursor.execute(sql, param)
            if rowcount>0:
                return cursor.fetchone()
            else:
                return None
        except BaseException as e:
            logging.error('数据库查询错误: %r', str(e))
        finally:
            cursor.close()
            # 将连接归还到连接池中，以便让其他程序使用它。
            conn.close()


    """
    @summary: 向数据表插入一条记录
    @param sql:要插入的ＳＱＬ格式
    @param value:要插入的记录数据tuple/list
    @return: insertId 插入行的ID
    """
    def insert_one(self, sql, param):
        # 从连接池中获取一个连接
        conn = pool.connection()
        cursor = conn.cursor()
        try:
            rowcount = cursor.execute(sql, param)
            conn.commit()
        except Exception as e:
            conn.rollback()
            logging.error('数据库插入错误: %r', str(e))
        finally:
            cursor.close()
            # 将连接归还到连接池中，以便让其他程序使用它。
            conn.close()


    """
    @summary: 向数据表插入mutiply条记录
    @param sql:要插入的ＳＱＬ格式
    @param value:要插入的记录数据tuple/list
    @return: insertId 插入行的ID
    """
    def insert_batch(self, sql, datas):
        # 从连接池中获取一个连接
        conn = pool.connection()
        cursor = conn.cursor()
        for data in datas:
            try:
                rowcount = cursor.execute(sql, data)
                conn.commit()
            except Exception as e:
                conn.rollback()
                # logging.error('数据库插入错误: %r', str(e))

        cursor.close()
        # 将连接归还到连接池中，以便让其他程序使用它。
        conn.close()


    """
    @summary: 向数据表插入多条记录
    @param sql:要插入的ＳＱＬ格式
    @param values:要插入的记录数据tuple(tuple)/list[list]
    @return: rowcount 受影响的行数
    """
    def insert_many(self, sql, values):
        # 从连接池中获取一个连接
        conn = pool.connection()
        cursor = conn.cursor()
        try:
            rowcount = cursor.executemany(sql, values)
            conn.commit()
            return rowcount
        except Exception as e:
            logging.error('数据库插入错误: %r', str(e))
            conn.rollback()
            return 0
        finally:
            cursor.close()
            # 将连接归还到连接池中，以便让其他程序使用它。
            conn.close()


    """
    @summary: 更新数据表记录
    @param sql: ＳＱＬ格式及条件，使用(%s,%s)
    @param param: 要更新的  值 tuple/list
    @return: rowcount 受影响的行数
    """
    def update(self, sql, param=None):
        # 从连接池中获取一个连接
        conn = pool.connection()
        cursor = conn.cursor()
        try:
            if param is None:
                rowcount = cursor.execute(sql)
            else:
                rowcount = cursor.execute(sql, param)
            conn.commit()
            return rowcount
        except Exception as e:
            logging.error('数据库修改错误: %r', str(e))
            conn.rollback()
            return 0
        finally:
            cursor.close()
            # 将连接归还到连接池中，以便让其他程序使用它。
            conn.close()


    """
    @summary: 删除数据表记录
    @param sql: ＳＱＬ格式及条件，使用(%s,%s)
    @param param: 要删除的条件 值 tuple/list
    @return: rowcount 受影响的行数
    """
    def delete(self, sql, param=None):
        # 从连接池中获取一个连接
        conn = pool.connection()
        cursor = conn.cursor()
        try:
            if param is None:
                rowcount = cursor.execute(sql)
            else:
                rowcount = cursor.execute(sql, param)
            conn.commit()
            return rowcount
        except Exception as e:
            logging.error('数据库删除错误: %r', str(e))
            conn.rollback()
            return 0
        finally:
            cursor.close()
            # 将连接归还到连接池中，以便让其他程序使用它。
            conn.close()


    """
    @summary: 删除数据表记录
    @param sql: ＳＱＬ格式及条件，使用(%s,%s)
    @param param: 要删除的条件 值 tuple/list
    @return: rowcount 受影响的行数
    """
    def delete_batch(self, sql, datas):
        # 从连接池中获取一个连接
        conn = pool.connection()
        try:
            with conn.cursor() as cursor:
                # 关闭二进制日志
                cursor.execute('SET sql_log_bin = 0;')
                for data in datas:
                    rowcount = cursor.execute(sql, data)
                # 重新设置二进制日志记录
                cursor.execute('SET sql_log_bin = 1;')
            conn.commit()
        finally:
            # 将连接归还到连接池中，以便让其他程序使用它。
            conn.close()


    def query_pagination(self, sql, param=None, idx=0, limit=20, cursorclass="dict"):
        sql = sql + " LIMIT %s,%s"
        param = param + (idx, limit)
        logging.debug(sql, *param)
        return self.query_all(sql=sql, param=param, cursorclass=cursorclass)


    def count_pagination(self, sql, param=None):
        logging.debug(sql, *param)
        data = self.query_one(sql, param)
        if data and "count" in data:
            return int(data['count'])
        else:
            return 0


    """
    @summary: 执行查询，并取出所有结果集
    @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    @param param: 可选参数，条件列表值（元组/列表）
    @return: result list(字典对象)/boolean 查询到的结果集
    """
    def query_columns(self, table_name):
        # 从连接池中获取一个连接
        conn = pool.connection()
        cursor = conn.cursor()
        try:
            sql = "SELECT * FROM `" + table_name + "`"
            # 执行查询语句
            cursor.execute(sql)
            # 获取列名列表
            column_names = [i[0] for i in cursor.description]
            return column_names
        except BaseException as e:
            logging.error('数据库查询错误: %r', str(e))
        finally:
            cursor.close()
            # 将连接归还到连接池中，以便让其他程序使用它。
            conn.close()


    """
    @summary: 执行查询，并取出所有结果集
    @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    @param param: 可选参数，条件列表值（元组/列表）
    @return: result list(字典对象)/boolean 查询到的结果集
    """
    def query_primary_columns(self, table_name):
        # 从连接池中获取一个连接
        conn = pool.connection()
        cursor = conn.cursor()
        try:
            sql = "SHOW INDEX FROM `" + table_name + "` WHERE `Key_name`='PRIMARY'"
            # 执行查询语句
            rowcount = cursor.execute(sql)
            if rowcount>0:
                # return cursor.fetchall()
                # 获取列名列表
                column_names = [i[4] for i in cursor.fetchall()]
                return column_names
            else:
                return []
        except BaseException as e:
            logging.error('数据库查询错误: %r', str(e))
        finally:
            cursor.close()
            # 将连接归还到连接池中，以便让其他程序使用它。
            conn.close()


    """
    @summary: 执行查询，并取出所有结果集
    @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
    @param param: 可选参数，条件列表值（元组/列表）
    @return: result list(字典对象)/boolean 查询到的结果集
    """
    def query_columns_info(self, table_name):
        # 从连接池中获取一个连接
        conn = pool.connection()
        cursor = conn.cursor()
        try:
            sql = "SHOW FULL COLUMNS FROM `" + table_name + "` "
            # 执行查询语句
            rowcount = cursor.execute(sql)
            if rowcount>0:
                # return cursor.fetchall()
                # 获取列名列表
                column_names = [i for i in cursor.fetchall()]
                return column_names
            else:
                return []
        except BaseException as e:
            logging.error('数据库查询错误: %r', str(e))
        finally:
            cursor.close()
            # 将连接归还到连接池中，以便让其他程序使用它。
            conn.close()


    def trans_begin(self, cursorclass="dict"):
        """
        @summary: 开启事务
        """
        # 从连接池中获取一个连接
        conn = pool.connection()
        if cursorclass == "tuple":
            cursor = conn.cursor()
        elif cursorclass == "dict":
            cursor = conn.cursor(pymysql.cursors.DictCursor)
        return conn,cursor


    def trans_end(self, conn, cursor, option='commit'):
        """
        @summary: 结束事务
        """
        conn.commit()


    def trans_dispose(self, conn, cursor):
        """
        @summary: 释放连接池资源
        """
        cursor.close()
        # 将连接归还到连接池中，以便让其他程序使用它。
        conn.close()


    def trans_close_binlog(self, conn, cursor):
        """
        @summary: 关闭二进制日志
        """
        cursor.execute('SET sql_log_bin = 0;')


    def trans_open_binlog(self, conn, cursor):
        """
        @summary: 重新设置二进制日志记录
        """
        cursor.execute('SET sql_log_bin = 1;')


    def trans_delete(self, conn, cursor, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: rowcount 受影响的行数
        """
        try:
            if param is None:
                rowcount = cursor.execute(sql)
            else:
                rowcount = cursor.execute(sql,param)
            return rowcount
        except Exception as e:
            logging.error('数据库删除错误: %r', str(e))
            return 0


    def trans_insert_one(self, conn, cursor, sql, value):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: rowcount 受影响的行数
        """
        try:
            return cursor.execute(sql,value)
        except Exception as e:
            # logging.error('数据库插入错误: %r', str(e))
            return 0


    """
    @summary: 向数据表插入多条记录
    @param sql:要插入的ＳＱＬ格式
    @param values:要插入的记录数据tuple(tuple)/list[list]
    @return: rowcount 受影响的行数
    """
    def trans_insert_many(self, conn, cursor, sql, values):
        try:
            return cursor.executemany(sql, values)
        except Exception as e:
            logging.error('数据库插入错误: %r', str(e))
            return 0


    def trans_update(self, conn, cursor, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: rowcount 受影响的行数
        """
        try:
            if param is None:
                rowcount = cursor.execute(sql)
            else:
                rowcount = cursor.execute(sql,param)
            return rowcount
        except Exception as e:
            logging.error('数据库修改错误: %r', str(e))
            return 0


    def trans_query_one(self, conn, cursor, sql, param=None, cursorclass="dict"):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            rowcount = cursor.execute(sql)
        else:
            rowcount = cursor.execute(sql,param)
        if rowcount>0:
            return cursor.fetchone()
        else:
            return None


    def trans_query_all(self, conn, cursor, sql, param=None, cursorclass="dict"):
        if cursorclass == "tuple":
            cursor = conn.cursor()
        elif cursorclass == "dict":
            cursor = conn.cursor(pymysql.cursors.DictCursor)

        try:
            if param is None:
                rowcount = cursor.execute(sql)
            else:
                rowcount = cursor.execute(sql, param)
            if rowcount>0:
                return cursor.fetchall()
            else:
                if cursorclass == "tuple":
                    return ()
                elif cursorclass == "dict":
                    return []
        except BaseException as e:
            logging.error('数据库查询错误: %r', str(e))
            if cursorclass == "tuple":
                return ()
            elif cursorclass == "dict":
                return []


if __name__ == '__main__':
    column_names = MysqlUtil().query_columns("industry_code")
    print(column_names)

    sql = "SELECT * FROM vaccine.527temp"
    results = MysqlUtil().query_all(sql, param=None, cursorclass="tuple")
    print(results)
