from DrissionPage import ChromiumPage, ChromiumOptions
from flask import Flask, request
import json
import time
import datetime

app = Flask(__name__)
co = ChromiumOptions()
co.set_pref('credentials_enable_service', False)
co.set_argument('--hide-crash-restore-bubble')
co.no_imgs(True)
# if param['parameters']['proxy']:
#     co.add_extension(f'../extension/{param["port"]}')
#     self.log.info('插件增加完毕')
# if param.get('user'):
#     co.set_user_data_path(param.get('user_path'))
co.set_address(f'127.0.0.1:25556')
# if self.config.get('user_path'):
#     co.set_user_data_path(self.config.get('user_path'))
#     self.log.info('用户信息加载完毕')
page = ChromiumPage(co)

@app.route('/pyspider', methods=['POST', 'GET'])
def handle_post():
    if request.method == 'GET':
        body = "method not allowed!"
        headers = {
            'Cache': 'no-cache',
            'Content-Length': len(body)
        }
        return body, 403, headers
    else:
        start_time = datetime.datetime.now()
        raw_data = request.get_data()
        # fetch = {'method': 'GET', 'headers': {'User-Agent': 'pyspider/0.4.0 (+http://pyspider.org/)'}, 'use_gzip': True,
        #          'connect_timeout': 20,
        #          'url': 'https://www.obei.com.cn/obei-web-ec-ego/ego/rfq/deploy/egoBusinessOpportunity.html#/id=c5904bfd81d54496952b583eaa4b34e2/rfqMethod=RAQ/orgCode=E31378700/statusFlag=0',
        #          'request_timeout': 120, 'fetch_type': 'phantomjs'}
        fetch = json.loads(raw_data, encoding='utf-8')
        fetch_url = fetch['url']
        result = {'orig_url': fetch_url,
                  'status_code': 200,
                  'error': '',
                  'content': '',
                  'headers': {},
                  'url': '',
                  'cookies': {},
                  'time': 0,
                  'js_script_result': '',
                  'save': '' if fetch.get('save') is None else fetch.get('save')
                  }
        try:
            page.set.cookies.clear()
            page.clear_cache()
            page.get(url=fetch_url, retry=3, interval=1, timeout=5)
            result['url'] = page.url
            result['content'] = page.html
            result['cookies'] = _parse_cookie(page.cookies)
        except Exception as e:
            import traceback
            traceback.print_exc()
            result['error'] = str(e)
            result['status_code'] = 599

        end_time = datetime.datetime.now()
        result['time'] = (end_time - start_time).seconds

        # print('result=', result)
        return json.dumps(result), 200, {
            'Cache': 'no-cache',
            'Content-Type': 'application/json',
        }

#
# def _parse_cookie(cookie_list):
#     print("cookie_list", cookie_list)
#     if cookie_list:
#         cookie_dict = dict()
#         for item in cookie_list:
#             cookie_dict[item['name']] = item['value']
#         return cookie_dict
#     return {}

def _parse_cookie(cookie_str):
    print("cookie_str", cookie_str, "\n")
    # print(type(cookie_str))
    # if cookie_str:
    #     cookie_list = [
    #         {
    #             "name": pair.split("=")[0].strip(),
    #             "value": pair.split("=")[1].strip() if "=" in pair else None,
    #         }
    #         for pair in cookie_str.split(";")
    #     ]
    #     cookie_dict = dict()
    #     for item in cookie_list:
    #         cookie_dict[item["name"]] = item["value"]
    #     return cookie_dict
    return cookie_str

class InitWebDriver(object):
    _web_driver = None
    isFirst = True

    @staticmethod
    def _init_web_driver(fetch):
        if InitWebDriver._web_driver is None:
            co = ChromiumOptions()
            co.set_pref('credentials_enable_service', False)
            co.set_argument('--hide-crash-restore-bubble')
            co.no_imgs(True)
            InitWebDriver._web_driver = ChromiumPage(co)

    @staticmethod
    def get_web_driver(fetch):
        if InitWebDriver._web_driver is None:
            InitWebDriver._init_web_driver(fetch)
        return InitWebDriver._web_driver

    @staticmethod
    def init_extra(fetch):
        # maybe throw TimeOutException
        driver = InitWebDriver._web_driver
        if fetch.get('timeout'):
            driver.set_page_load_timeout(fetch.get('timeout'))
            driver.set_script_timeout(fetch.get('timeout'))
        else:
            driver.set_page_load_timeout(20)
            driver.set_script_timeout(20)

    @staticmethod
    def quit_web_driver():
        if InitWebDriver._web_driver is not None:
            InitWebDriver._web_driver.quit()


if __name__ == '__main__':
    app.run('0.0.0.0', 22225, debug=True)
    InitWebDriver.quit_web_driver()