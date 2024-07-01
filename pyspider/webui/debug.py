#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-02-23 00:19:06
from flask import Flask, jsonify
import sys
import time
import socket
import inspect
from pypinyin import lazy_pinyin,pinyin
import datetime
from urllib.parse import urlparse
import traceback
from flask import render_template, request, json
from pyspider.libs import utils
import pytz
import re
try:
    import flask_login as login
except ImportError:
    from flask.ext import login

from pyspider.libs import utils, sample_handler, dataurl, template_browser, template_nomal
from pyspider.libs.response import rebuild_response
from pyspider.processor.project_module import ProjectManager, ProjectFinder
from .app import app
# from loguru import logger
# logger.add(".pyspider_hs.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", rotation="50 MB", filter="", level="DEBUG", encoding='utf-8')
logger = app.logger

default_task = {
    'taskid': 'data:,on_start',
    'project': '',
    'url': 'data:,on_start',
    'process': {
        'callback': 'on_start',
    },
}
# 代码检查



@app.route('/pyspider/debug/<project>', methods=['GET', 'POST'])
def debug(project):
    start_time = time.time()
    projectdb = app.config['projectdb']
    print("priject",project)
    if "sel_" in project:
        default_script = inspect.getsource(template_browser)
    else:
        default_script = inspect.getsource(template_nomal)
    if not projectdb.verify_project_name(project):
        return 'project name is not allowed!', 400
    info = projectdb.get(project, fields=['name', 'script','group'])
    if info:
        script = info['script']
    else:
        script = (default_script
                  .replace('__DATE__', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                  .replace('__PROJECT_NAME__', project)
                  .replace('###', "")
                  .replace('__START_URL__', request.values.get('start-urls') or '__START_URL__'))
    logger.debug(f"debug1耗时{time.time() - start_time}")

    taskid = request.args.get('taskid')
    if taskid:
        taskdb = app.config['taskdb']
        task = taskdb.get_task(
            project, taskid, ['taskid', 'project', 'url', 'fetch', 'process'])
    else:
        task = default_task
    logger.debug(f"debug2耗时{time.time() - start_time}")
    default_task['project'] = project
    return render_template("debug.html", task=task, script=script, project_name=project, gourp_name=info['group'])


# @app.before_first_request:修改: 新版本中已经删除
@app.before_request
def enable_projects_import():
    sys.meta_path.append(ProjectFinder(app.config['projectdb']))


@app.route('/pyspider/debug/<project>/pyspider/run', methods=['POST', ])
def run(project):
    start_time = time.time()
    try:
        task = utils.decode_unicode_obj(json.loads(request.form['task']))
    except Exception:
        result = {
            'fetch_result': "",
            'logs': u'task json error',
            'follows': [],
            'messages': [],
            'result': None,
            'time': time.time() - start_time,
        }
        return json.dumps(utils.unicode_obj(result)), \
            200, {'Content-Type': 'application/json'}

    project_info = {
        'name': project,
        'status': 'DEBUG',
        'script': request.form['script'],
    }

    fetch_result = {}
    try:
        module = ProjectManager.build_module(project_info, {
            'debugger': True,
            'process_time_limit': app.config['process_time_limit'],
        })
        # The code below is to mock the behavior that crawl_config been joined when selected by scheduler.
        # but to have a better view of joined tasks, it has been done in BaseHandler.crawl when `is_debugger is True`
        # crawl_config = module['instance'].crawl_config
        # task = module['instance'].task_join_crawl_config(task, crawl_config)

        fetch_result = app.config['fetch'](task)
        response = rebuild_response(fetch_result)
        ret = module['instance'].run_task(module['module'], task, response)
    except Exception:
        type, value, tb = sys.exc_info()
        tb = utils.hide_me(tb, globals())
        logs = ''.join(traceback.format_exception(type, value, tb))
        result = {
            'fetch_result': fetch_result,
            'logs': logs,
            'follows': [],
            'messages': [],
            'result': None,
            'time': time.time() - start_time,
        }
    else:
        result = {
            'fetch_result': fetch_result,
            'logs': ret.logstr(),
            'follows': ret.follows,
            'messages': ret.messages,
            'result': ret.result,
            'time': time.time() - start_time,
        }
        result['fetch_result']['content'] = response.text
        if (response.headers.get('content-type', '').startswith('image')):
            result['fetch_result']['dataurl'] = dataurl.encode(
                response.content, response.headers['content-type'])

    try:
        # binary data can't encode to JSON, encode result as unicode obj
        # before send it to frontend
        return json.dumps(utils.unicode_obj(result)), 200, {'Content-Type': 'application/json'}
    except Exception:
        type, value, tb = sys.exc_info()
        tb = utils.hide_me(tb, globals())
        logs = ''.join(traceback.format_exception(type, value, tb))
        result = {
            'fetch_result': "",
            'logs': logs,
            'follows': [],
            'messages': [],
            'result': None,
            'time': time.time() - start_time,
        }
        return json.dumps(utils.unicode_obj(result)), 200, {'Content-Type': 'application/json'}


@app.route('/pyspider/debug/<project>/save', methods=['POST', ])
def save(project):
    start_time = time.time()
    projectdb = app.config['projectdb']
    print(app.config)
    print(app.config['webui_username'])
    if not projectdb.verify_project_name(project):
        return 'project name is not allowed!', 400
    script = request.form['script']
    project_info = projectdb.get(project, fields=['name', 'status', 'group'])
    logger.debug(f"debugsave1耗时{time.time() - start_time}")
    if project_info and 'lock' in projectdb.split_group(project_info.get('group')) \
            and not login.current_user.is_active():
        return app.login_response
    # 获取当前 UTC 时间
    dt_utc = datetime.datetime.utcnow()
    # 定义中国标准时间（CST）时区
    cst_tz = pytz.timezone('Asia/Shanghai')
    # 将 UTC 时间转换为 CST
    dt_cst = dt_utc.replace(tzinfo=pytz.utc).astimezone(cst_tz)
    # print(444, dt_cst)
    # 打印 CST 时间
    print(dt_cst.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
    if project_info:
        info = {
            'script': script,
            'username': app.config['webui_username'],
            'update_date': dt_cst
        }
        print("更新", info)
        if project_info.get('status') in ('DEBUG', 'RUNNING', ):
            info['status'] = 'CHECKING'
        projectdb.update(project, info)
    else:
        info = {
            'name': project,
            'script': script,
            'status': 'TODO',
            'rate': app.config.get('max_rate', 1),
            'burst': app.config.get('max_burst', 2),
            'username':app.config['webui_username'],
            'update_date': dt_cst
        }
        projectdb.insert(project, info)
    logger.debug(f"debugsave2耗时{time.time() - start_time}")
    rpc = app.config['scheduler_rpc']
    if rpc is not None:
        try:
            rpc.update_project()
        except socket.error as e:
            app.logger.warning('connect to scheduler rpc error: %r', e)
            return 'rpc error', 200

    return 'ok', 200


@app.route('/pyspider/debug/<project>/get')
def get_script(project):
    projectdb = app.config['projectdb']
    if not projectdb.verify_project_name(project):
        return 'project name is not allowed!', 400
    info = projectdb.get(project, fields=['name', 'script'])
    return json.dumps(utils.unicode_obj(info)), \
        200, {'Content-Type': 'application/json'}



@app.route('/pyspider/debug/create_task', methods=['POST', ])
def create_task():
    pinyin_to_hanzi = {
        "dongyupeng": "DYP",
        "kangyanshuo": "KYS",
        "kongchao": "KC",
        "liziyang": "LZY",
        "tangjingbo": "TJB",
        "wanglei": "WL",
        "wangmengyu": "WMY",
        "xubinjie": "XBJ",
        "yangyong": "YY",
        "zhangjingsong": "ZJS",
        "zhangwensong": "ZWS",
        "super": "DYP",
        "tongxun": "TX",
        "zhaosiyu": "ZSY",
        "xunxiaofan": "XXF",
        "gongmiqi": "GMQ"
    }

    projectdb = app.config['projectdb']
    data = request.get_json()
    gourp = data.get('project_name') # gourp

    class_name = data.get('class_name')
    start_urls = data.get('start_urls')
    username = app.config['webui_username']
    parsed_url = urlparse(start_urls)
    main_host = parsed_url.netloc
    try:
        pattern = r'[^\w\s]'
        class_name = re.sub(pattern, '_', class_name)
    except Exception as e:
        print("名称错误",e)
    class_name_pinyin = "".join(lazy_pinyin(class_name))
    project = main_host.replace(".","_").replace(":","_")+"_"+class_name_pinyin
    project = utils.replace_chinese_punctuation(project)
    # print("创建任务接受到的参数",data, project)
    if not projectdb.verify_project_name(project):
        return 'project name is not allowed!', 400
    default_script = inspect.getsource(template_nomal)
    gourp_name = f"{gourp}({pinyin_to_hanzi[username]})-{class_name}"
    default_script = default_script.replace("WANGZHANMINGCHENG", gourp_name)
    default_script = (default_script
                      .replace('__DATE__', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                      .replace('__PROJECT_NAME__', project)
                      .replace('###', "")
                      .replace('__START_URL__', request.values.get('start-urls') or '__START_URL__'))
    script = default_script
    row = next(projectdb._select2dic(
        tablename='pyspider_project',
        what=['name', 'group', 'status', 'script', 'comments', 'rate', 'burst', 'updatetime', 'username', 'main_host',
              'class_name'],
        where="main_host = %s",
        where_values=[main_host]
    ), None)
    if row:
        if username != row['username']:
            msg = f"此任务与{row['username']}重复，请检查{row['group']},{row['name']}"
            status = {
                'status': 'repeat',
                'message': msg,
                'project': ''
            }
            return jsonify(status, 200)  # 状态码为 200
        else:
            script = row['script']
            gourp_name = f"{row['group'].split('-')[0]}-{class_name}"
            script = script.replace(row['group'],gourp_name)
            info = {
                'group': gourp_name,
                'main_host': main_host,
                'class_name': class_name,
                'name': project,
                'script': script,
                'status': 'TODO',
                'rate': app.config.get('max_rate', 1),
                'burst': app.config.get('max_burst', 2),
                'username': app.config['webui_username']
            }
            try:
                projectdb.insert(project, info)
            except:
                msg = f"此任务重复，请检查{row['group']},{row['name']}"
                status = {
                    'status': 'repeat',
                    'message': msg,
                    'project': ''
                }
                return jsonify(status, 200)  # 状态码为 200
            rpc = app.config['scheduler_rpc']
            if rpc is not None:
                try:
                    rpc.update_project()
                except socket.error as e:
                    app.logger.warning('connect to scheduler rpc error: %r', e)
                    return 'rpc error', 200
            status = {
                'status': 'ok',
                'message': "创建成功",
                'project': project
            }
            return jsonify(status, 200)  # 状态码为 200

    else:
        info = {
            'group': gourp_name,
            'main_host': main_host,
            'class_name': class_name,
            'name': project,
            'script': script,
            'status': 'TODO',
            'rate': app.config.get('max_rate', 1),
            'burst': app.config.get('max_burst', 2),
            'username':app.config['webui_username']
        }
        projectdb.insert(project, info)
        rpc = app.config['scheduler_rpc']
        if rpc is not None:
            try:
                rpc.update_project()
            except socket.error as e:
                app.logger.warning('connect to scheduler rpc error: %r', e)
                return 'rpc error', 200
        status = {
            'status': 'ok',
            'message': "创建成功",
            'project': project
        }
        return jsonify(status, 200)  # 状态码为 200


@app.route('/blank.html')
def blank_html():
    return ""
