#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on __DATE__
# Project: __PROJECT_NAME__


###from pyspider.libs.base_handler import *
###from lxml import etree
###from mytools.mytools import base64_encode, base64_decode, relative_url_replace, get_response_type
###from mytools.mytools import formate_insertd, insertd, remove_tags, check_pdf_content,generate_html
###import requests, filetype, datetime, pytz, io
###from mytools import myconfs
###from urllib.parse import urlparse, urljoin, unquote
###from mytools.myconfs import Setting
###from urllib.parse import urlparse
###import json, copy, re, hashlib
###from collections import OrderedDict
###
###
###key_order = ['title', 'publish_date','comments','description','table_name2','classd_name']
###proxy_tunnel = Setting.get_proxy()["http"].replace("http://", "").replace("/", "")
###every_times = 3 * 60  # 每隔多少分钟启动抓取一次  单位:分钟
###requests_expire_time = 3 * 60 * 60  # 请求过期时间设置  单位:秒
###is_debug = True  # True 代表当前为测试阶段, False为生产环境
###
###
###class Handler(BaseHandler):
###    crawl_config = {
###    }
###
###    def __init__(self):
###        pass
###
###    # 第一步：构造列表页请求参数、地址
###    @every(minutes=every_times)
###    def on_start(self):
###        # 基础配置
###        task_list = [
###            # 栏目一
###            {
###                "insert_d": {
###                    "classd_name": "模板620(DYP)-中标公告",  # 此处填写来源名称
###                    "table_name2": "ZBGG",  # 此处填写招标类型 招标公告:ZBGG, 中标公告:ZBGS
###                    "ok_status": "Y"  # 此处值为  Y:意味着自动发布， N: 会进入二手临时
###                },
###                "start_page": 1,
###                "end_page": 5,
###                "step": 1,
###                "list_url": "http://www.mitu.cn/zbcg/list*pageno*.htm",
###                "post_data": {}
###            },
###
###        ]
###        for task in task_list:
###            insert_d = copy.deepcopy(task["insert_d"])
###            for pageno in range(task["start_page"], task["end_page"], task["step"]):
###                list_url = task["list_url"].replace("*pageno*", str(pageno))
###                print(f"正在抓取栏目:{insert_d['classd_name']}, 抓取第{pageno} 页, 列表页地址【{list_url}】")
###                self.cookies = {}
###                headers = {
###                }
###                params = {
###
###                }
###                post_data = {
###
###                }
###                # proxy=proxy_tunnel,data=json.dumps(post_data),fetch_type="phantomjs",save={"render_fini###sh_flag":{"expected_text":"名截止日期"}
###                requets_method = "GET"
###                if requets_method == "GET":
###                    self.crawl(url=list_url, method=requets_method, cookies=self.cookies,
###                               headers=headers, connect_timeout=25, timeout=25, ###callback=self.handle_list_page,
###                               save={"insert_d": insert_d}, validate_cert=False)
###                elif requets_method == "POST":
###                    list_url = list_url
###                    self.crawl(url=list_url, method=requets_method, cookies=self.cookies, data=post_data,
###                               headers=headers, connect_timeout=25, timeout=25, ###callback=self.handle_list_page,
###                               save={"insert_d": insert_d}, validate_cert=False)
###
###
###    # 第二步：获取到列表页html， 从中提取出可用信息
###    @config(age=requests_expire_time)
###    @config(priority=3)
###    def handle_list_page(self, response):
###        insert_d1 = response.save["insert_d"]
###        list_xpath = '''//*[@id="wp_news_w6"]//li'''  # 配置列表页xpath
###        #list_xpath = self.css_to_xpath("#wp_news_w6 li") css转xpath
###        res_list = response.xpath(list_xpath)
###        self.logger.debug(f'当前列表页xpath共获取：{len(res_list)}元素\n')
###        for index, each in enumerate(res_list):
###            insert_d = copy.deepcopy(insert_d1)
###            insert_d["title"] = each.xpath(""".//a/attribute::title""")[0]
###            detail_url = urljoin(response.url, each.xpath(""".//a/attribute::href""")[0])
###            insert_d["comments"] = detail_url
###            insert_d["publish_date"] = each.xpath(""".//span[@class='Article_PublishDate']/text()""")[0]
###            ordered_data = OrderedDict([(key, insert_d[key]) for key in key_order if key in insert_d])
###            print(f"\n第{index}行数据: ", dict(ordered_data))
###            repeat_flag = myconfs.dedup_record(str_data=insert_d,web_debug=is_debug)
###            if repeat_flag["repeat"] == "true":
###                self.logger.info(f'当前信息数据库已经存在：{repeat_flag}')
###            else:
###                # 请在这里构造抓取详情页相关参数
###                requets_method = "GET"
###                cookies = {}
###                headers = {}
###                params = {}
###                post_data = {}
###                # proxy=proxy_tunnel,data=json.dumps(post_data),fetch_type="phantomjs",save={"render_fini###sh_flag":{"expected_text":"名截止日期"}
###                if requets_method == "GET":
###                    self.crawl(url=detail_url, method=requets_method, cookies=cookies,
###                               headers=headers, connect_timeout=25, timeout=25, ###callback=self.handle_detail_page,
###                               save={"insert_d": insert_d}, validate_cert=False)
###                elif requets_method == "POST":
###                    self.crawl(url=detail_url, method=requets_method, cookies=cookies, data=post_data,
###                               headers=headers, connect_timeout=25, timeout=25, ###callback=self.handle_detail_page,
###                               save={"insert_d": insert_d}, validate_cert=False)
###
###
###
###    # 第三步：在第三步中判断我网没有此数据时进行下一步处理、提取并将数据存入公司数据库
###    @config(age=requests_expire_time)
###    @config(priority=4)
###    def handle_detail_page(self, response):
###        #generate_html(insert_dict, rule_dict) # insert_dict为网站详情页返回的json内容,rule_dict为对应的替换规则
###        detail_xpath = '''//*[@id="container"]//div[@class="read"]'''
###        insert_d = response.save["insert_d"]
###        content_etree = response.xpath(detail_xpath)[0]
###        html = etree.tostring(content_etree, encoding='unicode', method='html')
###        insert_d["description"] = relative_url_replace(response.url, remove_tags(html))
###        insert_d["files"] = []
###        insert_d["files"].append({'attachment_url':f"附件地址", "method":"GET", "req_data":{"headers":{}, ###"data":{}, "cookies":{}}})
###        insert_result = insertd(insert_d)
###        if is_debug:
###            self.send_message(self.project_name, insert_result, url="%s" % (response.url))
###            return insert_result
###        else:
###            pub_res = myconfs.publish_to_cms(insert_result)
###            if pub_res.isdigit():
###                self.logger.debug(f'发布成功：{pub_res}')
###            else:
###                raise Exception("发布失败")
###
###
###     #如果内容只有附件，调用这个函数
###    @config(age=requests_expire_time)
###    def handle_attach_page(self, response):
###        insert_d = response.save["insert_d"]
###        content_length = len(x.content)
###        content_length_in_kb = content_length / 1024
###        self.logger.info(f"文件大小: {kb:.2f} KB")
###        insert_d["description"] = f"<a href='{response.url}'>点击下载附件</a>"
###        x = response
###        md5_hash = hashlib.md5()
###        md5_hash.update(insert_d['comments'].encode('utf-8'))
###        file_id = md5_hash.hexdigest()
###        file_name = file_id + '.' + get_response_type(x)
###        current_time = datetime.datetime.now(pytz.timezone('PRC'))
###        today = current_time.strftime('%Y/%m/%d')
###        path = "B" + today + "/" + str(file_id) + "/"
###        if (int(content_length_in_kb) == 0):
###            self.logger.info(f"Content length: {content_length_in_kb:.2f} KB")
###        else:
###            xxx = myconfs.Setting.files_upload(x, path=path, file_name=file_name)
###            if not xxx:
###                self.logger.error(f"附件上传失败")
###            else:
###                attachment = {}
###                attachment["file_name"] = file_name
###                real_path = path + file_name
###                attachment["file_path"] = path + file_name if '.' not in path else path
###                insert_d["files"] = [attachment]
###                insert_result = insertd(insert_d)
###                if is_debug:
###                    self.send_message(self.project_name, insert_result, url="%s" % (response.url))
###                    return insert_result
###                else:
###                    pub_res = myconfs.publish_to_cms(insert_result)
###                    if pub_res.isdigit():
###                        self.logger.debug(f'发布成功：{pub_res}')
###                    else:
###                        raise Exception("发布失败")
###
###
###
###
