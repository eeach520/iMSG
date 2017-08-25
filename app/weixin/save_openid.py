from ..models import Wechat
from .. import db


class Save_Openid:
    def __init__(self, openid):
        self.__openid = openid

    def save(self):
        number = Wechat.query.count()
        nickname = 'iMSG-' + str(10000 + number + 1)
        old_user = Wechat.query.filter_by(openID=self.__openid).first()
        if old_user:
            old_nickname = old_user.nickname
            return u'您已经有iMSG账号了：' + old_nickname
        else:
            user = Wechat(self.__openid, nickname)
            db.session.add(user)
            db.session.add()
            return u'您iMSG的账号是' + nickname
