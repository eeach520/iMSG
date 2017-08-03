from . import auth
from flask import request, jsonify
from .register import Register_User
from .login import Login_User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        register_data = request.get_data()
        user = Register_User(register_data)
        return user.get_response_to_views()
    return jsonify({'error': u'本接口只接受POST方法'})


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_data = request.get_data()
        user = Login_User(login_data)
        return user.get_response_to_views()
    return jsonify({'error': u'注册登陆后才可以使用本接口'})
