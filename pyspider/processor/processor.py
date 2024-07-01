#!/usr/b#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# 作者: Binux<i@binux.me>
#         http://binux.me
# 创建于: 2014-02-16 22:59:56

import sys
import six
import time
import logging
import traceback

# 导入日志记录器
logger = logging.getLogger("processor")

from six.moves import queue as Queue
from pyspider.libs import utils
from pyspider.libs.log import LogFormatter
from pyspider.libs.utils import pretty_unicode, hide_me
from pyspider.libs.response import rebuild_response
from .project_module import ProjectManager, ProjectFinder


class ProcessorResult(object):
    """
    回调函数产生的结果和日志
    """

    def __init__(self, result=None, follows=(), messages=(),
                 logs=(), exception=None, extinfo=None, save=None):
        # 如果extinfo为None,则设置为空字典
        if extinfo is None:
            extinfo = {}
        self.result = result
        self.follows = follows
        self.messages = messages
        self.logs = logs
        self.exception = exception
        self.extinfo = extinfo
        self.save = save

    def rethrow(self):
        """重新抛出异常"""

        if self.exception:
            raise self.exception

    def logstr(self):
        """将日志记录格式化为字符串"""

        result = []
        formater = LogFormatter(color=False)
        for record in self.logs:
            if isinstance(record, six.string_types):
                result.append(pretty_unicode(record))
            else:
                if record.exc_info:
                    a, b, tb = record.exc_info
                    tb = hide_me(tb, globals())
                    record.exc_info = a, b, tb
                result.append(pretty_unicode(formater.format(record)))
                result.append(u'\n')
        return u''.join(result)


class Processor(object):
    # 设置处理任务的时间限制为30秒
    PROCESS_TIME_LIMIT = 30
    # 设置异常限制为3次
    EXCEPTION_LIMIT = 3

    # 设置结果日志长度限制为1000字符
    RESULT_LOGS_LIMIT = 1000
    # 设置结果长度限制为10字符
    RESULT_RESULT_LIMIT = 10

    def __init__(self, projectdb, inqueue, status_queue, newtask_queue, result_queue,
                 enable_stdout_capture=True,
                 enable_projects_import=True,
                 process_time_limit=PROCESS_TIME_LIMIT):
        # 初始化输入队列、状态队列、新任务队列和结果队列
        self.inqueue = inqueue
        self.status_queue = status_queue
        self.newtask_queue = newtask_queue
        self.result_queue = result_queue
        self.projectdb = projectdb
        self.enable_stdout_capture = enable_stdout_capture

        # 设置退出标志为False
        self._quit = False
        # 设置异常计数为10
        self._exceptions = 10
        # 初始化项目管理器
        self.project_manager = ProjectManager(projectdb, dict(
            result_queue=self.result_queue,
            enable_stdout_capture=self.enable_stdout_capture,
            process_time_limit=process_time_limit,
        ))

        # 如果启用项目导入,则调用enable_projects_import函数
        if enable_projects_import:
            self.enable_projects_import()

    def enable_projects_import(self):
        '''
        启用导入其他项目作为模块的功能

        `from project import project_name`
        '''
        sys.meta_path.append(ProjectFinder(self.projectdb))

    def __del__(self):
        # 析构函数,暂时无需实现
        pass

    def on_task(self, task, response):
        '''处理一个任务'''
        # 记录任务开始时间
        start_time = time.time()
        # 重建响应对象
        response = rebuild_response(response)

        try:
            # 断言任务中包含taskid
            assert 'taskid' in task, 'need taskid in task'
            project = task['project']
            updatetime = task.get('project_updatetime', None)
            md5sum = task.get('project_md5sum', None)
            # 获取项目数据
            project_data = self.project_manager.get(project, updatetime, md5sum)
            assert project_data, "no such project!"
            if project_data.get('exception'):
                # 如果项目有异常,则将异常日志和异常对象作为结果返回
                ret = ProcessorResult(logs=(project_data.get('exception_log'), ),
                                      exception=project_data['exception'])

            else:
                # 否则运行项目实例的run_task函数处理任务
                ret = project_data['instance'].run_task(
                    project_data['module'], task, response)

        except Exception as e:
            # 如果发生异常,则将异常追踪信息作为日志和异常返回
            logstr = traceback.format_exc()
            ret = ProcessorResult(logs=(logstr, ), exception=e)
        # 计算任务处理时间
        process_time = time.time() - start_time

        # 如果不需要发送状态,则跳过以下步骤
        if not ret.extinfo.get('not_send_status', False):
            if ret.exception:
                # 如果有异常,则将响应头作为追踪头
                track_headers = dict(response.headers)
            else:
                # 否则只保留etag和last-modified头
                track_headers = {}
                for name in ('etag', 'last-modified'):
                    if name not in response.headers:
                        continue
                    track_headers[name] = response.headers[name]

            # 构造状态包
            status_pack = {
                'taskid': task['taskid'],
                'project': task['project'],
                'url': task.get('url'),
                'track': {
                    'fetch': {
                        'ok': response.isok(),
                        'redirect_url': response.url if response.url != response.orig_url else None,
                        'time': response.time,
                        'error': response.error,
                        'status_code': response.status_code,
                        'encoding': getattr(response, '_encoding', None),
                        'headers': track_headers,
                        'content': response.text[:500] if ret.exception else None,
                    },
                    'process': {
                        'ok': not ret.exception,
                        'time': process_time,
                        'follows': len(ret.follows),
                        'result': (
                            None if ret.result is None
                            else utils.text(ret.result)[:self.RESULT_RESULT_LIMIT]
                        ),
                        'logs': ret.logstr()[-self.RESULT_LOGS_LIMIT:],
                        'exception': ret.exception,
                    },
                    'save': ret.save,
                },
            }
            if 'schedule' in task:
                status_pack['schedule'] = task['schedule']

            # FIXME: unicode_obj应该在调度器中存储到数据库之前使用
            # 这里为了提高性能而使用
            self.status_queue.put(utils.unicode_obj(status_pack))

            # FIXME: unicode_obj应该在调度器中存储到数据库之前使用
            # 这里为了提高性能而使用
        if ret.follows:
            for each in (ret.follows[x:x + 1000] for x in range(0, len(ret.follows), 1000)):
                self.newtask_queue.put([utils.unicode_obj(newtask) for newtask in each])

        for project, msg, url in ret.messages:
            try:
                self.on_task({
                    'taskid': utils.md5string(url),
                    'project': project,
                    'url': url,
                    'process': {
                        'callback': '_on_message',
                    }
                }, {
                    'status_code': 200,
                    'url': url,
                    'save': (task['project'], msg),
                })
            except Exception as e:
                logger.exception('发送消息出错。')
                continue

        if ret.exception:
            logger_func = logger.error
        else:
            logger_func = logger.info

            # 打印出处理过程日志
        logger_func('处理 %s:%s %s -> [%d] 长度:%d -> 结果:%.10r 后续:%d 消息:%d 异常:%r 耗时:%d' % (
            task['project'], task['taskid'],
            task.get('url'), response.status_code, len(response.content),
            ret.result, len(ret.follows), len(ret.messages), ret.exception,process_time))
        # 打印出处理该任务所花费的时间
        return True

    def quit(self):
        '''设置退出信号'''
        self._quit = True

    def run(self):
        '''运行循环'''
        logger.info("processor启动中...")

        while not self._quit:
            try:
                task, response = self.inqueue.get(timeout=1)
                self.on_task(task, response)
                self._exceptions = 0
            except Queue.Empty as e:
                continue
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.exception(e)
                self._exceptions += 1
                if self._exceptions > self.EXCEPTION_LIMIT:
                    break
                continue

        logger.info("processor退出...")