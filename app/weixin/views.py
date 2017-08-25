from . import weixin
import hashlib
import time
from flask import request,make_response
import xml.etree.cElementTree as et
from .save_openid import Save_Openid


@weixin.route('/bind')
def index():
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
    elif request.method == 'POST':
        data = request.get_data()
        xml_rec = et.fromstring(data)
        toUser = xml_rec.find('ToUserName').text
        fromUser = xml_rec.find('FromUserName').text
        MsgType = xml_rec.find('MsgType').text
        Content = u'您好，暂时不能为您服务！'
        if MsgType == 'event':
            if xml_rec.find('Event').text == 'CLICK':
                if xml_rec.find('EventKey').text == 'get_openid':
                    save_openid = Save_Openid(fromUser)
                    Content = save_openid.save()
            elif xml_rec.find('Event').text == 'subscribe':
                Content = u'欢迎使用iMSG平台，我是小i。点击“获取我的iMSG账号”获取iMSG账号，即可畅享微信发送。'
        xmlss = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>" \
                % (fromUser, toUser, str(int(time.time())), Content)
        response = make_response(xmlss)
        response.content_type = "application/xml"
        return response
