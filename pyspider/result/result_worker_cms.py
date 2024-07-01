#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
# http://binux.me
# Created on 2014-10-19 15:37:46

import time
import json
import logging
import requests
from six.moves import queue as Queue

logger = logging.getLogger("result")
import os
import datetime
import string
import zipfile
import string
import zipfile
import requests
import cpca
import sys
import os,json
import time
import lxml
import requests
from io import BytesIO
from sys import version_info
from lxml.html import fromstring, tostring
from bs4 import BeautifulSoup
from w3lib.html import remove_tags
from w3lib.html import remove_tags_with_content
from w3lib.html import remove_comments
from urllib.parse import urljoin
import asyncio
import aiohttp
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
requests.packages.urllib3.disable_warnings()
import requests
import json
import platform
# logger.add("./logs/conf.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", rotation="50 MB", filter="", level="ERROR", encoding='utf-8')

if platform.node() in ['doyus'] or platform.node().startswith("DESKTOP"):
    APP_DEBUGE = True # 测试
    api_upload_file = 'https://cp1091.sygnew.com/group1/upload'
    api_get_token = 'https://sso.sygnew.com/oauth/token'
    api_url_repeat = 'https://cp1091.sygnew.com/313039312e302e7379675f62616e64/datax/json/cms_deduplicate?device=cmsWSDCXVF&cpcode=cmsQSXCVB'
    api_pub_data = 'https://cp1091.sygnew.com/313039312e302e7379675f62616e64/datax/json/cms_repeat?device=cmsWSDCXVF&cpcode=cmsQSXCVB'
else:
    APP_DEBUGE = False # 生产
    api_url_repeat = 'http://192.168.36.163/313039312e302e7379675f62616e64/datax/json/cms_deduplicate?device=cmsWSDCXVF&cpcode=cmsQSXCVB'
    api_get_token = 'http://192.168.36.163/oauth/token'
    api_upload_file = 'http://192.168.36.163/group1/upload'
    api_pub_data = 'http://192.168.36.163/313039312e302e7379675f62616e64/datax/json/cms_repeat?device=cmsWSDCXVF&cpcode=cmsQSXCVB'

class ResultWorker(object):
    """
    Do with result
    override this if needed.
    """
    def __init__(self, inqueue):
        self.inqueue = inqueue
        self._quit = False

    def on_result(self, task, result):
        '''Called every result'''
        if not result:
            return

        if 'taskid' in task and 'project' in task and 'url' in task:
            logger.info('result %s:%s %s -> %.30r' % (task['project'], task['taskid'], task['url'], result))
            insert_data = {
                "area": task.get("area"),
                "category": task.get("category"),
                "publish_date": task.get("pubtime"),
                "title": task.get("title"),
                "content": f"<a href=\"{task.get('detail_url')}\">点击查看内容</a>",
                "duration": None,
                "original_id": task.get("main_id"),
                "is_deleted": False,
                "area_id": task.get("area_id"),
                "category_id": task.get("category_id"),
                "cust_id": "",
                "description": f"<a href=\"{task.get('detail_url')}\">点击查看内容</a>",
                "table_name": "ZBXX",
                "table_name2": task.get("news_type"),
                "ok_status": "Y",
                "html_id": "1",
                "comments": task.get("detail_url"),
                "classd_id": "二手",
                "classd_name": task.get("spider_name") + "-" + task.get("type_name"),
            }
            publish_response = publish_to_cms(insert_data, task.get("title"))
            logger.info(publish_response)
        else:
            logger.warning('result UNKNOW -> %.30r' % result)
            return

    def quit(self):
        self._quit = True

    def run(self):
        '''Run loop'''
        logger.info("result_worker starting...")
        while not self._quit:
            try:
                task, result = self.inqueue.get(timeout=1)
                self.on_result(task, result)
            except Queue.Empty as e:
                continue
            except KeyboardInterrupt:
                break
            except AssertionError as e:
                logger.error(e)
                continue
            except Exception as e:
                logger.exception(e)
                continue
        logger.info("result_worker exiting...")

def publish_to_cms(data, title):
    # 处理数据
    s_data = data.copy()
    if len(s_data['description']) < 20:
        logger.error(f"内容字段长度异常，低于20个字符:{s_data['description']}")
        raise "内容字段长度异常，低于20个字符"
    if len(data['title']) > 100:
        data['title'] = data['title'][:100] + "..."
        data['description'] = f"<h2>{title}</h2" + data['description']

    # 调用发布接口
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_pub_data, data=json.dumps(data), headers=headers)

    if response.status_code != 200:
        logger.error(f"发布失败，信息发布接口状态错误{response.text},{s_data}")
        raise "发布失败，信息发布接口错误"
    if "error.rs" in response.text:
        logger.error(f"发布失败，信息发布接口error.rs错误{response.text},{s_data}")
        raise "发布失败，信息发布接口错误"

    # 处理发布结果
    try:
        GENERATED_KEY = response.json()['data'][0]["GENERATED_KEY"]
        if len(GENERATED_KEY) < 3:
            logger.error(f"发布失败，信息发布接口无生产id错误{response.text},{s_data}")
            raise "发布失败，信息发布接口无生产id错误"
    except Exception as e:
        logger.error(f"发布失败，信息发布接口错误{e},{response.text},{s_data}")
        raise "发布失败，信息发布接口错误"

    return f"发布：{s_data['comments']}，发布接口状态：{response.status_code}, 返回：{response.text}"

def reduce_repeat(url, data):
    try:
        response = requests.post(url, json=data)
        text = response.json()
        item = {'url': data['comments'], 'repeat_count': text['data'][0]['repeat_count'], 'msg': text['msg']}
        return item
    except Exception as e:
        logger.error(f"去重接口报错{e}")

# 其他辅助函数
# ...