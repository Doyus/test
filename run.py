#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
import click
from click.testing import CliRunner
from pyspider.run import main
import os
import requests,time
# if __name__ == '__main__':
#     main()

def ping_check():
    try:
        requests.get('http://192.168.36.163',timeout=(1,2))
        print("服务器环境")
        return False
    except Exception as e:
        print("开发环境")
        return True

APP_DEBUG = ping_check()
pyspider_path = "./"

if __name__ == "__main__":
    if APP_DEBUG:
        # conf_file = os.path.join(pyspider_path, 'conf_dev.json')
        # os.system(f'python {pyspider_path}/run.py -c {conf_file}')
        runner = CliRunner()
        result = runner.invoke(main(), ['-c', 'conf_test.json'])
        if result.exception:
            print(result.exception)
        else:
            print(result.output)
    else:
        main()