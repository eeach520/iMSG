from . import main
from flask import jsonify, request, make_response
from flask_login import login_required
from .send_message import Send_Message
from .wechat import Send_Wechat
import xml.etree.cElementTree as et
from ..models import Wechat_user
from .. import db
import hashlib, time, re


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


@main.route('/weixin', methods=['GET', 'POST'])
def weixin():
    if request.method == 'GET':
        data = request.args
        token = 'zhangxinglei'
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        my_list = [token, timestamp, nonce]
        my_list.sort()
        s = my_list[0] + my_list[1] + my_list[2]
        hashcode = hashlib.sha1(s.encode('utf-8')).hexdigest()
        if hashcode == signature:
            return echostr
        else:
            return ""
    if request.method == 'POST':
        data = request.get_data()
        xml_rec = et.fromstring(data)
        ToUserName = xml_rec.find('ToUserName').text
        fromUser = xml_rec.find('FromUserName').text
        MsgType = xml_rec.find('MsgType').text
        Content = " "
        if MsgType == 'event':
            msgcontent = xml_rec.find('Event').text
            if msgcontent == 'subscribe':
                user = Wechat_user.query.filter_by(openID=fromUser).first()
                if user is None:
                    Content = u'亲，你好！欢迎第一次光临本微信，我是小i。为了让我更方便记住你，你可以输入“name:你的昵称”（引号不用输入），让我为你存档哦！'
                else:
                    Content = u'欢迎回来' + user.nickname
            else:
                Content = None
        elif MsgType == 'text':
            from_Content = xml_rec.find('Content').text
            if re.match(r'name:', from_Content):
                nickname = from_Content.split(':')[1]
                if re.match(r'[0-9a-zA_Z\_]{4,9}', nickname):
                    old_user = Wechat_user.query.filter_by(nickname=nickname).first()
                    if old_user is None:
                        db.session.add(Wechat_user(nickname=nickname, openID=fromUser))
                        db.commit()
                        confirm_user = {"touser": fromUser,
                                        "content": u'尊敬的' + nickname + u'先生/女士，我们已经将您的信息保存，感谢您的信任，祝您使用愉快'}
                        new_user=Send_Wechat(confirm_user)
                    else:
                        Content = u'该昵称已存在'
                else:
                    Content = u'昵称不合法（长度为4-9，只能包含字母、数字和_）'
            else:
                Content = u'收到您发的信息“' + xml_rec.find('Content').text + '”，但我目前不会响应'
                pass
        else:
            Content = u'这是' + MsgType + u',我暂时还不认识!!!'
            pass
        xmlss = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>" \
                % (fromUser, ToUserName, str(int(time.time())), Content)
        response = make_response(xmlss)
        response.content_type = "application/xml"
        return response


@main.app_errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "哈哈,传说中的404错误"})
