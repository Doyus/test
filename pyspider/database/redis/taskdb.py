#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<roy@binux.me>
#         http://binux.me
# Created on 2015-05-16 21:01:52

import six
import time
import json
import redis
import logging
import itertools

from pyspider.libs import utils
from pyspider.database.base.taskdb import TaskDB as BaseTaskDB


class TaskDB(BaseTaskDB):
    UPDATE_PROJECTS_TIME = 10 * 60
    __prefix__ = 'taskdb_'

    def __init__(self, host='localhost', port=6379, db=0, username=None, password=None):
        # print("task_redis", host, port, db, password)
        # 处理包含用户名和密码的情况
        if username and password:
            redis_url = f"redis://{username}:{password}@{host}:{port}/{db}"
            pool = redis.ConnectionPool.from_url(redis_url)
            self.redis = redis.StrictRedis(connection_pool=pool)
        else:
            self.redis = redis.StrictRedis(host=host, port=int(port), db=int(db), password=password)
        # print(self.redis)
        try:
            self.redis.scan(count=1)
            self.scan_available = True
        except Exception as e:
            logging.debug("redis_scan disabled: %r", e)
            self.scan_available = False

    def _gen_key(self, project, taskid):
        return "%s%s_%s" % (self.__prefix__, project, taskid)

    def _gen_status_key(self, project, status):
        return '%s%s_status_%d' % (self.__prefix__, project, status)

    def _parse(self, data):
        if six.PY3:
            result = {}
            for key, value in data.items():
                if isinstance(value, bytes):
                    value = utils.text(value)
                result[utils.text(key)] = value
            data = result

        for each in ('schedule', 'fetch', 'process', 'track'):
            if each in data:
                if data[each]:
                    data[each] = json.loads(data[each])
                else:
                    data[each] = {}
        if 'status' in data:
            try:
                data['status'] = int(data['status'])
            except Exception as e:
                logging.error(f'redis 判断状态错误:{e},{str(data)}',)

        if 'lastcrawltime' in data:
            data['lastcrawltime'] = float(data['lastcrawltime'] or 0)
        if 'updatetime' in data:
            data['updatetime'] = float(data['updatetime'] or 0)
        return data

    def _stringify(self, data):
        for each in ('schedule', 'fetch', 'process', 'track'):
            if each in data:
                data[each] = json.dumps(data[each])
        return data

    @property
    def projects(self):
        if time.time() - getattr(self, '_last_update_projects', 0) \
                > self.UPDATE_PROJECTS_TIME:
            self._projects = set(utils.text(x) for x in self.redis.smembers(
                self.__prefix__ + 'projects'))
        return self._projects

    def load_tasks(self, status, project=None, fields=None):
        if project is None:
            project = self.projects
        elif not isinstance(project, list):
            project = [project, ]

        if self.scan_available:
            scan_method = self.redis.sscan_iter
        else:
            scan_method = self.redis.smembers

        if fields:
            def get_method(key):
                obj = self.redis.hmget(key, fields)
                if all(x is None for x in obj):
                    return None
                return dict(zip(fields, obj))
        else:
            get_method = self.redis.hgetall

        for p in project:
            status_key = self._gen_status_key(p, status)
            for taskid in scan_method(status_key):
                obj = get_method(self._gen_key(p, utils.text(taskid)))
                if not obj:
                    #self.redis.srem(status_key, taskid)
                    continue
                else:
                    yield self._parse(obj)

    def get_task(self, project, taskid, fields=None):
        if fields:
            obj = self.redis.hmget(self._gen_key(project, taskid), fields)
            if all(x is None for x in obj):
                return None
            obj = dict(zip(fields, obj))
        else:
            obj = self.redis.hgetall(self._gen_key(project, taskid))

        if not obj:
            return None
        return self._parse(obj)

    def delete_keys_with_pattern(self, pattern):
        """
        删除 Redis 中包含指定关键词的键
        :param redis_client: Redis 客户端实例
        :param pattern: 关键词
        """
        keys = self.redis.keys(f'*{pattern}*')
        if keys:
            self.redis.delete(*keys)
            print(f'已删除 {len(keys)} 个键,包含关键词 "{pattern}"')
        else:
            print(f'未找到包含关键词 "{pattern}" 的键')

    def status_count(self, project):
        '''
        return a dict
        '''
        pipe = self.redis.pipeline(transaction=False)
        for status in range(1, 5):
            pipe.scard(self._gen_status_key(project, status))
        ret = pipe.execute()

        result = {}
        for status, count in enumerate(ret):
            if count > 0:
                result[status + 1] = count
        return result

    def insert(self, project, taskid, obj={}):
        obj = dict(obj)
        obj['taskid'] = taskid
        obj['project'] = project
        obj['updatetime'] = time.time()
        obj.setdefault('status', self.ACTIVE)

        task_key = self._gen_key(project, taskid)

        pipe = self.redis.pipeline(transaction=False)
        if project not in self.projects:
            pipe.sadd(self.__prefix__ + 'projects', project)
        # pipe.hmset(task_key, self._stringify(obj))
        # pipe.sadd(self._gen_status_key(project, obj['status']), taskid)
        # pipe.execute()
        pipe.hmset(task_key, self._stringify(obj))
        # 检查 task_key 是否包含特定字符串
        if not any(substr in task_key for substr in ['on_finished', 'on_start', '_projects', 'status_']):
            pipe.expire(task_key, 1292000)  # 设置过期时间为一个月 (2592000 秒)
        pipe.sadd(self._gen_status_key(project, obj['status']), taskid)
        if not any(substr in task_key for substr in ['on_finished', 'on_start', '_projects', 'status_']):
            pipe.expire(task_key, 1292000)  # 设置过期时间为一个月 (2592000 秒)
        pipe.execute()

    def update(self, project, taskid, obj={}, **kwargs):
        obj = dict(obj)
        obj.update(kwargs)
        obj['updatetime'] = time.time()

        pipe = self.redis.pipeline(transaction=False)
        pipe.hmset(self._gen_key(project, taskid), self._stringify(obj))
        if not any(substr in project for substr in ['on_finished', 'on_start', '_projects', 'status_']):
            pipe.expire(project, 1292000)  # 设置过期时间为一个月 (2592000 秒)
        if 'status' in obj:
            for status in range(1, 5):
                if status == obj['status']:
                    pipe.sadd(self._gen_status_key(project, status), taskid)
                    if not any(substr in project for substr in ['on_finished', 'on_start', '_projects', 'status_']):
                        pipe.expire(project, 1292000)  # 设置过期时间为一个月 (2592000 秒)
                else:
                    pipe.srem(self._gen_status_key(project, status), taskid)
        pipe.execute()

    def drop(self, project):
        self.redis.srem(self.__prefix__ + 'projects', project)

        if self.scan_available:
            scan_method = self.redis.scan_iter
        else:
            scan_method = self.redis.keys

        for each in itertools.tee(scan_method("%s%s_*" % (self.__prefix__, project)), 100):
            each = list(each)
            if each:
                self.redis.delete(*each)
