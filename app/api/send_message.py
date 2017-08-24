import re
from .smtp import Send_Mail
from .read_json import Read_Json
from .token_verify import Token_Verify
from ..models import Wechat
from .sms import Send_Sms
from .message_control import Message_Control
from .save_message import Save_Message
from .register import judge_dict
from .config import ERROR
from .wechat import Send_Wechat


class Send_Message(Send_Wechat, Send_Sms, Send_Mail, Read_Json, Save_Message, Token_Verify):
    def __init__(self, send_data, ip):
        Read_Json.__init__(self, send_data)
        self.__data = Read_Json.get_data(self)
        self.__to_user = None
        if self.__data:
            self.__data['ip'] = ip
            self.verify_token()
            self.message_controling()

    def verify_token(self):
        if 'token' in self.__data:
            Token_Verify.__init__(self, self.__data['token'])
            if Token_Verify.check_token(self):
                self.message_confirm()
            else:
                Read_Json.set_response(self, ERROR[5])
        else:
            Read_Json.set_response(self, ERROR[2])

    def message_confirm(self):
        if judge_dict(self.__data, ['to', 'method', 'content']):
            if self.__data['method'] == 'smtp':
                self.to_user_controling_smtp()
                if isinstance(self.__data['content'], dict):
                    if judge_dict(self.__data['content'], ['subject', 'text']):
                        if self.__data['content']['text'] is "" or self.__data['content']['subject'] is "":
                            Read_Json.set_response(self, ERROR[9])
                        if 'attachment' in self.__data.keys():
                            if isinstance(self.__data['attachment'], dict):
                                if not judge_dict(self.__data['attachment'], ['file', 'filename']):
                                    Read_Json.set_response(self, ERROR[10])
                            else:
                                Read_Json.set_response(self, ERROR[10])
                    else:
                        Read_Json.set_response(self, ERROR[9])
                else:
                    Read_Json.set_response(self, ERROR[9])
            elif self.__data['method'] == 'sms':
                self.to_user_controling_sms()
                if isinstance(self.__data['content'], str):
                    if self.__data['content'] is "":
                        Read_Json.set_response(self, ERROR[9])
                else:
                    Read_Json.set_response(self, ERROR[9])
            elif self.__data['method'] == 'wechat':
                self.to_user_controling_wechat()
                if isinstance(self.__data['content'], str):
                    if self.__data['content'] is "":
                        Read_Json.set_response(self, ERROR[9])
                else:
                    Read_Json.set_response(self, ERROR[9])
            else:
                Read_Json.set_response(self, ERROR[8])
        else:
            Read_Json.set_response(self, ERROR[2])

    def to_user_controling_wechat(self):
        if isinstance(self.__data['to'], list):
            self.__to_user = []
            for item in self.__data['to']:
                user = Wechat.query.filter_by(username=item).first()
                if user:
                    self.__to_user.append(user.openID)
                else:
                    Read_Json.set_response(self, ERROR[11])
                    Read_Json.add_response(self, 'Details', u'微信用户' + item + u'不存在')
        elif isinstance(self.__data['to'], str):
            user = Wechat.query.filter_by(nickname=self.__data['to']).first()
            if user:
                self.__to_user = user.openID
            else:
                Read_Json.set_response(self, ERROR[11])
                Read_Json.add_response(self, 'Details', u'微信用户' + self.__data['to'] + u'不存在')
        else:
            Read_Json.set_response(self, ERROR[11])


    def to_user_controling_sms(self):
        if isinstance(self.__data['to'], str):
            if re.search('^1[0-9]{10}', self.__data['to']):
                self.__to_user = self.__data['to']
            else:
                Read_Json.set_response(self, ERROR[11])
        elif isinstance(self.__data['to'], list):
            for item in self.__data['to']:
                if not re.search('^1[0-9]{10}', item):
                    Read_Json.set_response(self, ERROR[11])
                    break
            self.__to_user = self.__data['to']
        else:
            Read_Json.set_response(self, ERROR[11])

    def to_user_controling_smtp(self):
        if isinstance(self.__data['to'], str):
            if re.search('^[a-zA-z0-9\_\.].*?@[0-9a-zA-Z\.].*?\.c[o]{0,1}[mn]$', self.__data['to']):
                self.__to_user = self.__data['to']
            else:
                Read_Json.set_response(self, ERROR[11])
        elif isinstance(self.__data['to'], list):
            for item in self.__data['to']:
                if not re.search('^[a-zA-z0-9\_\.].*?@[0-9a-zA-Z\.].*?\.c[o]{0,1}[mn]$', item):
                    Read_Json.set_response(self, ERROR[11])
                    break
            self.__to_user = self.__data['to']
        else:
            Read_Json.set_response(self, ERROR[11])

    def message_controling(self):
        if Read_Json.get_response_of_key(self, 'errorCode') is None:
            user = Token_Verify.get_username(self)
            message_control = Message_Control(user)
            if message_control.return_control_result():
                send_ways = self.__data['method']
                if send_ways == 'smtp':
                    print('6666')
                    Send_Mail.__init__(self, self.__data, self.__to_user)
                elif send_ways == 'sms':
                    print('2333')
                    Send_Sms.__init__(self, self.__data, self.__to_user)
                elif send_ways == 'wechat':
                    print('888')
                    Send_Wechat.__init__(self, self.__data, self.__to_user)
            else:
                Read_Json.set_response(self, ERROR[13])
                Save_Message.__init__(self, self.__data['ip'], self.__to_user, self.__data['method'], False,
                                      str(self.__data['content']), u'超出频率控制')
                Save_Message.add_message(self)
