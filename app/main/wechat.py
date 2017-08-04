from urllib import request, parse
import json, time
from .. import db
from ..read_json import Json_Data
from ..models import Wechat_user, Temp_token


class Send_Wechat(Json_Data):
    def __init__(self, send_data):
        self.__data = send_data
        self.__access_token = None
        self.__appid = 'wxfeee112304c755ea'
        self.__secret = '6c19249d9fa4074bd9207dc1269fac5c'
        self.__touser = None
        self.__content = None
        self.get_data_of_message()
        self.send_message()

    def get_data_of_message(self):
        if 'nickname' in self.__data.keys() and 'content' in self.__data.keys():
            touser = Wechat_user.query.filter_by(nickname=self.__data['nickname']).first()
            if touser is None:
                super().set_response('error', u'微信公众号无此用户')
            else:
                self.__content = self.__data['content']
                self.__touser = touser.openID
        else:
            super().set_response('error', u'未包含有效字段（微信发邮件应包括“nickname（用户昵称）”和“content（发送内容）”字段）')

    def generate_access__token(self):
        grant_type = 'client_credential'
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=' + grant_type + '&' + \
              'appid=' + self.__appid + '&' + 'secret=' + self.__secret
        access_token = request.Request(url)
        access_token = json.loads(request.urlopen(access_token).read())
        temp_token = Temp_token(id=1, temp_access_token=access_token['access_token'])
        db.session.add(temp_token)
        db.session.commit()

    def read_token(self):
        temp_token = Temp_token.query.filter_by(id=1).first()
        if temp_token is not None:
            self.__access_token = temp_token.temp_access_token

    def send_message(self):
        if self.__touser is not None:
            self.read_token()
            if self.__access_token is None:
                self.generate_access__token()
                self.send_message()
            else:
                print(self.__access_token)
                text_mod = {"touser": self.__touser, "msgtype": "text", "text": {"content": self.__content}}
                text_mod = json.dumps(text_mod, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
                url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=" + self.__access_token
                req = request.Request(url=url, data=text_mod)
                res = json.loads(request.urlopen(req).read())
                if res['errcode'] == 0:
                    super().set_response('success', True)
                    super().set_response('发送时间', time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()))
                elif res['errcode'] == 42001:
                    old_token = Temp_token.query.filter_by(id=1).first()
                    db.session.delete(old_token)
                    db.session.commit()
                    self.generate_access__token()
                    self.send_message()
                else:
                    super().set_response('error', res['errmsg'])
