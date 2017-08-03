from werkzeug.security import generate_password_hash
from ..models import User
from .. import db
from ..read_json import Json_Data


class Register_User(Json_Data):
    def __init__(self, json_data):
        super(Register_User, self).__init__(json_data)
        self.__data = super().get_data()
        self.username = None
        self.password_hash = None
        self.get_username_and_password()
        self.register_user()
        print(self.__data)

    def get_username_and_password(self):
        if 'username' in self.__data.keys() and 'password'in self.__data.keys():
            self.username = self.__data['username']
            __old_user = User.query.filter_by(name=self.username).first()
            if __old_user is None:
                # 为了安全起见,这里存储密码的哈希散列
                self.password_hash = generate_password_hash(self.__data['password'])
                super().set_response('success', True)
                super().set_response(self.username, u'欢迎注册iMSG平台')
            else:
                super().set_response('error', u'抱歉，用户名已存在')
        else:
            super().set_response('error', u'未包含用户名和密码')

    def register_user(self):
        if super().get_response_for_key('success') is True:
            __user = User(name=self.username, password=self.password_hash)
            db.session.add(__user)
            db.session.commit()
