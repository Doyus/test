#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-07-17 21:06:43

import time
import mysql.connector
from pyspider.database.base.projectdb import ProjectDB as BaseProjectDB
from pyspider.database.basedb import BaseDB
from .mysqlbase import MySQLMixin


class ProjectDB(MySQLMixin, BaseProjectDB, BaseDB):
    __tablename__ = 'pyspider_project'

    def __init__(self, host='localhost', port=3306, database='projectdb',
                 user='root', passwd=None):
        self.database_name = database
        self.conn = mysql.connector.connect(user=user, password=passwd,
                                            host=host, port=port, autocommit=True)
        if database not in [x[0] for x in self._execute('show databases')]:
            self._execute('CREATE DATABASE %s' % self.escape(database))
        self.conn.database = database
        #
        # self._execute('''
        # CREATE TABLE `pyspider_project` (
        #   `name` varchar(64) NOT NULL,
        #   `group` varchar(64) DEFAULT NULL,
        #   `status` varchar(16) DEFAULT NULL,
        #   `script` text,
        #   `comments` varchar(1024) DEFAULT NULL,
        #   `rate` float(11,4) DEFAULT NULL,
        #   `burst` float(11,4) DEFAULT NULL,
        #   `updatetime` double(16,4) DEFAULT NULL,
        #   `username` varchar(64) DEFAULT 'super',
        #   `main_host` varchar(255) NOT NULL DEFAULT '',
        #   `class_name` varchar(255) DEFAULT NULL,
        #   `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
        #   `update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        #   PRIMARY KEY (`name`)
        # ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        # ''')

    def insert(self, name, obj={}):
        obj = dict(obj)
        obj['name'] = name
        obj['updatetime'] = time.time()
        return self._insert(**obj)

    def update(self, name, obj={}, **kwargs):
        obj = dict(obj)
        obj.update(kwargs)
        obj['updatetime'] = time.time()
        ret = self._update(where="`name` = %s" % self.placeholder, where_values=(name, ), **obj)
        return ret.rowcount

    def get_all(self, fields=None):
        return self._select2dic(what=fields)

    # 分页查询
    def get_page(self, page_num=1, page_size=10, fields=None,where="", where_values=[],order=None):
        '''
        查询products表中除了'apple'之外的所有水果的名称和价格，结果按价格升序排列。
        db._select2dic(tablename="products", what=["name", "price"], where="category = 'fruit' AND name != %s", where_values=["apple"], order="price A
        tablename=None, what="*", where="", where_values=[],
                    order=None, offset=0, limit=None
        '''
        offset = (page_num - 1) * page_size
        limit = page_size
        # where = "title LIKE %s AND create_time IS NOT NULL"
        # where_values = [title_like]
        # order = "create_time DESC"
        return self._select2dic(what=fields, offset=offset, limit=limit, where=where, where_values=where_values,
                    order=order)

    def get(self, name, fields=None):
        where = "`name` = %s" % self.placeholder
        for each in self._select2dic(what=fields, where=where, where_values=(name, )):
            return each
        return None

    def drop(self, name):
        where = "`name` = %s" % self.placeholder
        return self._delete(where=where, where_values=(name, ))

    def check_update(self, timestamp, fields=None):
        where = "`updatetime` >= %f" % timestamp
        return self._select2dic(what=fields, where=where)
