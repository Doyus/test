#!/usr/bin/envutils
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-07-17 18:53:01


import re
import six
import time
import json
import mysql.connector

from pyspider.libs import utils
from pyspider.database.base.taskdb import TaskDB as BaseTaskDB
from pyspider.database.basedb import BaseDB
from .mysqlbase import MySQLMixin, SplitTableMixin


class TaskDB(MySQLMixin, SplitTableMixin, BaseTaskDB, BaseDB):
    __tablename__ = ''
    __mytaskname = 'pyspider_task'
    def __init__(self, host='localhost', port=3306, database='taskdb',
                 user='root', passwd=None):
        # self.database_name = database
        # self.conn = mysql.connector.connect(user=user, password=passwd,
        #                                     host=host, port=port, autocommit=True)
        # if database not in [x[0] for x in self._execute('show databases')]:
        #     self._execute('CREATE DATABASE %s' % self.escape(database))
        # self.conn.database = database
        # self._list_project()

        self.database_name = database
        self.conn = mysql.connector.connect(user=user, password=passwd, host=host, port=port, autocommit=True)
        if database not in [x[0] for x in self._execute('show databases')]:
            self._execute('CREATE DATABASE %s' % self.escape(database))
        self.conn.database = database
        self._list_project()

        # 检查表是否存在,不存在则创建
        tablename = self.__mytaskname
        table_list_name = [x[0] for x in self._execute('show tables')]
        # print(tablename,"table_list_name",table_list_name)
        if tablename not in table_list_name:
            self._create_project(tablename)


    def _create_project(self, project):
        assert re.match(r'^\w+$', project) is not None
        # 自定义表
        tablename = self.__mytaskname
        if tablename in [x[0] for x in self._execute('show tables')]:
            return
        self._execute('''
        CREATE TABLE %s (
          `taskid` varchar(64) NOT NULL,
          `project` varchar(64) NOT NULL,  -- 修改为 NOT NULL
          `url` varchar(1024) DEFAULT NULL,
          `status` int(1) DEFAULT NULL,
          `schedule` blob,
          `fetch` blob,
          `process` blob,
          `track` blob,
          `lastcrawltime` double(16,4) DEFAULT NULL,
          `updatetime` double(16,4) DEFAULT NULL,
          `createtime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
          PRIMARY KEY (`taskid`, `project`),  -- 联合主键设置在这里
          KEY `status_index` (`status`),
          KEY `project_index` (`project`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        ''' % self.escape(tablename))

    def _parse(self, data):
        for key, value in list(six.iteritems(data)):
            if isinstance(value, (bytearray, six.binary_type)):
                data[key] = utils.text(value)
        for each in ('schedule', 'fetch', 'process', 'track'):
            if each in data:
                if data[each]:
                    data[each] = json.loads(data[each])
                else:
                    data[each] = {}
        return data

    def _stringify(self, data):
        for each in ('schedule', 'fetch', 'process', 'track'):
            if each in data:
                data[each] = json.dumps(data[each])
        return data

    def load_tasks(self, status, project=None, fields=None):
        # print("\n正在载入任务taskdb11111",project, status, fields, "\n")
        if project and project not in self.projects:
            return
        where = "`status` = %s AND `project` = %s" % (self.placeholder, self.placeholder)
        if fields:
            what = ','.join(self.escape(f) for f in fields)
        else:
            what = '*'
        values = [status, project] if project else [status]
        for data in self._select2dic(self.__mytaskname, what=what, where=where, where_values=values):
            res = self._parse(data)
            # print("载入任务2222", project, status, res, "\n")
            yield res

    def get_task(self, project, taskid, fields=None):
        # print("\n正在获取任务taskdb11111",project, taskid,fields, "\n")
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return None

        where = "`taskid` = %s AND `project` = %s" % (self.placeholder, self.placeholder)
        if fields:
            what = ','.join(self.escape(f) for f in fields)
        else:
            what = '*'
        for data in self._select2dic(self.__mytaskname, what=what, where=where, where_values=(taskid, project)):
            return self._parse(data)
        return None

    def status_count(self, project):
        result = dict()
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return result

        tablename = self.__mytaskname
        where = "`project` = %s" % self.placeholder
        for status, count in self._execute("SELECT `status`, count(1) FROM %s WHERE %s GROUP BY `status`" %
                                           (self.escape(tablename), where), (project,)):
            result[status] = count
        return result

    def insert(self, project, taskid, obj={}):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            self._create_project(project)
            self._list_project()
        obj = dict(obj)
        obj['taskid'] = taskid
        obj['project'] = project
        obj['updatetime'] = time.time()
        tablename = self.__mytaskname
        # print("\n正在插入调度库taskdb11111", obj, tablename,"\n")
        # if "on_start" in obj['taskid']:
        #     obj['taskid'] = obj['project'] + obj['taskid']
        # if "on_finished" in obj['taskid']:
        #     obj['taskid'] = obj['project'] + obj['taskid']
        str_data = self._stringify(obj)
        return self._insert(tablename, **str_data)

    def update(self, project, taskid, obj={}, **kwargs):
        # print("\n正在进行任务更新taskdb11111",project, taskid, obj, kwargs, "\n")
        where = "`taskid` = %s AND `project` = %s" % (self.placeholder, self.placeholder)
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            raise LookupError
        # tablename = self._tablename(project)
        tablename = self.__mytaskname
        obj = dict(obj)
        obj.update(kwargs)
        obj['updatetime'] = time.time()
        return self._update(
            tablename,
            where=where,
            where_values=(taskid, project),
            **self._stringify(obj)
        )
