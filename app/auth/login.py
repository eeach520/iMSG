# -*- coding: utf-8 -*-
import time, secrets, base64, hmac, uuid
from flask_login import login_user
from werkzeug.security import check_password_hash
from .. import db
from ..models import User, Token
from ..read_json import Json_Data


class Login_User(Json_Data):
    def __init__(self, json_data):
        super(Login_User, self).__init__(json_data)
        self.__data = super().get_data()
        self.username = None
        self.password = None
        self.get_username_and_password()
        self.verify_username_and_password()
        self.get_token_and_save()

    def get_username_and_password(self):
        if 'username' in self.__data.keys() and 'password' in self.__data.keys():
            self.username = self.__data['username']
            self.password = self.__data['password']
        else:
            super().set_response('error', u'未包含用户名和密码')

    def verify_username_and_password(self):
        __user = User.query.filter_by(name=self.username).first()
        if __user is not None:
            if check_password_hash(__user.password, self.password):
                login_user(__user)
                super().set_response('success', True)
            else:
                super().set_response('error', u'密码错误')
        else:
            super().set_response('error', u'用户不存在')

    def generate_token(self, key, message, expire=3000):
        ts_str = str(time.time() + expire)
        sha1_str = hmac.new(key.encode('utf-8'), ts_str.encode('utf-8'), 'sha1').hexdigest()
        random_token = secrets.token_hex(16)
        token = random_token + ':' + ts_str + ':' + message + ':' + sha1_str
        base64_token = base64.urlsafe_b64encode(token.encode('utf-8')).decode('utf-8')
        return base64_token

    def get_token_and_save(self):
        if super().get_response_for_key('success') is True:
            token = self.generate_token(str(uuid.uuid1()), self.username)
            db_token = Token(token=token)
            db.session.add(db_token)
            db.session.commit()
            super().set_response('token', token)
