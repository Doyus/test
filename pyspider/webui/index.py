#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-02-22 23:20:39

import socket
import time

from six import iteritems, itervalues
from flask import render_template, request, json
try:
    import flask_login as login
except ImportError:
    from flask.ext import login
# from loguru import logger
from pyspider.mytools import myconfs

from .app import app
logger = app.logger

# logger.add(".pyspider_hs.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", rotation="50 MB", filter="", level="DEBUG", encoding='utf-8')
index_fields = ['name', 'group', 'status', 'comments', 'rate', 'burst', 'updatetime']


# 设置每页显示的项目数量（可配置）
PER_PAGE = 20

@app.route('/pyspider/index')
def index():
    projectdb = app.config['projectdb']
    page_num = int(request.args.get('page', 1))
    page_size = 30
    username = app.config['webui_username']
    if username == "super":
        projects = sorted(projectdb.get_page(page_num, page_size, fields=index_fields),
                          key=lambda k: (0 if k['group'] else 1, k['group'] or '', k['name']))
        return render_template("index.html", projects=projects, total=1000, page=page_num, keyword="")
    else:
        where = "`username` = %s"
        where_values = [username]
        projects = sorted(
            projectdb.get_page(page_num, page_size, fields=index_fields, where=where, where_values=where_values),
            key=lambda k: (0 if k['group'] else 1, k['group'] or '', k['name']))
        return render_template("index.html", projects=projects, total=1000, page=page_num, keyword="")


@app.route('/pyspider/search')
def search():
    projectdb = app.config['projectdb']
    page_num = int(request.args.get('page', 1))
    page_size = 30
    keyword = request.args.get('keyword', '').strip()
    username = app.config['webui_username']
    if len(keyword) == 0:
        if username == "super":
            projects = sorted(projectdb.get_page(page_num, page_size, fields=index_fields),
                              key=lambda k: (0 if k['group'] else 1, k['group'] or '', k['name']))
            return render_template("index.html", projects=projects, total=1000, page=page_num, keyword="")
        else:
            where = "`username` = %s"
            where_values = [username]
            projects = sorted(
                projectdb.get_page(page_num, page_size, fields=index_fields, where=where, where_values=where_values),
                key=lambda k: (0 if k['group'] else 1, k['group'] or '', k['name']))
            return render_template("index.html", projects=projects, total=1000, page=page_num, keyword="")
    else:
        if username == "super":
            if keyword.upper() in ["TODO","STOP","CHECKING","DEBUG","RUNNING"]:
                where = "`status` LIKE %s"
                where_values = [f'%%{keyword}%%']
                projects = sorted(projectdb.get_page(page_num, page_size, fields=index_fields, where=where,
                                                     where_values=where_values),
                                  key=lambda k: (0 if k['group'] else 1, k['group'] or '', k['name']))
                return render_template("index.html", projects=projects, total=100, page=page_num, keyword=keyword)
            else:
                where = "`group` LIKE %s"
                where_values = [f'%%{keyword}%%']
                projects = sorted(projectdb.get_page(page_num, page_size, fields=index_fields, where=where,
                                                     where_values=where_values),
                                  key=lambda k: (0 if k['group'] else 1, k['group'] or '', k['name']))
                return render_template("index.html", projects=projects, total=100, page=page_num, keyword=keyword)

        else:
            if keyword.upper() in ["TODO", "STOP", "CHECKING", "DEBUG", "RUNNING"]:
                where = "`username` = %s AND `status` LIKE %s"
                where_values = [username, f'%%{keyword}%%']
                projects = sorted(
                    projectdb.get_page(page_num, page_size, fields=index_fields, where=where, where_values=where_values),
                    key=lambda k: (0 if k['group'] else 1, k['group'] or '', k['name']))
                return render_template("index.html", projects=projects, total=100, page=page_num, keyword=keyword)
            else:
                where = "`username` = %s AND `group` LIKE %s"
                where_values = [username, f'%%{keyword}%%']
                projects = sorted(
                    projectdb.get_page(page_num, page_size, fields=index_fields, where=where,
                                       where_values=where_values),
                    key=lambda k: (0 if k['group'] else 1, k['group'] or '', k['name']))
                return render_template("index.html", projects=projects, total=100, page=page_num, keyword=keyword)

@app.route('/pyspider/queues')
def get_queues():
    def try_get_qsize(queue):
        if queue is None:
            return 'None'
        try:
            return queue.qsize()
        except Exception as e:
            return "%r" % e

    result = {}
    queues = app.config.get('queues', {})
    for key in queues:
        result[key] = try_get_qsize(queues[key])
    return json.dumps(result), 200, {'Content-Type': 'application/json'}


@app.route('/pyspider/update', methods=['POST', ])
def project_update():
    projectdb = app.config['projectdb']
    project = request.form['pk']
    name = request.form['name']
    value = request.form['value']
    project_info = projectdb.get(project, fields=('name', 'group'))
    if not project_info:
        return "no such project.", 404
    if 'lock' in projectdb.split_group(project_info.get('group')) \
            and not login.current_user.is_active():
        return app.login_response

    if name not in ('group', 'status', 'rate'):
        return 'unknown field: %s' % name, 400
    if name == 'rate':
        value = value.split('/')
        if len(value) != 2:
            return 'format error: rate/burst', 400
        rate = float(value[0])
        burst = float(value[1])
        update = {
            'rate': min(rate, app.config.get('max_rate', rate)),
            'burst': min(burst, app.config.get('max_burst', burst)),
        }
    else:
        update = {
            name: value
        }

    ret = projectdb.update(project, update)
    if ret:
        rpc = app.config['scheduler_rpc']
        if rpc is not None:
            try:
                rpc.update_project()
            except socket.error as e:
                logger.warning('connect to scheduler rpc error: %r', e)
                return 'rpc error', 200
        return 'ok', 200
    else:
        logger.warning("[webui index] projectdb.update() error - res: {}".format(ret))
        return 'update error', 500


@app.route('/pyspider/counter')
def counter():
    rpc = app.config['scheduler_rpc']
    if rpc is None:
        return json.dumps({})

    result = {}
    try:
        data = rpc.webui_update()
        for type, counters in iteritems(data['counter']):
            for project, counter in iteritems(counters):
                result.setdefault(project, {})[type] = counter
        for project, paused in iteritems(data['pause_status']):
            result.setdefault(project, {})['paused'] = paused

    except socket.error as e:
        logger.warning('connect to scheduler rpc error: %r', e)
        return json.dumps({}), 200, {'Content-Type': 'application/json'}
    return json.dumps(result), 200, {'Content-Type': 'application/json'}


@app.route('/pyspider/run', methods=['POST', ])
def runtask():
    project = request.form['project']
    rpc = app.config['scheduler_rpc']
    #rpc.delete_all_tasks(project)
    if rpc is None:
        return json.dumps({})
    if len(project)>3:
        try:
            logger.warning('删除历史任务: %r', project)
            app.config['taskdb'].delete_keys_with_pattern(project)
        except Exception as e:
            logger.error('删除历史任务失败: %r', e)
    projectdb = app.config['projectdb']
    project_info = projectdb.get(project, fields=('name', 'group'))
    if not project_info:
        return "no such project.", 404
    if 'lock' in projectdb.split_group(project_info.get('group')) \
            and not login.current_user.is_active():
        return app.login_response

    newtask = {
        "project": project,
        "taskid": "on_start",
        "url": "data:,on_start",
        "process": {
            "callback": "on_start",
        },
        "schedule": {
            "age": 0,
            "priority": 9,
            "force_update": True,
        },
    }
    try:
        ret = rpc.newtask(newtask)
    except Exception as e:
        err_info = f'connect to scheduler rpc error: {e}'
        logger.warning(err_info)
        try:
            myconfs.Setting.send_wechat(err_info)
        except Exception as e:
            logger.error(e)
        return json.dumps({"result": False}), 200, {'Content-Type': 'application/json'}
    return json.dumps({"result": ret}), 200, {'Content-Type': 'application/json'}


@app.route('/robots.txt')
def robots():
    return """User-agent: *
Disallow: /
Allow: /$
Allow: /debug
Disallow: /pyspider/debug/*?taskid=*
""", 200, {'Content-Type': 'text/plain'}
