from . import main
from flask import jsonify, request
from flask_login import login_required
from .send_message import Send_Message


@main.route('/', methods=['GET', 'POST'])
def hello_world():
    return jsonify({'注册地址': '/register', '登陆地址': '/login', '发送信息': '/send'})


@main.route('/send', methods=['GET', 'POST'])
@login_required
def send():
    if request.method == 'POST':
        send_data = request.get_data()
        send_message = Send_Message(send_data)
        return send_message.get_response_to_views()
    return jsonify({'error': "只接受POST方法"})


@main.app_errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "哈哈,传说中的404错误"})
