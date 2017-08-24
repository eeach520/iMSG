from .. import db
from ..models import Message, Wechat
from .token_verify import Token_Verify


class Save_Message(Token_Verify):
    def __init__(self, ip, to_user, method, result, content, reason,attachment=None):
        self.__from_user = Token_Verify.get_username(self)
        self.__ip = ip
        self.__to_user = to_user
        self.__method = method
        self.__content = content
        self.__result = result
        self.__reason = reason
        self.__attachment = attachment
        print('save0', Token_Verify.get_username(self))

    def add_message(self):
        if isinstance(self.__to_user, str):
            if self.__method=='wechat':
                to_user = Wechat.query.filter_by(openID=self.__to_user).first().nickname
            else:
                to_user = self.__to_user
            message = Message(self.__from_user, self.__ip, to_user, self.__method, self.__result, self.__content,
                              self.__reason, self.__attachment)
            db.session.add(message)
            db.session.commit()
        else:
            for item in self.__to_user:
                if self.__method == 'wechat':
                    to_user = Wechat.query.filter_by(openID=item).first().nickname
                else:
                    to_user = item
                message = Message(self.__from_user, self.__ip, to_user, self.__method, self.__result, self.__content,
                                  self.__reason, self.__attachment)
                db.session.add(message)
                db.session.commit()
