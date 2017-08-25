# -*- coding: utf-8 -*-
import smtplib
import base64
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .read_json import Read_Json
from .config import SMTP, ERROR
from .save_message import Save_Message


class Send_Mail(Read_Json, Save_Message):
    def __init__(self, send_data, to_user):
        self.__data = send_data
        self.__smtp = smtplib.SMTP()
        self.__server = SMTP.SERVER
        self.__port = SMTP.PORT
        self.__username = SMTP.USERNAME
        self.__password = SMTP.PASSWORD
        self.__subject = None
        self.__context = None
        self.__to_Address = to_user
        self.__attachment = None
        self.__filename = None
        self.__message = MIMEMultipart()
        self.get_data_from_request()

    def get_data_from_request(self):
        self.__subject = self.__data['content']['subject']
        self.__context = self.__data['content']['text']
        if 'attachment' in self.__data.keys():
            self.__attachment = base64.b64decode(self.__data['attachment']['file'].encode())
            self.__filename = self.__data['attachment']['filename']
            self.attach_accessory_files()
        self.make_message()

    def make_message(self):
        if isinstance(self.__to_Address, list):
            self.__message['To'] = ','.join(self.__to_Address)
        else:
            self.__message['To'] = self.__to_Address
        self.__message['From'] = self.__username + SMTP.ADDRESS
        self.__message['Subject'] = self.__subject
        self.__message.attach(MIMEText(self.__context, 'plain', 'utf-8'))
        self.connect_and_login()

    def attach_accessory_files(self):
        attachment = MIMEText(self.__attachment, 'plain', 'utf-8')
        if attachment is not None:
            attachment_name = self.__filename
            attachment.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', attachment_name))
            self.__message.attach(attachment)

    def connect_and_login(self):
        try:
            self.__smtp.connect(self.__server, self.__port)
            self.__smtp.login(self.__username, self.__password)
            self.send_mail()
        except Exception as e:
            Save_Message.__init__(self, self.__data['ip'], self.__to_Address, u'邮件', False, str(self.__data['content']),
                                  str(e), None)
            Save_Message.add_message(self)
            super().set_response(ERROR[12])

    def send_mail(self):
        try:
            self.__smtp.sendmail(self.__username + SMTP.ADDRESS, self.__to_Address, self.__message.as_string())
            super().set_response(ERROR[0])
            if self.__attachment:
                file_name = '/home/files/' + str(
                    datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-")) + self.__filename
                __file = open(file_name, 'wb')
                __file.write(self.__attachment)
                Save_Message.__init__(self, self.__data['ip'], self.__to_Address, 'smtp', True,
                                      str(self.__data['content']),
                                      'OK', file_name)
            else:
                Save_Message.__init__(self, self.__data['ip'], self.__to_Address, 'smtp', True,
                                      str(self.__data['content']), 'OK')
            Save_Message.add_message(self)
        except Exception as e:
            super().set_response(ERROR[12])
            Save_Message.__init__(self, self.__data['ip'], self.__to_Address, 'smtp', False,
                                  str(self.__data['content']),
                                  str(e))
            Save_Message.add_message(self)
