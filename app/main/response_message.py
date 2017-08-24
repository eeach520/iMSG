from app.api.read_json import Read_Json
from app.models import Message
from flask import jsonify


class Reponse_Message(Read_Json):
    def __init__(self, json_data):
        Read_Json.__init__(self, json_data)
        self.__data = Read_Json.get_data(self)
        print(self.__data)
        self.__start = self.__data['start_time'].replace('-', ' ').replace('/', '-')
        self.__end = self.__data['end_time'].replace('-', ' ').replace('/', '-')
        self.__from = self.__data['from_user']
        self.__to = self.__data['to']
        self.__ip = self.__data['ip']
        self.__method = self.__data['method']
        self.__result = self.__data['result']
        self.__page = self.__data['pageIndex']
        self.__order = self.__data['order']
        self.__size = self.__data['pageSize']
        self.__datas = None
        self.__ordername = None
        if 'ordername' in self.__data.keys():
            self.__ordername = self.__ordername = self.__data['ordername']
        self.get_data_order()
        self.get_data_search()

    def get_data_order(self):
        if self.__ordername:
            if self.__order == 'asc':
                if self.__ordername == 'from_user':
                    self.__datas = Message.query.order_by(Message.from_user.asc())
                elif self.__ordername == 'ip':
                    self.__datas = Message.query.order_by(Message.ip.asc())
                elif self.__ordername == 'to_user':
                    self.__datas = Message.query.order_by(Message.to_user.asc())
                else:
                    self.__datas = Message.query.order_by(Message.send_time.asc())
            else:
                if self.__ordername == 'from_user':
                    self.__datas = Message.query.order_by(Message.from_user.desc())
                elif self.__ordername == 'ip':
                    self.__datas = Message.query.order_by(Message.ip.desc())
                elif self.__ordername == 'to_user':
                    self.__datas = Message.query.order_by(Message.to_user.desc())
                else:
                    self.__datas = Message.query.order_by(Message.send_time.desc())
        else:
            if self.__order == 'asc':
                self.__datas = Message.query.order_by(Message.id.asc())
            else:
                self.__datas = Message.query.order_by(Message.id.desc())

    def get_data_search(self):
        if self.__start != '' and self.__end != '':
            self.__datas = self.__datas.filter(Message.send_time > self.__start, Message.send_time < self.__end)
        if self.__start != '' and self.__end == '':
            self.__datas = self.__datas.filter(Message.send_time > self.__start)
        if self.__start == '' and self.__end != '':
            self.__datas = self.__datas.filter(Message.send_time < self.__end)
        if self.__from != '':
            self.__datas = self.__datas.filter_by(from_user=self.__from)
        if self.__to != '':
            self.__datas = self.__datas.filter_by(to_user=self.__to)
        if self.__ip != '':
            self.__datas = self.__datas.filter_by(ip=self.__ip)
        if self.__method == u'邮件':
            self.__datas = self.__datas.filter_by(send_method='smtp')
        if self.__method == u'微信':
            self.__datas = self.__datas.filter_by(send_method='wechat')
        if self.__method == u'短信':
            self.__datas = self.__datas.filter_by(send_method='sms')
        if self.__result:
            self.__datas = self.__datas.filter_by(send_result=True)

    def response_rows(self):
        total = self.__datas.count()
        pagination = self.__datas.all()
        response = []
        for index in range(len(pagination)):
            if ((index + 1) > (self.__page - 1) * self.__size) and ((index + 1) <= (self.__page * self.__size)):
                content = pagination[index].content
                if pagination[index].send_method=='smtp':
                    content=content.split('\'')[3]
                response.append(
                    {"index": index + 1, "id": pagination[index].id, "from_user": pagination[index].from_user,
                     "ip": pagination[index].ip, "to_user": pagination[index].to_user,
                     "send_method": pagination[index].send_method,
                     "send_result": pagination[index].send_result,
                     "content": content,
                     "send_time": str(pagination[index].send_time)})
        return jsonify({"total": total, "rows": response})
