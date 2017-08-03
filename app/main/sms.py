import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
from urllib.request import urlopen
import base64
import hmac
from hashlib import sha1
import time
import uuid
import ssl
from ..read_json import Json_Data


class Send_Sms(Json_Data):
    def __init__(self, send_data):
        self.__data = send_data
        self.__templateParam = None
        self.__phoneNumber = None
        self.__user_params = {}
        self.access_key_id = 'LTAI8k5R9SLp49Dh'
        self.access_key_secret = 'om3WttcF0ugQ1gpES3PqOOsyYzt36x'
        self.server_address = 'https://dysmsapi.aliyuncs.com'
        self.get_data_to_param()
        self.make_request(self.__user_params)

    def get_data_to_param(self):
        if 'content' in self.__data.keys() and 'phoneNumber' in self.__data.keys():
            self.__templateParam = {"name": self.__data['content'], "index": "1"}
            self.__user_params = {'Action': 'SendSms', 'TemplateParam': self.__templateParam,
                                  'PhoneNumbers': self.__data['phoneNumber'], 'SignName': 'iMSG平台', \
                                  'TemplateCode': 'SMS_79340001'}
        else:
            super().set_response('error', u'未包含有效字段（发送短信应有“phoneNumber（电话号码）”和“content（内容）”字段）')

    def percent_encode(self, encodeStr):
        encode_Str = str(encodeStr)
        res = urllib.parse.quote(encode_Str.encode('utf8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    def compute_signature(self, parameters, access_key_secret):
        sortedParameters = sorted(list(parameters.items()), key=lambda parameters: parameters[0])
        canonicalizedQueryString = ''
        for (k, v) in sortedParameters:
            canonicalizedQueryString += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)
        stringToSign = 'GET&%2F&' + self.percent_encode(canonicalizedQueryString[1:])
        h = hmac.new((access_key_secret + '&').encode(encoding="utf-8"), stringToSign.encode('utf-8'), sha1)
        signature = base64.encodestring(h.digest()).strip()
        return signature

    def compose_url(self, user_params):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))
        parameters = { \
            'Format': 'JSON', \
            'Version': '2017-05-25', \
            'AccessKeyId': self.access_key_id, \
            'SignatureVersion': '1.0', \
            'SignatureMethod': 'HMAC-SHA1', \
            'SignatureNonce': str(uuid.uuid1()), \
            'RegionId': 'cn-hangzhou',
            'Timestamp': timestamp, \
            "OutId": "106980001711226769"
        }
        for key in list(user_params.keys()):
            parameters[key] = user_params[key]
        signature = self.compute_signature(parameters, self.access_key_secret)
        parameters['Signature'] = signature
        url = self.server_address + "/?" + urllib.parse.urlencode(parameters)
        return url

    def make_request(self, user_params):
        if super().get_response_for_key('error') is None:
            url = self.compose_url(user_params)
            request = urllib.request.Request(url)
            context = ssl._create_unverified_context()
            conn = urlopen(request, context=context)
            response = conn.read().decode('utf-8')
            message = response.split('"')
            send_message = message[3]
            if send_message == 'OK':
                super().set_response('success', True)
                super().set_response('发送时间', time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()))
            else:
                super().set_response('error', send_message)
