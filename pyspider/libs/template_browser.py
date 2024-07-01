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
###
###proxy_tunnel = Setting.get_proxy()["http"].replace("http://","").replace("/","")
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
###                "classd_name": "漳州市工程项目网上中介服务平台(DYP)-重发公告",  # 此处填写来源名称
###                "table_name2": "ZBGG",  # 此处填写招标类型 招标公告:ZBGG, 中标公告:ZBGS
###                "ok_status": "Y"  # 此处值为  Y:意味着自动发布， N: 会进入二手临时
###               },
###              "start_page":0,
###              "end_page":5,
###              "step":1,
###              "list_url":"http://zjfw.zhangzhou.gov.cn/imng/zjfw/browse/resendBidNotice/bidNotice",
###              "post_data":{
###                    'pageno': 1,
###                }
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
###                post_data = task['post_data']
###                post_data["pageno"] = str(pageno)
###                requets_method = "POST"
###                if requets_method == "GET":
###                    self.crawl(list_url, method=requets_method, cookies=self.cookies,
###                               headers=headers, connect_timeout=20, callback=self.handle_list_page_xpath,
###                               save={"insert_d": insert_d}, validate_cert=False)
###                elif requets_method == "POST":
###                    if pageno == 1:# 当等于第一页的适合是不需要点击 下一页按钮的
###                        self.crawl(list_url, method=requets_method, data=post_data, cookies=self.cookies,
###                        headers=headers, connect_timeout=20, callback=self.handle_list_page_xpath, fetch_type='phantomjs',
###                        save={"insert_d":insert_d, "ajax_re":"BidNoticeCmd/queryResendList", "pageno":pageno,"tunnel_proxy":"no"})
###                    else:
###                        self.crawl(list_url, method=requets_method, data=post_data, cookies=self.cookies,
###                                    headers=headers, connect_timeout=20, callback=self.handle_list_page_xpath, ###fetch_type='phantomjs',
###                                    save={"insert_d":insert_d,
###                                         "ajax_re":"BidNoticeCmd/queryResendList",
###                                         "pageno":pageno,
###                                         "js_script":f'bltable.pageIndex({str(pageno)});queryBidNoticeList();',
###                                         "only_next_button":"no",
###                                         "tunnel_proxy":"no"}
###                                  )
###
###
###    # 第二步：获取到列表页html， 从中提取出可用信息
###    # XPATH方式处理列表页方式
###    @config(age=requests_expire_time)
###    def handle_list_page_xpath(self, response):
###        insert_d1 = response.save["insert_d"]
###        # 配置列表页xpath
###        list_xpath = '//*[@id="bid_notice_data"]//tr'
###        res_list = response.xpath(list_xpath)
###        self.logger.debug(f'当前列表页xpath共获取：{len(res_list)}元素\n')
###        for index, each in enumerate(res_list):
###            insert_d = copy.deepcopy(insert_d1)
###            # 配置标题xpath,detail_url等类似
###            insert_d["title"] = each.xpath(""".//a/attribute::title""")[0]
###            insert_d["comments"] = urljoin(response.url, each.xpath(""".//a/attribute::href""")[0])
###            insert_d["publish_date"] = ###each.xpath(""".//td[@class='text-muted']/text()""")[0].strip().replace("\n","").replace("\r","")
###            pattern = re.compile(r"bid_view\('([^']+)','([^']+)'\)")
###            match = pattern.search(insert_d["comments"])
###            if match:
###                row_item_id = match.group(1)
###                row_item_parent_bid_id = match.group(2)
###                real_detail_url = f"http://zjfw.zhangzhou.gov.cn/imng/zjfw/browse/resendBidNotice/###purchaseannouncement?id={row_item_id}&parentBidId={row_item_parent_bid_id}"
###                insert_d["comments"] = real_detail_url
###                detail_url = real_detail_url
###                print(f"\n列表页第{index}行数据: ", insert_d)
###                repeat_flag = myconfs.dedup_record(str_data=insert_d["comments"])
###                if repeat_flag["repeat"] == "true":
###                    self.logger.info(f'当前信息数据库已经存在：{repeat_flag}')
###                else:
###                    # 请在这里构造抓取详情页相关参数
###                    requets_method = "GET"
###                    cookies = {}
###                    headers = {}
###                    params = {}
###                    post_data = {}
###                    if requets_method == "GET":
###                        self.crawl(url=detail_url, method=requets_method, cookies=cookies,
###                                   headers=headers, connect_timeout=20, callback=self.handle_detail_page,
###                                   save={"insert_d": insert_d}, validate_cert=False, fetch_type='phantomjs')
###                    elif requets_method == "POST":
###                        self.crawl(url=detail_url, method=requets_method, cookies=cookies, data=post_data,
###                                   headers=headers, connect_timeout=20, callback=self.handle_detail_page,
###                                   save={"insert_d": insert_d}, validate_cert=False, fetch_type='phantomjs')
###
###    # 第三步：在第三步中判断我网没有此数据时进行下一步处理、提取并将数据存入公司数据库 XPATH选择器方式处理列表页方式
###    @config(age=requests_expire_time)
###    def handle_detail_page(self, response):
###        detail_xpath = '''//section[@class="article-body"]'''
###        insert_d = response.save["insert_d"]
###        content_etree = response.xpath(detail_xpath)[0]
###        html = etree.tostring(content_etree, encoding='unicode', method='html')
###        insert_d["description"] = relative_url_replace(response.url,remove_tags(html))
###        insert_result = insertd(insert_d)
###        print("最后结果", insert_result)
###        if is_debug:
###            self.send_message(self.project_name, insert_result, url="%s" % (response.url))
###            return insert_result
###        else:
###            pub_res = myconfs.publish_to_cms(insert_result)
###            if pub_res.isdigit():
###                self.logger.debug(f'发布成功：{pub_res}')
###            else:
###                raise Exception("发布失败")###