"""
@author: liming.wang
@license:
@contact: wanglm.mickel@gmail.com
@software:
@file: sql_helper.py
@time: 2020/5/17 12:26
@desc:
"""

import pymysql
# from DBUtils.PooledDB import PooledDB
from dbutils.pooled_db import PooledDB
from threading import Lock
from config import setting 
# from config.setting import config
lock = Lock()


class SQLHelper(object):
    __pool = None

    # def __new__(cls, *args, **kwargs):
    #     if not cls.__pool:
    #         cls.__pool = super().__new__(cls, *args, **kwargs)
    #     return cls.__pool

    def __init__(self, mysqlhost, mysqlport, mysqluser, mysqlpassword, mysqldatabase, ):
        self.pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=0,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=0,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=0,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=0,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的
            # threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=False,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is
            # created, 4 = when a query is executed, 7 = always
            # host='117.80.87.15',  # rds6d7n2b4lk931zwp0r.mysql.rds.aliyuncs.com
            # host="rm-bp14y5n6x4a49993c.mysql.rds.aliyuncs.com",
            # port=3306,  # 3306 / 43060
            # user="igasv4_igc",  # igasv4
            # database='igasv4',
            # password="IgasV85517505Qyzn",  # igasV85540001
            # host="58.215.2.82",
            # port=11306,  # 3306 / 43060
            # user="root",  # igasv4
            # password='QyisTestDB123',
            # database='igasv4',
            # host=config["host"],
            # port=config["port"],
            # user=config["user"],
            # password=config["password"],
            # database=config["database"],
            
            host=mysqlhost,
            port=mysqlport,
            user=mysqluser,
            password=mysqlpassword,
            db=mysqldatabase,
            charset='utf8mb4'
        )

        # print("mysqlhost=[", setting.mysqlhost, "] [port=", setting.mysqlport,
        #     "] [user=", setting.mysqluser, "] [mysqlpassword=", setting.mysqlpassword,
        #     "] database=[", setting.mysqldatabase, "]")
        self.conn = None
        self.cursor = None

    def get_con(self):
        conn = self.pool.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        return conn, cursor

    def close(self, conn=None, cursor=None):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    def fetch_one(self, sql, args):
        cursor = None
        try:
            _, cursor = self.get_con()
            cursor.execute(sql, args)
            result = cursor.fetchone()
            return result
        except Exception as error:
            print("***fetch_one", error)
            return False
        finally:
            self.close(cursor=cursor)
            # return True

    def fetch_one_noparam(self, sql):
        cursor = None
        try:
            _, cursor = self.get_con()
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
        except Exception as error:
            print("***fetch_one", error)
            return False
        finally:
            self.close(cursor=cursor)
            # return True

    def fetch_all(self, sql, args):
        try:
            _, cursor = self.get_con()
            cursor.execute(sql, args)
            result = cursor.fetchall()
            return result
        except Exception as error:
            print("***fetch_all", error)
            return False
        finally:
            self.close(cursor=cursor)

    def fetch_all_noparam(self, sql):
        try:
            _, cursor = self.get_con()
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as error:
            print("***fetch_all", error)
            return False
        finally:
            self.close(cursor=cursor)

    def update(self, sql, args):
        conn, cursor = self.get_con()
        # self.cursor.execute(sql, args)
        try:
            cursor.execute(sql, args)
            conn.commit()
            return True
        except Exception as error:
            print("***update", error)
            # self.conn.rollback()
            return False
        finally:
            self.close(conn, cursor)

    def update_all(self, sql, args):
        conn, cursor = self.get_con()
        # self.cursor.execute(sql, args)
        try:
            cursor.executemany(sql, args)
            conn.commit()
            return True
        except Exception as error:
            print("***update_all", error)
            # self.conn.rollback()
            # self.close()
            return False
        finally:
            self.close(conn, cursor)


# sql_helper = SQLHelper(config=config[config["env"]]["db_config"]["ipwater"])
sql_helper = SQLHelper(setting.mysqlhost, setting.mysqlport, setting.mysqluser, setting.mysqlpassword,  setting.mysqldatabase)
# 
# db2_sql_helper = SQLHelper(setting.db2_mysqlhost, setting.db2_mysqlport, setting.db2_mysqluser, setting.db2_mysqlpassword,  setting.db2_mysqldatabase)

