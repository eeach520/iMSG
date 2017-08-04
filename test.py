import time
# a = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
# print(a)
import uuid
import hmac, secrets, base64

# print(uuid.uuid1())
# key = str(uuid.uuid1())
# print('key',key)
# message = 'eeach'
# ts_str = str(time.time() + 300)
# sha1_str = hmac.new(key.encode('utf-8'), ts_str.encode('utf-8'), 'sha1').hexdigest()
# print('sha1_str=', sha1_str)
# random_token = secrets.token_hex(16)
# print('random=', random_token)
# token = random_token + ':' + ts_str + ':' + message + ':' + sha1_str
# print('token', token)
# base64_token = base64.urlsafe_b64encode(token.encode('utf-8')).decode('utf-8')
# print('base64', base64_token,type(base64_token))
# haha=base64.urlsafe_b64decode(base64_token).decode('utf-8')
# print(haha)
# class A():
#     def __init__(self, str):
#         self.data = str + "haha"
#
#     def set_data(self, str_add):
#         self.data += str_add
#
#     def return_data(self):
#         return self.data
#
#     def get_data(self):
#         return (self.data + 'kl')
#
#
# class B():
#     def __init__(self, str):
#         self.data = str
#
#     def get_data(self):
#         return self.data + '这是B'
#
#
# class C(A, B):
#     def __init__(self, str):
#         A.__init__(self, str)
#         self.sdata = super().return_data()
#         B.__init__(self, self.sdata)
#
#     def show(self):
#         print(super().return_data())
#         # print(super().get_data())
#         print(B.get_data(self))
#         # super(C, self).show()


# if __name__ == '__main__':
# b = {'username': 'eeach','sad':'asd' ,'pssword': 'zxl123'}
# if 'username' in b.keys() and 'password' in b.keys():
#     print('可以')
# # if b.has_key('username'):
# #     print("这个也可以")
# print(list(b.keys()),type(b.keys()))
# if ['username','passqord'] in list(b.keys()):
#     print('成功一半')
# a = C('eeach')
# a.show()
# a = '{"message":"你好","Raskdl":"asdasd"}'
# b = a.split('"')
# print(b)
# c=dict(b)

from urllib import parse, request
from urllib.parse import quote
import json

access_token = 'Z0cbG6ecyLW9x2KkKqyeox1nXi5o9jfYAEY5dJqwPQlM0TLG4t_7Ez6bee5hRuIczv9Tjh7bgLMPmlPgQIQo669h45ezjmoAEd7DalC9oItUNjCy8PCf9N3GiuSJa6_BWNJdAGAHYU'
texmod = {"touser": "oLMsSw3UBKRwnWeDgzG7eLCQFxJE", "msgtype": "text", "text": {"content": 'as'}}
print(texmod)
# texmod=
texmod = json.dumps(texmod, ensure_ascii=False, separators=(',', ':'))
texmod = texmod.encode()
print(texmod)
url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=" + access_token
req = request.Request(url=url, data=texmod)
res = request.urlopen(req)
res = res.read()
res = json.loads(res)
print(res,type(res))
print(res['errcode'])




# -*- coding: utf-8 -*-
# from flask import Flask, request, render_template, make_response
# from flask import Flask, request, render_template, make_response
# from flask.ext.script import Manager
# import hashlib
# import xml.etree.cElementTree as et
# import time
#
# app = Flask(__name__)
# manager = Manager(app)
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
# @app.route('/weixin', methods=['GET', 'POST'])
# def weixin():
#     if request.method == 'GET':
#         data = request.args
#         token = 'zhangxinglei'
#         signature = data.get('signature', '')
#         timestamp = data.get('timestamp', '')
#         nonce = data.get('nonce', '')
#         echostr = data.get('echostr', '')
#         mylist = [token, timestamp, nonce]
#         mylist.sort()
#         s = mylist[0] + mylist[1] + mylist[2]
#         hashcode = hashlib.sha1(s.encode('utf-8')).hexdigest()
#         if hashcode == signature:
#             return echostr
#         else:
#             return ""
#     if request.method == 'POST':
#         data = request.get_data()
#         xml_rec = et.fromstring(data)
#         ToUserName = xml_rec.find('ToUserName').text
#         fromUser = xml_rec.find('FromUserName').text
#         MsgType = xml_rec.find('MsgType').text
#         if MsgType == 'event':
#             msgcontent = xml_rec.find('Event').text
#             if msgcontent == 'subscribe':
#                 user=
#                 Content = u'亲，你好！'
#             else:
#                 Content = None
#         else:
#             Content = xml_rec.find('Content').text
#         xmlss = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>" % (
#             fromUser, ToUserName, str(int(time.time())), Content)
#         response = make_response(xmlss)
#         response.content_type = "application/xml"


# import re
#
# if re.match(r'^name:', 'name:asascasdasd'):
#     print('name:')
#     print('成功')
# else:
#     print('失败')
# a = '张兴磊'
# # print(len(a))
# import re
#
# if re.match(r'[0-9a-z\_]{4}$', 'a_ss'):
#     print('成功')
# else:
#     print('失败')
