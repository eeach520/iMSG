import time
import base64
from .. import db
from ..models import Token, User


class Token_Verify:
    def __init__(self, token):
        self.__token = token
        self.__username = None

    def check_token(self):
        old_token = Token.query.filter_by(token=self.__token).first()
        if old_token is None:
            return False
        else:
            token_str = base64.urlsafe_b64decode(self.__token).decode()
            token_list = token_str.split(':')
            expire_time = token_list[1]
            self.__username = token_list[2]
            if float(expire_time) < time.time():
                db.session.delete(old_token)
                db.session.commit()
                return False
            else:
                new_user = User.query.filter_by(username=self.__username).first()
                if new_user:
                    new_user.ping()
                return True

    def get_username(self):
        return self.__username
