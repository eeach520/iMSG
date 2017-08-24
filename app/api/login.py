# -*- coding: utf-8 -*-
import time
import hmac
import uuid
import base64
import datetime
import secrets
from .. import db
from .config import ERROR
from ..models import User, Token
from .read_json import Read_Json
from werkzeug.security import check_password_hash


def generate_token(key, message, expire=3000):
    ts_str = str(time.time() + expire)
    sha1_str = hmac.new(key.encode(), ts_str.encode(), 'sha1').hexdigest()
    random_token = secrets.token_hex(16)
    token = random_token + ':' + ts_str + ':' + message + ':' + sha1_str
    base64_token = base64.urlsafe_b64encode(token.encode()).decode()
    return base64_token


class Login(Read_Json):
    def __init__(self, json_data):
        super(Login, self).__init__(json_data)
        self.__data = super().get_data()
        self.__username = None
        self.__password = None
        self.get_username_and_password()
        self.delete_old_token()

    def get_username_and_password(self):
        if 'username' in self.__data.keys() and 'password' in self.__data.keys():
            self.__username = self.__data['username']
            self.__password = self.__data['password']
            self.verify_username_and_password()
        else:
            super().set_response(ERROR[2])

    def verify_username_and_password(self):
        __user = User.query.filter_by(username=self.__username).first()
        if __user is not None:
            if check_password_hash(__user.password, self.__password):
                self.get_token_and_save()
                super().set_response(ERROR[0])
            else:
                super().set_response(ERROR[7])
        else:
            super().set_response(ERROR[6])

    def get_token_and_save(self):
        token = generate_token(str(uuid.uuid1()), self.__username)
        db_token = Token(token=token)
        db.session.add(db_token)
        db.session.commit()
        super().add_response('token', token)

    def delete_old_token(self):
        now = datetime.datetime.now()
        old_time = (now + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        old_token = Token.query.filter(Token.generate_time > str(old_time)).all()
        if old_token:
            for item in old_token:
                db.session.delete(item)
                db.session.commit()
