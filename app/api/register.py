from .. import db
from .config import ERROR
from ..models import User
from .read_json import Read_Json
from werkzeug.security import generate_password_hash


def judge_dict(dict0, key):
    answer = True
    for item in key:
        if item not in dict0.keys():
            answer = False
            break
        else:
            pass
    return answer


class Register(Read_Json):
    def __init__(self, json_data):
        super(Register, self).__init__(json_data)
        self.__data = super().get_data()
        self.__username = None
        self.__password_hash = None
        if self.__data:
            self.get_data_from_request()

    def get_data_from_request(self):
        if judge_dict(self.__data, ['username', 'password']):
            self.__username = self.__data['username']
            if User.query.filter_by(username=self.__username).first():
                super().set_response(ERROR[4])
            else:
                self.__password_hash = generate_password_hash(self.__data['password'])
                self.register_user()
        else:
            super().set_response(ERROR[2])

    def register_user(self):
        try:
            __user = User(self.__username, self.__password_hash)
            db.session.add(__user)
            db.session.commit()
            super().set_response(ERROR[0])
        except:
            super().set_response(ERROR[3])
