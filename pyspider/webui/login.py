#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<roy@binux.me>
#         http://binux.me
# Created on 2014-12-10 20:36:27

import base64
from flask import Response
try:
    import flask_login as login
except ImportError:
    from flask.ext import login
from .app import app
import mysql.connector
import datetime
from pyspider.mytools.myconfs import APP_DEBUGE
login_manager = login.LoginManager()
login_manager.init_app(app)


class AnonymousUser(login.AnonymousUserMixin):

    def is_anonymous(self):
        return True

    def is_active(self):
        return False

    def is_authenticated(self):
        return False

    def get_id(self):
        return


class User(login.UserMixin):

    def __init__(self, id, password):
        if not APP_DEBUGE:
            self.id = id
            self.password = password
            self.database_name = "spider"
            user = "spider"
            passwd = "1b6bd97f1922791DD"
            host = "rm-2zeiqj4rqux185icj.rwlb.rds.aliyuncs.com"
            port = 3306
            self.conn = mysql.connector.connect(user=user, password=passwd, host=host, port=port, autocommit=True)
            self.conn.database = self.database_name
            self.expiration_date = datetime.datetime.now() + datetime.timedelta(hours=200)  # 设置1小时的有效期
        else:
            self.id = id
            self.password = password
            self.database_name = "pyspider"
            user = "root"
            passwd = "pspwd456"
            host = "8.141.1.85"
            port = 3307
            self.conn = mysql.connector.connect(user=user, password=passwd, host=host, port=port, autocommit=True)
            self.conn.database = self.database_name
            self.expiration_date = datetime.datetime.now() + datetime.timedelta(hours=200)  # 设置1小时的有效期


    def execute_sql(self, query, params=None):
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(f"Error executing SQL query: {error}")
            return None

    def is_authenticated(self):
        query = "SELECT * FROM user_table WHERE username = %s AND password = %s"
        params = (self.id, self.password)
        app.config['webui_username'] = self.id
        app.config['webui_password'] = self.password
        result = self.execute_sql(query, params)
        # 检查API密钥是否在有效期内
        # if result and datetime.datetime.now() < self.expiration_date:
        #     return True
        # else:
        #     return False
        return bool(result)

    def is_active(self):
        return self.is_authenticated()



login_manager.anonymous_user = AnonymousUser


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key[len("Basic "):]
        try:
            api_key = base64.b64decode(api_key).decode('utf8')
            return User(*api_key.split(":", 1))
        except Exception as e:
            app.logger.error('wrong api key: %r, %r', api_key, e)
            return None
    return None
app.login_response = Response(
    "need auth.", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}
)


@app.before_request
def before_request():
    if app.config.get('need_auth', False):
        if not login.current_user.is_active():
            return app.login_response
