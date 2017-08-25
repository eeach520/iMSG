from urllib import request
import json
import datetime
from app.models import Wechat
from .read_json import Read_Json
from .save_message import Save_Message
from .config import WECHAT, ERROR


class Send_Wechat(Read_Json, Save_Message):
    def __init__(self, send_data, to_user):
        self.__data = send_data
        self.__to_user = to_user
        self.__access_token = None
        self.__appid = WECHAT.APPID
        self.__secret = WECHAT.APPSECRET
        self.__content = None
        self.get_data_of_message()

    def get_data_of_message(self):
        self.__content = self.__data['content']
        if isinstance(self.__to_user, list):
            self.generate_access__token(True)
        else:
            self.generate_access__token()

    def generate_access__token(self, opid_list=False):
        url = WECHAT.TOKEN_URL + '&appid=' + self.__appid + '&secret=' + self.__secret
        access_token = request.Request(url)
        self.__access_token = json.loads(request.urlopen(access_token).read())['access_token']
        if opid_list:
            judge = True
            for item in self.__to_user:
                request_answer = self.send_message(item)
                if request_answer['errcode'] != 0:
                    super().add_response_wechat('details',
                                                {Wechat.query.filter_by(openID=item).first().nickname: request_answer})
                    judge = False
                else:
                    super().add_response_wechat('details', {Wechat.query.filter_by(openID=item).first().nickname: ERROR[0]})
            if judge:
                super().set_response(ERROR[0])
            else:
                super().set_response(ERROR[16])
        else:
            request_answer = self.send_message(self.__to_user)
            if request_answer['errcode'] == 0:
                super().set_response(ERROR[0])
            elif request_answer['errcode'] == 40003:
                super().set_response(ERROR[15])
            elif request_answer['errcode'] == 43004:
                super().set_response(ERROR[14])
            else:
                super().set_response(ERROR[12])

    def send_message(self, to_user):
        text_mod = {'touser': to_user, 'template_id': 'x6fR7lSwNb_TMGwLbKLNR8m3aDVncm1pK_CvfUoXtiw',
                    'url': 'http://www.tcxa.com.cn/',
                    'data': {'welcome': {'value': u'欢迎使用iMSG平台', 'color': '#173177'},
                             'from': {'value': u'iMSG平台', 'color': '#173177'},
                             'iptable': {'value': self.__data['ip'], 'color': '#173177'},
                             'message': {'value': self.__content, 'color': '#173177'},
                             'time': {'value': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                      'color': '#173177'},
                             'attach': {'value': u'欢迎继续使用iMSG平台', 'color': '#173177'}}}
        text_mod = json.dumps(text_mod, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        url = WECHAT.MESSAGE_URL + self.__access_token
        req = request.Request(url=url, data=text_mod)
        res = json.loads(request.urlopen(req).read())
        print(res)
        if res['errcode'] == 0:
            Save_Message.__init__(self, self.__data['ip'], to_user, 'wechat', True,
                                  str(self.__data['content']), 'OK')
            Save_Message.add_message(self)
        else:
            Save_Message.__init__(self, self.__data['ip'], to_user, 'wechat', False,
                                  str(self.__data['content']), res['errmsg'])
            Save_Message.add_message(self)
        return res
