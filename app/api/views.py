from . import api
from flask import request, jsonify
from .send_message import Send_Message
from .login import Login
from ..models import Message
from .modify_frequency import Modify_Frequency
from .register import Register


@api.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        json_data = request.get_data()
        reg = Register(json_data)
        return reg.get_response_to_views()
    return 'register'


@api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        json_data = request.get_data()
        reg = Login(json_data)
        return reg.get_response_to_views()
    return 'login'


@api.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        ip = request.remote_addr
        json_data = request.get_data()
        reg = Send_Message(json_data, ip)
        return reg.get_response_to_views()
    return 'send'


@api.route('/modify', methods=['GET', 'POST'])
def modify():
    if request.method == 'POST':
        json_data = request.get_data()
        reg = Modify_Frequency(json_data)
        return reg.get_response_to_views()
    return 'modify'


@api.route('/query')
def query():
    response = Message.query.order_by(Message.send_time.desc()).all()
    total = Message.query.order_by(Message.send_time.desc()).count()
    res = {}
    for i in range(len(response)):
        haha = {}
        haha['from'] = response[i].from_user
        haha['ip'] = response[i].ip
        haha['to'] = response[i].to_user
        haha['method'] = response[i].send_method
        haha['result'] = response[i].send_result
        haha['time'] = response[i].send_time
        haha['content'] = response[i].content
        haha['error'] = response[i].error_reason
        res[i + 1] = haha
    return jsonify({"total": total, "total_data": res})


@api.app_errorhandler(403)
def forbidden(e):
    return u'传说中的403'


@api.app_errorhandler(404)
def page_not_found(e):
    return u'传说中的404'


@api.app_errorhandler(500)
def internal_server_error(e):
    return u'传说中的400'


@api.app_errorhandler(400)
def bad_request(e):
    return u'传说中的400'
