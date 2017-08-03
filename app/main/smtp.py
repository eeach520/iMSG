# -*- coding: utf-8 -*-
import smtplib, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..read_json import Json_Data


class Send_Mail(Json_Data):
    def __init__(self, send_data):
        self.__data = send_data
        self.__smtp = smtplib.SMTP()
        self.__server = 'smtp.163.com'
        self.__port = 25
        self.__username = 'eeach_test'
        self.__password = 'zxl123456'
        self.__subject = None
        self.__context = None
        self.__to_Address = None
        self.__attach_Path = None
        self.__message = None
        self.get_data_from_json()
        self.make_message()
        self.attach_accessory_files()
        self.connect_and_login()
        self.send_mail()

    def get_data_from_json(self):
        if 'to_Address' in self.__data.keys() and 'content' in self.__data.keys() and 'subject' in self.__data.keys():
            self.__to_Address = self.__data['to_Address']
            self.__subject = self.__data['subject']
            self.__context = self.__data['content']
            if 'attach' in self.__data.keys():
                self.__attach_Path = self.__data['attach']
                super().set_response('Having_Attachment', 'YES')
            else:
                super().set_response('Having_Attachment', 'NO')
        else:
            super().set_response('error', \
                                   u'未包含有效字段(使用邮件至少包括“to_Address（收件人）”、”subject（主题）“和“content（正文）这三个字段”)')

    def make_message(self):
        if super().get_response_for_key('error') is None:
            self.__message = MIMEMultipart()
            self.__message['From'] = self.__username + '@163.com'
            self.__message['To'] = self.__to_Address
            self.__message['Subject'] = self.__subject
            self.__message.attach(MIMEText(self.__context, 'plain', 'utf-8'))

    def attach_accessory_files(self):
        if (super().get_response_for_key('error'), \
            super().get_response_for_key('Have_Attachment')) \
                is (None, 'YES'):
            pass

    def connect_and_login(self):
        try:
            self.__smtp.connect(self.__server, self.__port)
            self.__smtp.login(self.__username, self.__password)
        except:
            super().set_response('error', u'登陆邮箱失败')

    def send_mail(self):
        if Json_Data.get_response_for_key(self, 'error') is None:
            try:
                self.__smtp.sendmail(self.__username + '@163.com', self.__to_Address, self.__message.as_string())
                super().set_response('success', True)
                super().set_response('发送时间', time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()))
            except Exception as e:
                super().set_response('error', str(e))
