import hmac, base64, time
from ..models import Token
from .. import db
from flask_login import current_user


class VerifyToken():
    def __init__(self, dict_data):
        self.__data = dict_data
        self.__token = None
        self.get_data_to_token()

    def get_data_to_token(self):
        if 'token' in self.__data.keys():
            self.__token = self.__data['token']

    def return_token(self):
        return self.__token

    def vsrify_token(self):
        old_token = Token.query.filter_by(token=self.__token).first()
        if old_token is None:
            return 'NO'
        else:
            token_str = base64.urlsafe_b64decode(self.__token).decode('utf-8')
            token_list = token_str.split(':')
            expire_time = token_list[1]
            expire_name = token_list[2]
            if float(expire_time) < time.time():
                db.session.delete(old_token)
                db.session.commit()
                return 'invalid'
            if current_user.name != expire_name:
                return 'error'
            return 'correct'
