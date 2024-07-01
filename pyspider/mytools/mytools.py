# coding=utf-8
# -*- encoding: utf-8 -*-
"""
Name : tools.py
Author  : dos
Contect : 
Time    : 2023/9/13 9:26
Desc: 
"""
import string
import zipfile
import requests
from urllib.parse import urlparse
import cpca
import sys
import os,json
import filetype
import io
import lxml
import requests
from io import BytesIO
from sys import version_info
from lxml.html import fromstring, tostring
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time, datetime
from dateutil import parser as date_string_parser
import copy
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
requests.packages.urllib3.disable_warnings()
import re
from loguru import logger
import PyPDF2
import pikepdf
import pypdf
import io
from pyDes import des, PAD_PKCS5, ECB
import base64
import json
import time
from PIL import Image
from io import BytesIO
import cv2,ddddocr
import numpy as np
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.Cipher import AES, DES
from Crypto import Random
import hashlib
import pdfplumber
# from Crypto.Cipher import DES
# from Crypto.Cipher import DES
# 64位ID的划分
# WORKER_ID_BITS = 5
WORKER_ID_BITS = 1
# DATACENTER_ID_BITS = 5
DATACENTER_ID_BITS = 1
# SEQUENCE_BITS = 12
SEQUENCE_BITS = 10
# 最大取值计算
# 移位偏移计算
WOKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS
# Twitter元年时间戳
# 机器id所占的位数
WORKER_ID_BITS = 10
# 数据中心id所占的位数
DATACENTER_ID_BITS = 5
# 毫秒内序列所占的位数
SEQUENCE_BITS = 12
# 机器ID最大值
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)
# 数据中心ID最大值
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)
# 幂等毫秒内序列最大值
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)
# 生成ID的起始时间戳,可根据业务设置
TWEPOCH = 1577808000000
# 时间戳相对值位数
TIMESTAMP_BITS = 6
# 数据中心id位数
DATACENTER_ID_BITS = 2
# 机器id位数
WORKER_ID_BITS = 4
# 毫秒内序列号位数
SEQUENCE_BITS = 4

area_dict ={"北京":1,"上海":2,"天津":3,"重庆":4,"河北":5,"山西":6,"内蒙":7,"内蒙古":7,"辽宁":8,
"吉林":9,"黑龙江":10,"江苏":11,"浙江":12,"安徽":13,"福建":14,"江西":15,"山东":16,"河南":17,
"湖北":18,"湖南":19,"广东":20,"广西":21,"海南":22,"贵州":23,"云南":24,"西藏":25,"陕西":26,"四川":27,
"甘肃":28,"青海":29,"新疆":30,"宁夏":31,"香港":32,"澳门":33,"台湾":34,"跨省":36,
"亚洲":43,"欧洲":44,"非洲":45,"北美洲":46,"南美洲":47,"大洋洲":48,"中美洲":49,"加勒比":50,
"北京市":1,"上海市":2,"天津市":3,"重庆市":4,"河北省":5,"山西省":6,"辽宁省":8,"吉林省":9,
"黑龙江省":10,"江苏省":11,"浙江省":12,"安徽省":13,"福建省":14,"江西省":15,"山东省":16,
"河南省":17,"湖北省":18,"湖南省":19,"广东省":20,"海南省":22,"贵州省":23,"云南省":24,
"陕西省":26,"四川省":27,"甘肃省":28,"青海省":29,"香港特区":32,"香港特别行政区":32,"澳门特区":33,"台湾省":34,
"广西自治区":21,"新疆自治区":30,"宁夏自治区":31,"内蒙古自治区":7,"西藏自治区":25,"广西壮族自治区":21,"新疆维吾尔自治区":30,"宁夏回族自治区":31,}

cate_dict = {
    "1":"交通运输",
    "2":"网络通讯计算机",
    "3":"市政房地产建筑",
    "4":"水利桥梁",
    "5":"机械电子电器",
    "6":"环保",
    "8":"医疗卫生",
    "9":"科技文教旅游",
    "10":"冶金矿产原材料",
    "11":"出版印刷",
    "12":"轻工纺织食品",
    "13":"农林牧渔",
    "14":"商业服务",
    "15":"其它",
    "16":"园林绿化",
    "17":"能源",
    "18":"化工",
    "":"未知"
}

cate_inv = {
    "园林绿化": "16",
    "商业服务": "14",
    "能源": "17",
    "冶金矿产原材料": "10",
    "农林牧渔": "13",
    "机械电子电器": "5",
    "医疗卫生": "8",
    "科技文教旅游": "9",
    "其它": "15",
    "轻工纺织食品": "12",
    "环保": "6",
    "市政房地产建筑": "3",
    "出版印刷": "11",
    "网络通讯计算机": "2",
    "交通运输": "1",
    "未知": "",
    "化工": "18",
    "水利桥梁": "4",
    "房屋建筑": "3",
    "市政": "3",
    "信息电子": "2",
    "广电通信": "2",
    "科教文卫": "9",
    "石油石化": "17",
    "能源电力": "17",
    "化学工业": "18",
    "水运": "1",
    "铁路": "1",
    "公路": "1",
    "民航": "1",
    "航空航天": "1",
    "港口航道": "1",
    "机械设备": "5",
    "保险金融": "14",
    "水利水电": "17",
    "矿产冶金": "10",
    "生态环保": "6",
    "生物医药": "8",
    "其他": "15",
    "纺织轻工": "12"
}

def parse_curl_command(curl_command: str):
    # -> Dict[str, Union[str, Dict[str, str], Dict[str, list]]]
    url_pattern = r'(https?://[^\s\'"]+)'
    header_pattern = r'-H\s+([\'"])(.+?)\1'
    data_pattern = r'--data-raw\s+([\'"])(.+?)\1'
    cookie_pattern = r'--cookie\s+([\'"])(.+?)\1'
    method_pattern = r'--request\s+(\w+)'
    result = {}

    url_match = re.search(url_pattern, curl_command)
    if url_match:
        result['url'] = url_match.group(1)

    header_matches = re.findall(header_pattern, curl_command)
    if header_matches:
        headers = {}
        for header_match in header_matches:
            header_key, header_value = header_match[1].split(': ', 1)
            headers[header_key] = header_value
        result['headers'] = headers

    data_match = re.search(data_pattern, curl_command)
    if data_match:
        try:
            result['data'] = json.loads(data_match.group(2))
        except json.JSONDecodeError:
            result['data'] = data_match.group(2)

    cookie_matches = re.findall(cookie_pattern, curl_command)
    if cookie_matches:
        cookies = {}
        for cookie_match in cookie_matches:
            for cookie in cookie_match[1].split('; '):
                cookie_key, cookie_value = cookie.split('=', 1)
                cookies[cookie_key] = cookie_value
        result['cookies'] = cookies

    method_match = re.search(method_pattern, curl_command)
    if method_match:
        result['method'] = method_match.group(1).upper()
    else:
        result['method'] = 'GET'

    return result

def flatten_dict(nested_dict):
    def get_all_keys(d):
        keys = set()
        for key, value in d.items():
            keys.add(key)
            if isinstance(value, dict):
                keys.update(get_all_keys(value))
        return keys

    all_keys = get_all_keys(nested_dict)
    duplicate_keys = set([key for key in all_keys if list(all_keys).count(key) > 1])

    def flatten(d, prefix=''):
        items = []
        for key, value in d.items():
            new_key = f"{prefix}_{key}" if key in duplicate_keys and prefix else key
            if isinstance(value, dict):
                items.extend(flatten(value, new_key).items())
            else:
                items.append((new_key, value))
        return dict(items)

    return flatten(nested_dict)

def generate_html(insert_dict, rule_dict):
    insert_dict = flatten_dict(insert_dict)
    def convert_to_html(value, key):
        if isinstance(value, dict):
            html_table = "<table border='1'>\n"
            for sub_key, sub_value in value.items():
                if sub_key in rule_dict:
                    display_key = rule_dict[sub_key]
                    html_table += f"  <tr><td>{display_key}</td><td>{convert_to_html(sub_value, sub_key)}</td></tr>\n"
            html_table += "</table>\n"
            return html_table
        elif isinstance(value, list):
            html_table = "<table border='1'>\n"
            for item in value:
                if isinstance(item, dict):
                    html_table += "  <tr>\n"
                    for sub_key, sub_value in item.items():
                        if sub_key in rule_dict:
                            display_key = rule_dict[sub_key]
                            sub_value = "是" if sub_value is True else "否" if sub_value is False else sub_value
                            html_table += f"    <td>{display_key}: {convert_to_html(sub_value, sub_key)}</td>\n"
                    html_table += "  </tr>\n"
            html_table += "</table>\n"
            return html_table
        else:
            return "是" if value is True else "否" if value is False else value
    html_string = "<div>\n"
    for key, value in insert_dict.items():
        if key in rule_dict or (isinstance(value, list) and any(isinstance(item, dict) and any(sub_key in rule_dict for sub_key in item) for item in value)):
            html_string += f"  <p>{rule_dict.get(key, key)}: {convert_to_html(value, key)}</p>\n"
    html_string += "</div>"
    return html_string

def unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&amp;", "&")
    return s

def remove_tags(html):
    # 对 class="company-name-flag" 的标签进行处理
    soup = BeautifulSoup(html, 'html.parser')
    company_name_flag_tags = soup.find_all(lambda tag: tag.has_attr('class') and 'company-name-flag' in tag['class'])
    for tag in company_name_flag_tags:
        for tag in company_name_flag_tags:
            tag.decompose()

    remove_tags = ['path', 'svg', 'style','input']
    # 找到所有的 path 标签并移除
    for tag in remove_tags:
        path_tags = soup.find_all(tag)
        for tag in path_tags:
            tag.decompose()

    tags_with_src = soup.find_all(lambda tag: tag.has_attr('src'))
    for tag in tags_with_src:
        del tag['src']

    tags_with_src = soup.find_all(lambda tag: tag.has_attr('class'))
    for tag in tags_with_src:
        del tag['class']

    tags_with_src = soup.find_all(lambda tag: tag.has_attr('id'))
    for tag in tags_with_src:
        del tag['id']
    html = str(soup)
    html = html.replace("layui-table-link'>{{d","")
    return html


def base64_encode(data):
    # 将字符串转换为字节型数据
    data_bytes = data.encode('utf-8')
    # 进行Base64编码
    encoded_bytes = base64.b64encode(data_bytes)
    # 将字节型数据转换为字符串并返回
    encoded_data = encoded_bytes.decode('utf-8')
    return encoded_data


def base64_decode(encoded_data):
    # 将Base64编码的字符串转换为字节型数据
    encoded_bytes = encoded_data.encode('utf-8')
    # 进行Base64解码
    decoded_bytes = base64.b64decode(encoded_bytes)
    # 将解码后的字节型数据转换为字符串并返回
    decoded_data = decoded_bytes.decode('utf-8')
    return decoded_data


def identify_industry(title, content):
    keyword_map = {
        "1": ["交通", "运输", "物流", "货运", "航空", "航海", "铁路", "公路", "城市交通","汽车","航运"],
        "2": ["网络", "通讯", "计算机", "信息传输", "互联网", "数字", "IT", "电子信息", "软件", "硬件", "通信"],
        "3": ["市政", "房地产", "建筑", "城市规划", "工程", "基础设施", "房屋", "建筑材料"],
        "4": ["水利", "桥梁", "水电", "河流", "水坝", "水务", "水利工程","发电","光热","国网","电力"],
        "5": ["机械", "电子", "电器", "制造", "自动化", "仪器仪表", "设备", "装备"],
        "6": ["环保", "生态", "绿色", "节能", "可再生能源", "环境治理", "污染防治"],
        "8": ["医疗", "卫生", "健康", "医药", "医院", "药品", "医疗器械"],
        "9": ["科技", "文教", "旅游", "科学", "研究", "教育", "培训", "文化", "休闲", "旅行", "景区"],
        "10": ["冶金", "矿产", "原材料", "采矿", "金属", "矿业", "资源"],
        "11": ["出版", "印刷", "编辑", "传媒", "图书", "杂志", "报纸"],
        "12": ["轻工", "纺织", "食品", "日用品", "服装", "鞋帽", "家用电器", "食品饮料"],
        "13": ["农林", "牧渔", "种植", "养殖", "农产品", "林业", "渔业"],
        "14": ["商业", "服务", "贸易", "零售", "批发", "金融", "保险", "咨询", "广告"],
        "16": ["园林", "绿化", "园艺", "景观", "花卉", "绿地"],
        "17": ["能源", "电力", "煤炭", "石油", "天然气", "新能源",'煤矿', '煤气'],
        "18": ["化工", "化学", "材料", "涂料", "塑料", "橡胶"]
    }
    for industry_id, keywords in keyword_map.items():
        for keyword in keywords:
            if keyword in title or keyword in content:
                res = {"category_id":industry_id, "category":cate_dict[industry_id]}
                return res
    return {"category_id":"15", "category":"其它"}

def trade(categorys):
    trade = ""
    category_list = categorys.split(",")
    for category_id in category_list:
        if category_id != "":
            category = cate_dict[category_id]
            if trade:
                trade += ',' + category
            else:
                trade = category
    return trade

def extract_category(title, content,pdf_file=None):
    for x in range(5):
        try:
            if pdf_file:
                pdf_str=get_pdf_text(pdf_file)
                content=content+pdf_str
            body = {
                "title": title,
                "content": title+content,
            }
            headers = {'Content-Type': 'application/json;charset=UTF-8'}
            url = 'https://categor-extract-test-rddozbgsat.cn-beijing.fcapp.run/extract'
            response = requests.post(url=url,headers=headers, json=body,timeout=10)
            if response.status_code == 200:
                category_id = response.text
                if category_id:
                    return category_id,trade(category_id)
                else:
                    return 15,cate_dict['15']
            else:
                return 15,cate_dict['15']
        except Exception as e:
            continue
    return 15,cate_dict['15']

def get_pdf_text(response_content):
    with pdfplumber.open(BytesIO(response_content)) as pdf:
        pdf_content = ""
        for page in pdf.pages:
            text = "".join(page.extract_text())
            pdf_content += text
    return pdf_content


def trade_inv(categorys):
    trade = ""
    category_list = categorys.split(",")
    for category_id in category_list:
        if category_id == "能源电力":
            category_id = "能源"
        if category_id != "":
            if category_id in cate_inv:
                category = cate_inv[category_id]
                trade += category
            else:
                category = ""
    return trade

def filepath():
    uu = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return (uu)

# def get_response_type(response):
#     """查看文件流的类型"""
#     file_type=filetype.guess_mime(io.BytesIO(response.content))
#     if file_type:
#         return str(file_type).split('/')[-1]
#     file_type=response.headers.get('Content-Disposition')
#     if file_type:
#         file_type=file_type.split('.')[-1].replace('"', '').replace("'", '')
#         return file_type
#     return None

class IdWorker(object):
    """
     SnowFlake 算法,结合机器ID和数据中心ID,以及毫秒内序列号
    生成全局唯一ID
    """
    def __init__(self, datacenter_id, worker_id, sequence=0):
        """
        初始化
        :param datacenter_id: 数据中心(机器区域)ID
        :param worker_id: 机器ID
        :param sequence: 毫秒内序列号
        """
        # 校验数据中心ID和机器ID是否超过最大值
        if datacenter_id > MAX_DATACENTER_ID or worker_id > MAX_WORKER_ID:
            raise ValueError('数据中心ID或机器ID超过最大值')

        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        self.sequence = sequence
        self.last_timestamp = -1  # 上次计算的时间戳

    def _gen_timestamp(self):
        """
        生成整数时间戳
        :return:int timestamp
        """
        return int(time.time() * 1000)

    def get_id(self):
        """
        获取新ID
        :return:
        """
        timestamp = self._gen_timestamp()

        # 如果上次计算的时间戳与新产生的时间戳相等,在毫秒内序列号加一,为了保证在毫秒内不会产生重复
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        # 移位并通过或运算拼到一起组成64位的ID
        new_id = ((timestamp - TWEPOCH) << (WORKER_ID_BITS + DATACENTER_ID_BITS + SEQUENCE_BITS)) | \
                 (self.datacenter_id << (WORKER_ID_BITS + SEQUENCE_BITS)) | \
                 (self.worker_id << SEQUENCE_BITS) | self.sequence
        return new_id

    def _til_next_millis(self, last_timestamp):
        """
        等到下一毫秒
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp

def get_id():
    worker = IdWorker(6, 4, 0)
    return worker.get_id()


def get_response_type(response):
    """查看文件流的类型"""
    file_type = filetype.guess_mime(io.BytesIO(response.content))
    if file_type:
        return str(file_type).split('/')[-1].replace('vnd.openxmlformats-officedocument.wordprocessingml.document',
                                                     'doc') \
            .replace('vnd.ms-excel', 'xls').replace('msword', 'doc') \
            .replace('vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'xlsx').replace('x-rar-compressed', 'rar')
    file_type = response.headers.get('Content-Disposition')
    if file_type:
        file_type = file_type.split('.')[-1].replace('"', '').replace("'", '')
        return file_type
    return None


def calculate_md5(*args):
    combined_str = ''.join(map(str, args))
    print("进行md5",combined_str)
    md5_hash = hashlib.md5(combined_str.encode()).hexdigest()
    return md5_hash



def extract_area_pro(*args):
    combined_str = ''.join(map(str, args))
    combined_str = combined_str.replace("晋能控股", "山西省")
    combined_str = combined_str.replace("北京时间", "")
    area_dict = {"北京": 1, "上海": 2, "天津": 3, "重庆": 4, "河北": 5, "山西": 6, "内蒙": 7, "内蒙古": 7, "辽宁": 8,
                 "吉林": 9, "黑龙江": 10, "黑龙江省": 10, "江苏": 11, "浙江": 12, "安徽": 13, "福建": 14, "江西": 15,
                 "山东": 16, "河南": 17,
                 "湖北": 18, "湖南": 19, "广东": 20, "广西": 21, "海南": 22, "贵州": 23, "云南": 24, "西藏": 25,
                 "陕西": 26, "四川": 27,
                 "甘肃": 28, "青海": 29, "新疆": 30, "宁夏": 31, "香港": 32, "澳门": 33, "台湾": 34, "跨省": 36,
                 "亚洲": 43, "欧洲": 44, "非洲": 45, "北美洲": 46, "南美洲": 47, "大洋洲": 48, "中美洲": 49,
                 "加勒比": 50,
                 "北京市": 1, "上海市": 2, "天津市": 3, "重庆市": 4, "河北省": 5, "山西省": 6, "辽宁省": 8, "吉林省": 9,
                 "江苏省": 11, "浙江省": 12, "安徽省": 13, "福建省": 14, "江西省": 15, "山东省": 16,
                 "河南省": 17, "湖北省": 18, "湖南省": 19, "广东省": 20, "海南省": 22, "贵州省": 23, "云南省": 24,
                 "陕西省": 26, "四川省": 27, "甘肃省": 28, "青海省": 29, "香港特区": 32, "澳门特区": 33, "台湾省": 34,
                 "广西自治区": 21, "新疆自治区": 30, "宁夏自治区": 31, "西藏自治区": 25,
                 "广西壮族自治区": 21, "新疆维吾尔自治区": 30, "宁夏回族自治区": 31, "内蒙古自治区": 7}

    addr = [combined_str]
    addr_d = cpca.transform(addr)
    province = str(addr_d.iloc[0]['省'])
    if province == "None":
        result = {"area_name":"跨省", "area_id":'36'}
        return result
    else:
        result = {"area_name": province, "area_id": area_dict[province]}
        return result


def extract_area(*args):
    '''md5 提取地区'''
    combined_str = ''.join(map(str, args))
    combined_str = combined_str.replace("晋能控股","山西省")
    combined_str = combined_str.replace("北京时间","")
    addr = [combined_str]
    addr_d = cpca.transform(addr)
    province = str(addr_d.iloc[0]['省'])
    if province == "None":
        return "跨省"
    else:
        return province
def extract_pdf_text(response_content):
    try:
        with pdfplumber.open(BytesIO(response_content)) as pdf:
            pageno = 0
            pdf_content = ""
            for page in pdf.pages:
                text = "".join(page.extract_text())
                pdf_content += text
                pageno += 1
                if pageno>2:
                    break
            if "访问本页面的频率过高" in pdf_content or "分钟后再次尝试访问" in pdf_content:
                return False
            else:
                return True
    except:
        return False

def check_pdf_content(response_content, detail_url):
    try:
        # 使用BytesIO将响应内容转换为文件流
        pdf_stream = io.BytesIO(response_content)
        pdf_reader = PyPDF2.PdfReader(pdf_stream)
        total_pages = len(pdf_reader.pages)
        page_number = 0  # 要读取的页面数，从0开始计数
        page = pdf_reader.pages[page_number] # 获取指定页面的Page对象
        text = str(page.extract_text())  # 提取页面的文本内容
        text = "".join(text)
        if "访问本页面的频率过高" in text or "分钟后再次尝试访问" in text:
            logger.error("附件中1：访问本页面的频率过高")
            return False
        if not extract_pdf_text(response_content):
            logger.error("附件中2：访问本页面的频率过高")
            return False
        else:
            return True
    except Exception as e:
        logger.error(f"PyPDF2错误{e}")
        try:
            pdf = pikepdf.Pdf.open(pdf_stream)
        except Exception as e:
            logger.error(f"pikepdf错误{e}")
            try:
                pdf_reader = pypdf.PdfReader(pdf_stream)
            except Exception as e:
                logger.error("附件中2：访问本页面的频率过高")
                return False
            else:
                return True
        else:
            return True

class dc_des:
    def __init__(self, DES_KEY):
        self.des_obj = des(DES_KEY, ECB, DES_KEY, padmode=PAD_PKCS5)  # 初始化一个des对象，参数是秘钥，加密方式，偏移， 填充方式
        self.des_obj.setKey(DES_KEY)  # 自定义key，位数不限

    def encrypt(self, obj):
        des_obj = self.des_obj
        secret_bytes = des_obj.encrypt(obj)  # 用对象的encrypt方法加密
        return base64.b64encode(secret_bytes).decode()

    def decrypt(self, secret_bytes):
        des_obj = self.des_obj
        secret_bytes = base64.b64decode(secret_bytes)  # 这里中文要转成字节
        obj = des_obj.decrypt(secret_bytes)  # 用对象的decrypt方法解密
        return obj.decode()

# 时间处理函数
class Util(object):
    def __init__(self):
        pass
    @staticmethod
    def formate_date(str):
        '''
        时间格式化，替换年月日
        '''
        if str[-1] == '日':
            str = str.replace('日', '')
        str = str.replace('年', '-').replace('月', '-').replace('\r', '').replace('\n', '').replace('\t', '').replace(
            u'\xa0', '').replace('&nbsp;', '')
        return str

    @staticmethod
    def sjc_formate(shijian, ms='ms'):
        '''
        时间戳转时间
        '''
        shijian = int(shijian)
        if len(str(shijian)) == 13:
            shijian = time.localtime(float(shijian / 1000))
            shijian = time.strftime("%Y-%m-%d %H:%M:%S", shijian)
        elif len(str(shijian)) == 10:
            shijian = time.localtime(float(shijian))
            shijian = time.strftime("%Y-%m-%d %H:%M:%S", shijian)
        return shijian

    @staticmethod
    def rep_space(str_s):
        str_res = "".join(str_s.split())
        str_res = str_res.strip().replace('\'', '"').replace('\r', '').replace('\n', '').replace('\t', '').replace(' ',
                                   '').replace(
            u'\xa0', '').replace(u'\s', '')
        return str_res

    @staticmethod
    def remove_empty_tag(input):
        # 删除空标签
        # input=input.replace('<td></td>','<td>&nbsp;</td>').replace('<th></th>','<th>&nbsp;</th>')
        # pattern = re.compile(r'<([a-z]+\d?)\b[^>]*>(&nbsp;&nbsp;|[\s　])*</\1>',re.IGNORECASE)
        pattern = re.compile(r'<(?!td|th|iframe)([a-z]+\d?)\b[^>]*>(&nbsp;|[\s　])*</\1>', re.IGNORECASE)
        maxLoopTimes = 10
        i = 0
        while i < maxLoopTimes:
            tem = pattern.sub('', input)
            if tem == input:
                input = tem
                break
            else:
                input = tem
            i += 1
        return input

    @staticmethod
    def remove_Allhtml(html):
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', html)
        return dd

    @staticmethod
    def remove_Allhtml_kongge(html):
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub(' ', html)
        return dd

    @staticmethod
    def format_date(content):
        pattern = r'(20\d{2})-(\d{1,2})-(\d{1,2})'
        # 示例:[2020-07-28]
        m = bool(re.search(pattern, content))
        if m:
            # 如果匹配到格式 [2020-07-28]
            result = list(re.findall(pattern, content)[0])
            # 如果月日是个位数,前面补0
            for a in range(1, 3):
                if len(result[a]) == 1:
                    result[a] = '0' + result[a]
            result_str = '-'.join(result)
            return result_str

        pattern = r'(20\d{2})\.(\d{1,2})\.(\d{1,2})'
        # 示例:[2020.07.28]
        m = bool(re.search(pattern, content))
        if m:
            result = list(re.findall(pattern, content)[0])
            for a in range(1, 3):
                if len(result[a]) == 1:
                    result[a] = '0' + result[a]

            result_str = '.'.join(result)
            return result_str

        # 匹配格式 [2020年07月28日]
        pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
        m = bool(re.search(pattern, content))
        if m:
            result = list(re.findall(pattern, content)[0])
            for a in range(1, 2):
                if len(result[a]) == 1:
                    result[a] = '0' + result[a]
            result_str = '-'.join(result)
            return result_str

        # 匹配格式 [20年07月28日]
        pattern = r'(\d{2})年(\d{1,2})月(\d{1,2})日'
        m = bool(re.search(pattern, content))
        if m:
            result = list(re.findall(pattern, content)[0])
            for a in range(1, 2):
                if len(result[a]) == 1:
                    result[a] = '0' + result[a]

            result_str = "20" + '-'.join(result[1:])
            return result_str

        # 匹配格式 [07月28日]
        pattern = r'(\d{1,2})月(\d{1,2})日'
        m = bool(re.search(pattern, content))
        if m:
            result = list(re.findall(pattern, content)[0])
            for a in range(0, 2):
                if len(result[a]) == 1:
                    result[a] = '0' + result[a]

            result_str = '2021-' + '-'.join(result)
            return result_str

        # 匹配格式 [10-28-20]
        pattern = r'(\d{1,2})-(\d{1,2})-(\d{1,2})'
        m = bool(re.search(pattern, content))
        if m:
            result = list(re.findall(pattern, content)[0])
            for a in range(0, 2):
                if len(result[a]) == 1:
                    result[a] = '0' + result[a]
            result_str = '20' + '-'.join(result)
            return result_str

        # 匹配格式 [20200909]
        pattern = r'(\d{8})'
        m = bool(re.search(pattern, content))
        if m:
            result = re.findall(pattern, content)[0]
            year = result[0:4]
            month = result[4:6]
            day = result[6:8]
            result_str = f"{year}-{month}-{day}"
            return result_str
    @staticmethod
    def remove_other(content):
        re_extract = 'style="(.*?)"|<script(.*?)</script>|class="(.*?)"|<!--header-->|<divid="headPart">'
        rs = re.sub(re_extract, " ", content)
        return rs


def my_pad(text, pad_type='pkcs7', block_size=16):
    if text is None or type(text) != str:
        return None
    result = None
    text_len = len(text)
    if pad_type == 'pkcs7':
        pad_len = block_size - text_len % block_size;
        result = text + pad_len * chr(pad_len)
    elif pad_type == 'zero':
        if text_len % block_size != 0:
            result = text + (block_size - text_len % block_size) * chr(0)
        else:
            result = text

    return result


def my_unpad(text, pad_type='pkcs7'):
    if text is None or type(text) != str:
        return None
    result = None
    text_len = len(text)
    pad_len = 0
    if pad_type == 'pkcs7':
        pad_len = ord(text[-1])
    elif pad_type == 'zero':
        for i in range(text_len):
            if ord(text[-1 - i]) != 0:
                break
            pad_len += 1
    return text[:0 - pad_len]

def make_base64(data, coding='utf8'):
    if type(data) == str:
        temp = data.encode(coding)
    else:
        temp = data
    return base64.encodebytes(temp).decode(coding)


def parse_base64(data, coding='utf8'):
    if type(data) == str:
        temp = data.encode(coding)
    else:
        temp = data
    return base64.decodebytes(temp).decode(coding)

def rsa_encrypt(pkey, data, length=50):
    key = '-----BEGIN PUBLIC KEY-----\n' + pkey + '\n-----END PUBLIC KEY-----'
    pub_key = RSA.importKey(str(key))
    cipher = PKCS1_cipher.new(pub_key)
    data = data.encode()
    if len(data) <= length:
        result = base64.b64encode(cipher.encrypt(data))
    else:
        rsa_text = b""
        for i in range(0, len(data), length):
            cont = data[i:i + length]
            rsa_text += cipher.encrypt(cont)

        result = base64.b64encode(bytes.fromhex(rsa_text.hex()))
    return result.decode()

def rsa_decrypt(pkey, encrypt_text):
    key = '-----BEGIN PUBLIC KEY-----\n' + pkey + '\n-----END PUBLIC KEY-----'
    random_generator=Random.new().read
    rsa_key = RSA.importKey(key)
    cipher = PKCS1_cipher.new(rsa_key)
    text = cipher.decrypt(base64.b64decode(encrypt_text), random_generator)
    return text.decode('utf-8')
def encrypt_aes(key, text, text_pad_type='pkcs7', key_pad_type='zero', mode='ECB', iv=None):
    if mode == 'ECB':
        cipher = AES.new(my_pad(key, key_pad_type).encode(), AES.MODE_ECB)
    elif mode == 'CBC':
        cipher = AES.new(my_pad(key, key_pad_type).encode(), AES.MODE_CBC, iv=iv.encode('utf-8'))
    else:
        return None
    result = make_base64(cipher.encrypt(my_pad(text).encode()))
    return result


def decrypt_aes(key, text, text_pad_type='pkcs7', key_pad_type='zero', mode='ECB', iv=None):
    if mode == 'ECB':
        cipher = AES.new(my_pad(key, key_pad_type).encode(), AES.MODE_ECB)
    elif mode == 'CBC':
        cipher = AES.new(my_pad(key, key_pad_type).encode(), AES.MODE_CBC, iv=iv.encode('utf-8'))
    else:
        return None
    result = my_unpad(cipher.decrypt(base64.decodebytes(text.encode())).decode(), text_pad_type)
    return result


def decrypt_des(key, text, text_pad_type='pkcs7', key_pad_type='zero', mode='ECB', key_size=8):
    if key_size:
        if len(key) < key_size:
            raise '长度不对'
        key = key[:key_size]
    if mode == 'ECB':
        cipher = DES.new(key.encode(), DES.MODE_ECB)
    elif mode == 'CBC':
        cipher = DES.new(my_pad(key, key_pad_type, 8).encode(), DES.MODE_CBC)
    else:
        return None
    result = my_unpad(cipher.decrypt(base64.decodebytes(text.encode())).decode(), text_pad_type)
    return result

def parse_click_image(image_file_name=None, image64=None, rotate=12):
    if image64 is not None:
        image = cv2.imdecode(np.fromstring(base64.b64decode(image64), np.uint8), cv2.IMREAD_COLOR)
    else:
        image = cv2.imread(image_file_name)
    det = ddddocr.DdddOcr(det=True, show_ad=False)
    ocr = ddddocr.DdddOcr(old=True, show_ad=False)
    buf = BytesIO()
    Image.fromarray(image).save(buf, format='PNG')
    poses = det.detection(buf.getvalue())
    result = {}
    result['shape'] = image.shape
    for box in poses:
        sub = image[box[1] - 5:box[3] + 5, box[0] - 5:box[2] + 5]
        height, width = sub.shape[:2]
        center = (width / 2, height / 2)
        for i in range(rotate):
            rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=i * (360 / rotate), scale=1)
            rotated_image = cv2.warpAffine(src=sub, M=rotate_matrix, dsize=(width, height))
            res = ocr.classification(Image.fromarray(rotated_image))
            if len(res) > 0 and res not in result:
                result[res] = box
    return result

# 清理html 中无用熟悉、空格、样式、脚本
def clean_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    # 去除所有样式
    for style in soup.find_all('style'):
        style.decompose()

    # 去除所有脚本
    for script in soup.find_all('script'):
        script.decompose()

    # 去除所有注释
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    # 去除所有空白字符和空白行
    for tag in soup.findAll():
        if tag.string:
            tag.string = tag.string.strip()

    # 去除多余的标签
    for tag in soup.findAll():
        if not tag.contents:
            tag.extract()

    # 去除HTML实体编码
    soup = BeautifulSoup(re.sub(r'&\w+?;', convert_entities, str(soup)), 'html.parser')
    # 保留 src 和 href 属性，去除其他属性
    for tag in soup.find_all():
        attrs_to_keep = ['src', 'href']
        tag.attrs = {k: v for k, v in tag.attrs.items() if k in attrs_to_keep}

    return str(soup)

def convert_entities(match):
    entity = match.group()
    if entity == '&lt;':
        return '<'
    elif entity == '&gt;':
        return '>'
    elif entity == '&amp;':
        return '&'
    elif entity == '&quot;':
        return '"'
    elif entity == '&apos;':
        return "'"
    else:
        return entity





class TimeCheckError(Exception):

    def __init__(self, *args):
        super(TimeCheckError, self).__init__(*args)


def check_time(string, time_format="%Y-%m-%d %H:%M:%S"):
    if not string:
        return ''
    if isinstance(string, (int, float)):
        string = str(int(string))
    if not isinstance(string, str):
        raise TimeCheckError(f"时间格式化失败 {str(string)}")
    if string.isdigit():
        if len(string) == 13:
            return time.strftime(time_format, time.localtime(int(string) / 1000))
        elif len(string) == 10:
            return time.strftime(time_format, time.localtime(int(string)))
        else:
            raise TimeCheckError(f"时间格式化失败 {str(string)}")
    string = string.strip()
    if '年' in string and '月' in string and '日' in string:
        string = string.split("日")[0]
        if "年" in time_format or '月' in time_format or '日' in time_format:
            t_format = time_format
        else:
            t_format = "%Y年%m月%d"
        try:
            d = datetime.datetime.strptime(string, t_format)
        except Exception as e:
            raise TimeCheckError(f"时间格式化失败 {string} -- {str(e)}")
    elif '年' in string and '月' in string:
        string = string.split(" ")[0]
        if "年" in time_format or '月' in time_format:
            t_format = time_format
        else:
            t_format = "%Y年%m月%d"
        try:
            d = datetime.datetime.strptime(string, t_format)
        except Exception as e:
            raise TimeCheckError(f"时间格式化失败 {string} -- {str(e)}")
    else:
        try:
            d = date_string_parser.parse(string)
        except Exception as e:
            raise TimeCheckError(f"时间格式化失败 {string} {str(e)}")
    if d.tzinfo:
        d = d.replace(tzinfo=None)
    try:
        n_year_later = datetime.datetime.now().replace(year=datetime.datetime.now().year + 1)
        if d > n_year_later:
            raise TimeCheckError(f"格式化后时间大于一年后时间 {str(d)}")
    except Exception as e:
        if 'day is out of range for month' in str(e):
            pass
        if '格式化后时间大于一年后时间' in str(e):
            raise TimeCheckError(f"格式化后时间大于一年后时间 {str(d)}")
    return d.strftime(time_format)


def comparison_time(pub_date: [str, int], stop_pub_date: str) -> bool:
    """
    对比发布时间，
    """
    format_pub_date = check_time(pub_date)
    format_stop_pub_date = check_time(stop_pub_date)
    if format_pub_date < format_stop_pub_date:
        print(f'发布时间小于{format_stop_pub_date}')
        return False
    else:
        return True


def check_word_title(title: str, words=None) -> bool:
    """
    标题中包含这些词语，才会进行采集
    """
    word_list = ["更正", "单一来源", "中选", "招标", "成交", "验收", "中标", "采购", "候选人", "遴选", "询价", "议价", "竞争性谈判", "竞价", "合同", "采购意向",
                 "结果", "寻源", "磋商", "供应商招募", "招募", "征集", "招商项目", "招租", "招标文件预公示", "招商文件发售公告", "答疑", "澄清", "采购计划", "招采公告",
                 "产权交易", "竞投", "拍卖", "流标公告", "终止公告", "暂停公告", "二次", "二次公告", "采购意向", "废标公告", "补遗", "失败公告", "比选"]
    if words:
        word_list += words
    for word in word_list:
        if word in title:
            return True
    return False

def check_title_for_keywords(insert_s):
    title = insert_s['title'] + insert_s["classd_name"]
    """
    判断栏目类型
    """
    keywords = ["中标", "成交", "结果", "流标", "废标", "合同"]
    for keyword in keywords:
        if keyword in title:
            return "ZBGS"
    return "ZBGG"

def replace_word_content(content: str,words=None) -> str:
    """
    替换正文的文本
    """
    word_list = [
        "中国招标与采购网",
        "招标采购导航网",
        "中国采购招标网",
        "中国招标采购网",
        "千里马招标网",
        "中国采招网",
        "中国招标网",
        "中国电力招标采购网",
        "www.chinabidding.cc",
        "www.bidchance.com",
        "www.dlztb.com",
        "中机采招网",
        "qianlima",
        "https://user.zhaobiao.cn/login.html",
        "https://www.bidcenter.com.cn",
        "https://www.infobidding.com",
        "https://www.okcis.cn",
        "http://www.chinazbcg.com/index.action",
    ]
    if words:
        word_list+=words
    for word in word_list:
        content = content.replace(word, '')
    return content

def insertd(data1):
    data1["classd_id"] = "二手"
    insert_s = copy.deepcopy(data1)
    if not insert_s.get("table_name",False):
        insert_s["table_name"] = "ZBXX"
    if len(insert_s.get("table_name2",""))<3:
        insert_s['table_name2'] = check_title_for_keywords(insert_s)
    insert_s['description'] = replace_word_content(insert_s.get('description',""))
    insert_s["original_id"] = get_id()
    insert_s["area"] = extract_area_pro(insert_s["title"], insert_s["description"])["area_name"]
    insert_s["area_id"] = extract_area_pro(insert_s["title"], insert_s["description"])["area_id"]
    insert_s["category"] = identify_industry(insert_s["title"], insert_s["description"])["category"]
    insert_s["category_id"] = identify_industry(insert_s["title"], insert_s["description"])["category_id"]
    return insert_s

def formate_insertd(data1,title):
    content_to_add = f'<br><a href="{data1["comments"]}">点击查看原文</a>'
    data1["description"] = data1["description"] + content_to_add
    s_data = copy.deepcopy(data1)
    if len(s_data['description']) < 20:
        logger.error(f"内容字段长度异常，低于20个字符:{s_data['description']}")
        raise "内容字段长度异常，低于20个字符"
    if len(s_data['title']) > 100:
        s_data['title'] = s_data['title'][:100] + "..."
        s_data['description'] = f"<h2>{title}</h2" + s_data['description']
    md5_hash = hashlib.md5()
    md5_hash.update(s_data['comments'].encode('utf-8'))
    md5_digest = md5_hash.hexdigest()
    s_data['content'] = ""
    s_data['source'] = '2'
    s_data['main_host'] = urlparse(s_data['comments']).netloc
    s_data['deduct_md5'] = md5_digest
    s_data['description'] = base64_encode(s_data['description'])
    s_data['title'] = base64_encode(s_data['title'])
    s_data['comments'] = base64_encode(s_data['comments'])
    try:
        s_data['files'] = base64_encode(json.dumps(s_data['files']))
    except:
        s_data['files'] = base64_encode(json.dumps([]))
    s_data['classd_name'] = s_data["classd_name"]+"(pyspider)"
    return s_data

def relative_url_replace(page_url, html_content):
    base_url = urlparse(page_url)
    base_url = f"{base_url.scheme}://{base_url.netloc}"
    soup = BeautifulSoup(html_content, 'html.parser')
    prettified_html = soup.prettify()
    soup = BeautifulSoup(prettified_html, 'html.parser')
    for tag in soup.find_all(['img', 'a', 'link', 'script', 'source']):
        attr_name = None
        for attr in ['src', 'href', 'url']:
            if attr in tag.attrs:
                attr_name = attr
                break
        if attr_name:
            url = tag[attr_name]
            if len(url) >= 3 and 'http' not in url:
                full_url = urljoin(base_url, url)
                tag[attr_name] = full_url
    return str(soup)

