#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on __DATE__
# Project: __PROJECT_NAME__

###from pyspider.libs.base_handler import *
###from lxml import etree
###from mytools.mytools import base64_encode, base64_decode,relative_url_replace,get_response_type
###from mytools.mytools import formate_insertd, insertd, remove_tags, check_pdf_content
###import requests, filetype, datetime, pytz, io
###from mytools import myconfs
###from urllib.parse import urlparse, urljoin, unquote
###from mytools.myconfs import Setting
###from urllib.parse import urlparse
###import json, copy, re
###from cssselect import GenericTranslator
###
###every_times = 3*60 #每隔多少分钟启动抓取一次  单位:分钟
###requests_expire_time = 3 * 60 * 60 # 请求过期时间设置  单位:秒
###is_debug = True  # True 代表当前为测试阶段
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
###              # 栏目一
###              {
###               "insert_d": {
###                "classd_name": "福建信息职业技术学院(DYP)-招标采购",  # 此处填写来源名称
###                "table_name2": "ZBGG",  # 此处填写招标类型 招标公告:ZBGG, 中标公告:ZBGS
###                "ok_status": "Y"  # 此处值为  Y:意味着自动发布， N: 会进入二手临时
###               },
###              "start_page":1,
###              "end_page":5,
###              "step":1,
###              "list_url":"http://www.mitu.cn/zbcg/list*pageno*.htm",
###              "post_data":{}
###              },
###
###         ]
###        for task in task_list:
###            insert_d = task["insert_d"]
###            for pageno in range(task["start_page"], task["end_page"], task["step"]):
###                list_url = task["list_url"].replace("*pageno*",str(pageno))
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
###                requets_method = "GET"
###                if requets_method == "GET":
###                    self.crawl(list_url, method=requets_method, cookies=self.cookies,
###                               headers=headers, connect_timeout=20, callback=self.handle_list_page_xpath,
###                               save={"insert_d": insert_d}, validate_cert=False)
###                elif requets_method == "POST":
###                    list_url = list_url
###                    self.crawl(list_url, method=requets_method, cookies=self.cookies, data=post_data,
###                               headers=headers, connect_timeout=20, callback=self.handle_list_page_xpath,
###                               save={"insert_d": insert_d}, validate_cert=False)
###
###
###    # 第二步：获取到列表页html， 从中提取出可用信息
###    # XPATH方式处理列表页方式
###    @config(age=requests_expire_time)
###    def handle_list_page_xpath(self, response):
###        insert_d = response.save["insert_d"]
###        # 配置列表页xpath
###        list_doc = """"""
###        list_xpath = '''//*[@id="wp_news_w6"]//li'''
###        if len(list_doc) > 1:
###            list_xpath = GenericTranslator().css_to_xpath(list_doc)
###        res_list = response.xpath(list_xpath)
###        print("获取到元素", len(res_list),"\n")
###        for index, each in enumerate(res_list):
###            insert_d = copy.deepcopy(insert_d)
###            # 配置标题xpath,detail_url等类似
###            insert_d["title"] = each.xpath(""".//a/attribute::title""")[0]
###            insert_d["comments"] = urljoin(response.url, each.xpath(""".//a/attribute::href""")[0])
###            insert_d["publish_date"] = each.xpath(""".//span[@class='Article_PublishDate']/text()""")[0]
###            print(f"列表页提取数据第{index}行数据: ", insert_d)
###            # 得到详情页地址后判断与cms是否已经存在
###            self.crawl(myconfs.api_url_repeat, method='POST', data={'comments': base64_encode(insert_d["comments"])},
###                       callback=self.judge_repeat_flag, save={"insert_d": insert_d}, validate_cert=False)
###
###    # 第三步：在第二步中提取到详情页url地址后，需要先去公司数据库查重，如果没有才进行后续处理
###    # 排重接口
###    @config(age=requests_expire_time)
###    def judge_repeat_flag(self, response):
###        insert_d = response.save["insert_d"]
###        repeat_data = json.loads(response.text)
###        repeat_count = repeat_data['data'][0]['repeat_count']
###        if int(repeat_count) > 0:
###            self.logger.info(f'当前信息数据库已经存在：{repeat_data}')
###        else:
###            self.logger.info(f'正在进行详情页处理：{repeat_data}')
###            self.crawl(insert_d["comments"], callback=self.handle_detail_page_xpath, save={"insert_d": insert_d})
###
###    # 第四步：在第三步中判断我网没有此数据时进行下一步处理、提取并将数据存入公司数据库
###    @config(age=requests_expire_time)
###    def handle_detail_page_xpath(self, response):
###        detail_doc = ""
###        detail_xpath = '''//*[@id="container"]//div[@class="read"]'''
###        if len(detail_doc) > 1:
###            detail_xpath = GenericTranslator().css_to_xpath(detail_doc)
###        insert_d = response.save["insert_d"]
###        content_etree = response.xpath(detail_xpath)[0]
###        html = etree.tostring(content_etree, encoding='unicode', method='html')
###        insert_d["description"] = relative_url_replace(response.url,remove_tags(html))
###        # 最终明文数据的结果
###        insert_result = insertd(insert_d)
###        print("最终结果", insert_result)
###        if is_debug:
###            self.send_message(self.project_name, insert_result, url="%s" % (response.url))
###            return insert_result
###        else:
###            # 进行编码后的结果
###            cms_insert = formate_insertd(insert_result, insert_result["title"])
###            self.crawl(myconfs.api_pub_data + f"#page-{cms_insert['deduct_md5']}", method='POST', data=cms_insert,
###                       callback=self.save_cms_database, save={"insert_d": cms_insert}, validate_cert=False)
###
###    # 第五步：保存数据进入cms公司数据库
###    @config(age=requests_expire_time)
###    @config(priority=3)
###    def save_cms_database(self, response):
###        self.logger.info(f'当前数据已经发送到cms：{response.text}')
###
###    # AJAX选择器方式处理列表页方式
###    @config(age=requests_expire_time)
###    def handle_list_page_ajax(self, response):
###        pass
###
###    # 获取附件地址
###    @config(age=requests_expire_time)
###    def get_pdf_url(self, detail, detail_url):
###        url_list = []
###        tree = etree.HTML(detail)
###        pdfs = tree.xpath(
###            "//*[contains(text(), '.PDF') or contains(text(), '.JPEG') or contains(text(), '.JPG') or contains(text(), '.RAR') or contains(text(), '.DOCX') or contains(text(), ###'.XLSX') or contains(text(), '.XLS') or contains(text(), '.ZIP') or contains(text(), '.PNG') or contains(text(), '.DOC') or  contains(text(), '.GZSZB') or contains(###text(), '.pdf') or contains(text(), '.jpeg') or contains(text(), '.jpg') or contains(text(), '.rar') or contains(text(), '.docx') or contains(text(), '.xlsx') or ###contains(text(), '.xls') or contains(text(), '.zip') or contains(text(), '.png') or contains(text(), '.doc') or contains(text(), '.GZSZB') or contains(@href,'.pdf') ###or contains(@href,'.jpeg') or contains(@href,'.jpg') or contains(@href,'.rar') or contains(@href,'.docx') or contains(@href,'.xlsx') or contains(@href,'.xls') or ###contains(@href,'.zip') or contains(@href,'.png') or contains(@href,'.doc') or contains(@href,'.GZSZB') or contains(@href,'.PDF') or contains(@href,'.JPEG') or ###contains(@href,'.JPG') or contains(@href,'.RAR') or contains(@href,'.DOCX') or contains(@href,'.XLSX') or contains(@href,'.XLS') or contains(@href,'.ZIP') or ###contains(@href,'.PNG') or contains(@href,'.DOC') or contains(@src,'.pdf') or contains(@src,'.jpeg') or contains(@src,'.jpg') or contains(@src,'.rar') or ###contains(@src,'.docx') or contains(@src,'.xlsx') or contains(@src,'.xls') or contains(@src,'.zip') or contains(@src,'.png') or contains(@src,'.doc') or ###contains(@src,'.GZSZB') or contains(@src,'.PDF') or contains(@src,'.JPEG') or contains(@src,'.JPG') or contains(@src,'.RAR') or contains(@src,'.DOCX') or ###contains(@src,'.XLSX') or contains(@src,'.XLS') or contains(@src,'.ZIP') or contains(@src,'.PNG') or contains(@src,'.DOC')]")
###        for x in pdfs:
###            url = x.xpath('.//@href|.//@src')
###            if url:
###                url = url[0].replace(' ', '')
###                if 'ec.runshihua.com/web/web/viewer.html' in url:
###                    url = unquote(url.split('file=')[-1])
###                if 'ec.runshihua.com/web/web/viewer.html' in url:
###                    url = unquote(url.split('file=')[-1])
###                if 'file:///C:\\Users' in url:
###                    continue
###                if 'file:///C:/Users' in url:
###                    continue
###                if 'javascript:void(0)' in url:
###                    continue
###                if 'http' not in url:
###                    url = urljoin(detail_url, url)
###                url_list.append({
###                    'url': url
###                })
###        return url_list
###
###    @config(age=requests_expire_time)
###    def file_downup(self, pdf_url, file_id):
###        for x in range(3):
###            try:
###                self.logger.info(f'正在下载：{pdf_url}')
###                headers = {
###                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61"
###                }
###                attachment = {}
###                current_time = datetime.datetime.now(pytz.timezone('PRC'))
###                today = current_time.strftime('%Y/%m/%d')
###                x = requests.get(url=pdf_url, headers=headers, proxies=myconfs.Setting.get_proxy(), timeout=(3, 60))
###                file_name = file_id + '.' + get_response_type(x)
###                path = "B" + today + "/" + str(file_id) + "/"
###                content_length = len(x.content)
###                content_length_in_kb = content_length / 1024
###                self.logger.info(f"Content length: {content_length_in_kb:.2f} KB")
###                if (int(content_length_in_kb) == 0):
###                    print(f'{str(content_length_in_kb)}下载文件太小')
###                    return None
###                if 'pdf' in file_name:
###                    if not check_pdf_content(x.content, ""):
###                        continue
###                xxx = myconfs.Setting.files_upload(x, path=path, file_name=file_name)
###                if not xxx:
###                    return None
###                attachment["file_name"] = file_name
###                real_path = path + file_name
###                attachment["file_path"] = path + file_name if '.' not in path else path
###                return attachment
###            except Exception as e:
###                self.logger.error(e)
###
###    def on_message(self, project, msg):
###        return msg
###
###
###
###