from .. import db
from ..models import User
from .token_verify import Token_Verify
from .read_json import Read_Json
from .register import judge_dict
from .config import ERROR


class Modify_Frequency(Token_Verify, Read_Json):
    def __init__(self, json_data):
        Read_Json.__init__(self, json_data)
        self.__data = Read_Json.get_data(self)
        if self.__data:
            self.get_message()

    def get_message(self):
        Token_Verify.__init__(self, self.__data['token'])
        if 'available' in self.__data.keys() and Token_Verify.check_token(self):
            if isinstance(self.__data['available'], bool):
                User.query.filter_by(username=Token_Verify.get_username(self)).update({
                    'available': self.__data['available']
                })
                db.session.commit()
            else:
                Read_Json.set_response(self, ERROR[17])
        if judge_dict(self.__data, ['token', 'per_day', 'per_hour']):
            if isinstance(self.__data['per_day'], int) and isinstance(self.__data['per_hour'], int):
                if Token_Verify.check_token(self):
                    print(Token_Verify.get_username(self))
                    if Read_Json.get_response_of_key(self, 'errorCode') is None:
                        User.query.filter_by(username=Token_Verify.get_username(self)).update({
                            'max_day_times': self.__data['per_day'],
                            'max_hour_times': self.__data['per_hour']
                        })
                        db.session.commit()
                        Read_Json.set_response(self, ERROR[0])
                else:
                    Read_Json.set_response(self, ERROR[5])
            else:
                Read_Json.set_response(self, ERROR[17])
        else:
            Read_Json.set_response(self, ERROR[2])
