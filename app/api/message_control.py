# -*- coding: utf-8 -*-
import datetime
from ..models import User, Message


class Message_Control:
    def __init__(self, username):
        self.__username = username
        self.__user = None
        self.__send_times = None

    def verify_available_limit(self):
        self.__user = User.query.filter_by(username=self.__username).first()
        if self.__user:  # 这里引入判断为了防止临时操作数据引起的异常
            if self.__user.available is False:
                return False
            else:
                return True
        else:
            return False

    def verify_day_limit(self):
        now = datetime.datetime.now()
        newest = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
        latest = newest + datetime.timedelta(days=1)
        print(newest, latest)
        send_times = Message.query.filter_by(send_result=True).filter(Message.send_time > str(newest),
                                                                      Message.send_time < str(latest)).count()
        print(send_times, 'day')
        if send_times < self.__user.max_day_times:
            return True
        else:
            return False

    def verify_hour_limit(self):
        now = datetime.datetime.now()
        newest = (now - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        latest = (now + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        send_times = Message.query.filter_by(send_result=True).filter(Message.send_time > str(newest),
                                                                      Message.send_time < str(latest)).count()
        print(send_times, 'hour')
        if send_times < self.__user.max_hour_times:
            return True
        else:
            return False

    def return_control_result(self):
        # 这里首先判断verify_available_limit()，即便后两个函数中有异常也不会去执行，因为verify_available_limit()首先返回False
        if self.verify_available_limit() and self.verify_day_limit() and self.verify_hour_limit():
            return True
        else:
            return False
