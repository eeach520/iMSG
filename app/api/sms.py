import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
from urllib.request import urlopen
from .config import SMS, ERROR
from .save_message import Save_Message
import base64
import hmac
from hashlib import sha1
import ssl
from .read_json import Read_Json


class Send_Sms(Read_Json, Save_Message):
    def __init__(self, send_data, to_user):
        self.__data = send_data
        self.__to_user = to_user
        self.__phone = ''
        self.__templateParam = SMS.TEMPLATE_PARAM
        self.__user_params = SMS.USER_PARAMS
        self.access_key_id = SMS.KEY_ID
        self.access_key_secret = SMS.KEY_SECRET
        self.server_address = SMS.SERVER
        self.get_data_to_param()
        self.make_request(self.__user_params)

    def get_data_to_param(self):
        self.__templateParam['errorMessage'] = self.__data['content']
        if isinstance(self.__to_user, list):
            for item in self.__to_user:
                if self.__phone:
                    self.__phone += ',' + item
                else:
                    self.__phone += item
        else:
            self.__phone = self.__to_user
        self.__user_params['PhoneNumbers'] = self.__phone
        self.__user_params['TemplateParam'] = str(self.__templateParam)
        print(self.__user_params)

    def percent_encode(self, encodeStr):
        encode_Str = str(encodeStr)
        res = urllib.parse.quote(encode_Str.encode(), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    def compute_signature(self, parameters, access_key_secret):
        sorted_parameters = sorted(list(parameters.items()), key=lambda parameters: parameters[0])
        canonicalized_query_string = ''
        for (k, v) in sorted_parameters:
            canonicalized_query_string += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)
        string_to_sign = 'GET&%2F&' + self.percent_encode(canonicalized_query_string[1:])
        h = hmac.new((access_key_secret + '&').encode(encoding="utf-8"), string_to_sign.encode('utf-8'), sha1)
        signature = base64.encodestring(h.digest()).strip()
        return signature

    def compose_url(self, user_params):
        import uuid
        import time
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))
        parameters = SMS.PARAMETERS
        parameters['Timestamp'] = timestamp
        parameters['SignatureNonce'] = str(uuid.uuid1())
        for key in list(user_params.keys()):
            parameters[key] = user_params[key]
        signature = self.compute_signature(parameters, self.access_key_secret)
        print(signature)
        parameters['Signature'] = signature.decode()
        print(parameters)
        for key in parameters.keys():
            print(key, type(parameters[key]))
        url = self.server_address + "/?" + urllib.parse.urlencode(parameters)
        for key in list(user_params.keys()):
            parameters.pop(key)
        parameters.pop('Signature')
        return url

    def make_request(self, user_params):
        if super().get_response_of_key('errorCode') is None:
            url = self.compose_url(user_params)
            request = urllib.request.Request(url)
            context = ssl._create_unverified_context()
            conn = urlopen(request, context=context)
            response = conn.read().decode()
            message = response.split('"')
            send_message = message[3]
            print(response)
            if send_message == 'OK':
                super().set_response(ERROR[0])
                Save_Message.__init__(self, self.__data['ip'], self.__to_user, 'sms', True,
                                      str(self.__data['content']), 'OK')
                Save_Message.add_message(self)
            else:
                Save_Message.__init__(self, self.__data['ip'], self.__to_user, 'sms', False,
                                      str(self.__data['content']), send_message)
                Save_Message.add_message(self)
                super().set_response(ERROR[12])
