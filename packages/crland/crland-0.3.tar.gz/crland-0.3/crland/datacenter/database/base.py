#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.types import NVARCHAR, Float, Integer
import pymysql.cursors

from crland.config import Config
from crland.datacenter.database import EMPTY_DATA, EMPTY_NUM

_bound_num = 10000

class Database:
    """ Python连接到 MySQL 数据库及相关操作 """
    
    connected = False
    __conn = None
    engine = None

    # 构造函数，初始化时直接连接数据库
    def __init__(self, conf):
        if type(conf) is not dict:
            print('错误: 参数不是字典类型！')
        else:
            for key in ['host', 'port', 'user', 'pw', 'db']:
                if key not in conf.keys():
                    print('错误: 参数字典缺少 %s' % key)
            if 'charset' not in conf.keys():
                conf['charset'] = 'utf8'
        try:
            self.__conn = pymysql.connect(
                host=conf['host'],
                port=conf['port'],
                user=conf['user'],
                passwd=conf['pw'],
                db=conf['db'],
                charset=conf['charset'],
                cursorclass=pymysql.cursors.DictCursor)
            self.connected = True
            self.engine = create_engine(
                'mysql+pymysql://%(user)s:%(pw)s@%(host)s:%(port)d/%(db)s?charset=utf8' % conf
            )         
        except pymysql.Error as e:
            print('数据库连接失败:', end='')

    def create_table(self, table, contents):
        try:
            #使用execute()方法执行sql，如果表存在则删除
            with self.__conn.cursor() as cursor:             
                cursor.execute('drop table if EXISTS ' + table)
            #创建表的sql
                if isinstance(contents, dict):
                    new_contents = ""
                    for k, v in contents.items():
                        new_contents += k + " " + v + ","
                    contents = new_contents[:-1] #delete last ","
                sql = '''
                    create table ''' + table + '''(
                    ''' + contents + '''
                    )
                '''
                print(sql)
                cursor.execute(sql)
        except pymysql.Error as e:
            self.__conn.rollback()
            return False

    def add_column_to_table(self, table, contents):
        try:
            with self.__conn.cursor() as cursor:
                if isinstance(contents, dict):
                    new_contents = ""
                    for k, v in contents.items():
                        new_contents += k + " " + v + ","
                    contents = new_contents[:-1] #delete last ","
                sql = '''ALTER TABLE ''' + table + ''' ADD ''' + contents
                print(sql)
                cursor.execute(sql)
        except pymysql.Error as e:
            self.__conn.rollback()
            return False

    # 插入数据到数据表
    def insert(self, table, val_obj):
        sql_top = 'INSERT INTO ' + table + ' ('
        sql_tail = ') VALUES ('
        try:
            for key, val in val_obj.items():
                sql_top += key + ','
                if isinstance(val, str):
                    val = "\"" + val + "\"" 
                sql_tail += val + ','
            sql = sql_top[:-1] + sql_tail[:-1] + ')'
            #print(sql)
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return self.__conn.insert_id()
        except pymysql.Error as e:
            self.__conn.rollback()
            return False

    # 插入数据到数据表
    def execute(self, sql):
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return True
        except pymysql.Error as e:
            self.__conn.rollback()
            return False

    # 更新数据到数据表
    def update(self, table, val_obj, range_str):
        sql = 'UPDATE ' + table + ' SET '
        try:
            for key, val in val_obj.items():
                sql += key + '=' + val + ','
            sql = sql[:-1] + ' WHERE ' + range_str
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.rowcount
        except pymysql.Error as e:
            self.__conn.rollback()
            return False

    # 删除数据在数据表中
    def delete(self, table, range_str):
        sql = 'DELETE FROM ' + table + ' WHERE ' + range_str
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.rowcount
        except pymysql.Error as e:
            self.__conn.rollback()
            return False

    # 查询唯一数据在数据表中
    def select_one(self, table, factor_str, field='*'):
        sql = 'SELECT ' + field + ' FROM ' + table + ' WHERE ' + factor_str
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.fetchall()[0]
        except pymysql.Error as e:
            return False

    # 查询多条数据在数据表中
    def select_more(self, table, range_str, field='*'):
        sql = 'SELECT ' + field + ' FROM ' + table + ' WHERE ' + range_str
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.fetchall()
        except pymysql.Error as e:
            return False

    # 查询条件筛选查询
    def select_by_order(self, table, order_column, limit_num=4, field='*'):
        inner_sql = 'SELECT ' + field + ' FROM ' + table + \
                    ' order by ' + order_column + ' desc limit ' + str(limit_num)
        sql = "SELECT * from (" + inner_sql + ")t order by " + order_column
        #print(sql)
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.fetchall()
        except pymysql.Error as e:
            print(e)
            return False

    # 直接执行
    def exec(self, sql):
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.fetchall()
        except pymysql.Error as e:
            print(e)
            return False

    # 统计某表某条件下的总行数
    def count(self, table, range_str='1'):
        sql = 'SELECT count(*)res FROM ' + table + ' WHERE ' + range_str
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.fetchall()[0]['res']
        except pymysql.Error as e:
            return False

    # 统计某字段（或字段计算公式）的合计值
    def sum(self, table, field, range_str='1'):
        sql = 'SELECT SUM(' + field + ') AS res FROM ' + table + ' WHERE ' + range_str
        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
            self.__conn.commit()
            return cursor.fetchall()[0]['res']
        except pymysql.Error as e:
            return False

    # 销毁对象时关闭数据库连接
    def __del__(self):
        try:
            self.__conn.close()
        except pymysql.Error as e:
            pass

    # 关闭数据库连接
    def close(self):
        self.__del__()


    def insert_data_by_pandas(
        self, 
        dataframe, 
        table_name, 
        dtypes={}, 
        if_exists='append', 
        single=False
    ):
        '''
        通过dataframe 向 sql 中插入表，此方法缺点是若表已存在，不能替换表中部分重复数据，只能替换/追加整张表
        :param dataframe: pd.Dataframe类型
        :param table_name: 插入的表名
        :param if_exists: {'fail', 'replace', 'append'}, default 'fail'
            - fail: If table exists, do nothing.
            - replace: If table exists, drop it, recreate it, and insert data.
            - append: If table exists, insert data. Create if does not exist.
        :return:
        '''

        def create_upsert_method(primary_key_column):
            def method(table, conn, keys, data_iter):
                # Create the INSERT statement with named placeholders
                insert = f"INSERT INTO {table.name} ({','.join(keys)})"
                try:
                    for d in data_iter:
                        values = " VALUES("
                        update = " ON DUPLICATE KEY UPDATE "                        
                        for i, name in enumerate(keys):
                            new_val = "NULL,"
                            if d[i]:
                                new_val = "'" + str(d[i]) + "',"
                            values += new_val
                            if name not in primary_key_column:
                                update += name + "=" + new_val
                        
                        values = values[:-1] + ")"
                        sql = insert + values + update[:-1]
                        conn.execute(text(sql))
                except Exception as e:
                    print("An error occurred:", str(e))
            return method

        if single:
            for i in range(len(dataframe)):
                try:
                    dataframe.iloc[i:i+1].to_sql(
                        table_name, 
                        self.engine, 
                        if_exists=if_exists, 
                        index=False, 
                        chunksize=100,
                        dtype = dtypes,
                        method = create_upsert_method(list(dtypes.keys()))
                    )
                except:
                    print("e")
                    pass
        else:
            try:
                dataframe.to_sql(
                    table_name, 
                    self.engine, 
                    if_exists=if_exists, 
                    index=False, 
                    chunksize=100,
                    dtype = dtypes,
                    method = create_upsert_method(list(dtypes.keys()))                    
                )
            except:
                pass 

    # 查询多条数据在数据表中
    def get_data_and_manuel_summary(
        self, 
        table, 
        order_str, 
        limit_num=3, 
        columns_to_names = None, 
        with_chart=False
    ):
        fields = ""
        if columns_to_names is None:
            fields = "*"
        else:
            fields = ", ".join(k for k, v in columns_to_names.items())
        # order name not in show
        if order_str not in fields:
            fields += ", " + order_str
        data = self.select_by_order(
            table = table, 
            order_column = order_str,
            limit_num=limit_num,            
            field = fields
            )
        #print(data, columns_to_names)
        idx = 0         
        for line in data[-3:]:
            for k, v in line.items():
                if k in columns_to_names:
                    if 0 == idx:
                        columns_to_names[k] = columns_to_names[k] + " in temporal order:"
                    try:
                        if abs(v) > _bound_num:
                            columns_to_names[k] += "{:.1e}".format(v) + ", " # to short it number                            
                        else:
                            columns_to_names[k] += str(round(float(v), 1)) + ", " # to short it number
                    except:
                        columns_to_names[k] += str(v) + ", "
            idx += 1
        result = ""
        if fields == "*":
            result = " \n".join("The " + k + " : " + v for k, v in columns_to_names.items())
            # error here, to improve later
        else:
            result = " \n".join(v[:-2] for k, v in columns_to_names.items())
        if with_chart:
            return {
                "result": result,
                "chart": data
            }
        else:
            return result

    # 直接执行sql查询多条数据在数据表中
    def exec_by_modelformat(
        self, 
        sql, 
        columns_to_names
    ):
        data = self.exec(sql)
        if not data:
            return EMPTY_DATA
        # print(data, columns_to_names)
        hit_columns = dict()
        idx = 0         
        for line in data:
            for k, v in line.items():
                if k in columns_to_names:
                    if 0 == idx:
                        hit_columns[k] = "Progressive " + columns_to_names[k] + ":"
                    try:
                        if abs(v) > _bound_num:
                            hit_columns[k] += "{:.1e}".format(v) + ", " # to short it number                            
                        else:
                            hit_columns[k] += str(round(float(v), 1)) + ", " # to short it number
                    except:
                        hit_columns[k] += str(v) + ", "
            idx += 1
        result = " \n".join(v[:-2] for k, v in hit_columns.items())
        return result