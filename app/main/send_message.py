from .smtp import Send_Mail
from ..read_json import Json_Data
from flask_login import logout_user
from .verifyTokens import VerifyToken
from .wechat import Send_Wechat
from .sms import Send_Sms


class Send_Message(Send_Wechat, Send_Sms, Send_Mail, Json_Data, VerifyToken):
    def __init__(self, send_data):
        Json_Data.__init__(self, send_data)
        self.__data = Json_Data.get_data(self)
        VerifyToken.__init__(self, self.__data)
        self.verify_token()

    def verify_token(self):
        if VerifyToken.return_token(self) is None:
            Json_Data.set_response(self, 'error', u'未包含token字段')
        else:
            token_answer = VerifyToken.vsrify_token(self)
            if token_answer is 'NO':
                Json_Data.set_response(self, 'error', u'token不存在或已失效')
            elif token_answer is 'invalid':
                logout_user()
                Json_Data.set_response(self, 'error', u'token已失效')
            elif token_answer is 'error':
                logout_user()
                Json_Data.set_response(self, 'error', u'token与用户不匹配')
            elif token_answer is 'correct':
                self.run()

    def run(self):
        if 'ways' not in self.__data.keys():
            Json_Data.set_response(self, 'error', u'未指明发送方式')
        else:
            send_ways = self.__data['ways']
            if send_ways == 'smtp':
                Send_Mail.__init__(self, self.__data)
            elif send_ways == 'sms':
                Send_Sms.__init__(self, self.__data)
            elif send_ways == 'wechat':
                Send_Wechat.__init__(self,self.__data)
            else:
                Json_Data.set_response(self, 'error', u'不能识别发送方式，请选择smtp（邮件）、sms（短信）或wechat（微信）')
