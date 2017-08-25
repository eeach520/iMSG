from flask import render_template, abort, flash, redirect, url_for, request, make_response
from flask import send_from_directory
from . import main
from .. import db
import json
import os
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from flask_login import login_required, current_user
from ..models import User, Message
from .response_message import Reponse_Message


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template('main/admin.html')


@main.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        print(data)
        user = User.query.filter_by(username=current_user.username).first()
        if check_password_hash(current_user.password, data[0]):
            try:
                user.password = generate_password_hash(data[1])
                db.session.add(user)
                db.session.commit()
                response = {"success": "OK"}
            except Exception as e:
                response = {"success": "no", "error": str(e)}
        else:
            response = {"success": "no", "error": "原密码错误"}
        return jsonify(response)
    return 'asdas'


@main.route('/messages', methods=['GET', 'POST'])
@login_required
def message():
    now = str(datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S'))
    return render_template('main/message.html', now=now)


@main.route('/message', methods=['GET', 'POST'])
@login_required
def show_message():
    id = request.args.get('id')
    print(id)
    message_data = Message.query.filter_by(id=id).first()
    subject = None
    text = None
    filename = None
    if message_data.attachment:
        filename = message_data.attachment.split('/')[len(message_data.attachment.split('/')) - 1]
    if message_data.send_method == 'smtp':
        print(message_data.content.split('\''))
        subject = message_data.content.split('\'')[3]
        text = message_data.content.split('\'')[7]
    if not message_data:
        abort(404)
    if current_user.role_id == 1 or message_data.from_user == current_user.username:
        print('adasd')
        pass
    else:
        abort(404)
    return render_template('message.html', message=message_data, subject=subject, text=text, filename=filename)


@main.route('/user', methods=['GET', 'POST'])
@login_required
def show_user():
    username = request.args.get('username')
    user_message = User.query.filter_by(username=username).first()
    smtp_times_ok = Message.query.filter_by(from_user=username, send_method='smtp', send_result=True).count()
    sms_times_ok = Message.query.filter_by(from_user=username, send_method='sms', send_result=True).count()
    wechat_times_ok = Message.query.filter_by(from_user=username, send_method='wechat', send_result=True).count()
    smtp_times_no = Message.query.filter_by(from_user=username, send_method='smtp', send_result=False).count()
    sms_times_no = Message.query.filter_by(from_user=username, send_method='sms', send_result=False).count()
    wechat_times_no = Message.query.filter_by(from_user=username, send_method='wechat', send_result=False).count()
    if not user_message:
        abort(404)
    if current_user.role_id == 1 or username == current_user.username:
        pass
    else:
        abort(404)
    return render_template('user.html', user=user_message, smtp_ok=smtp_times_ok, sms_ok=sms_times_ok,
                           wechat_ok=wechat_times_ok, smtp_no=smtp_times_no, sms_no=sms_times_no,
                           wechat_no=wechat_times_no)


@main.route('/userdata', methods=['GET', 'POST'])
@login_required
def user_data():
    if request.method == 'POST':
        if request.get_data():
            print('1', json.loads(request.get_data()))
            page = int(json.loads(request.get_data())['pageIndex'])
            size = int(json.loads(request.get_data())['pageSize'])
            search = None
            if 'searchText' in dict(json.loads(request.get_data())).keys():
                search = json.loads(request.get_data())['searchText']
        total = User.query.filter_by(role_id=2).count()
        pagination = User.query.filter_by(role_id=2)
        if current_user.role_id == 2:
            pagination = pagination.filter_by(username=current_user.username).all()
            total = 1
        else:
            if search:
                print('hu')
                search = '%' + search + '%'
                pagination = pagination.filter(User.username.like(search)).all()
            else:
                pagination = pagination.all()
        response = []
        for index in range(len(pagination)):
            if ((index + 1) > (page - 1) * size) and ((index + 1) <= (page * size)):
                response.append({"id": index + 1, "index": pagination[index].id, "username": pagination[index].username,
                                 "per_day": pagination[index].max_day_times,
                                 "per_hour": pagination[index].max_hour_times, "available": pagination[index].available,
                                 "since": pagination[index].member_since, "seen": pagination[index].last_seen})
        return jsonify({"total": total, "rows": response})
    return ''


@main.route('/users')
@login_required
def user():
    return render_template('main/user.html')


@main.route('/dataget', methods=['GET', 'POST'])
@login_required
def data_get():
    if request.method == 'POST':
        print(request.get_data())
        res = Reponse_Message(request.get_data(), current_user.username)
        return res.response_rows()
    return ''


@main.route('/download/<file_path>/', methods=['GET', 'POST'])
def download(file_path):
    print(file_path, type(file_path))
    if os.path.isfile('D:/git-git/files/' + file_path):
        response = make_response(send_from_directory('D:/git-git/files/', file_path, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(file_path.encode().decode('latin-1'))
        return response
    else:
        abort(404)


@main.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'POST':
        print(request.get_data())
        print(json.loads(request.get_data()), type(json.loads(request.get_data())))
        try:
            data = json.loads(request.get_data())
            for item in data:
                user = User.query.filter_by(username=item).first()
                db.session.delete(user)
                db.session.commit()
            response = {"success": "OK"}
        except Exception as e:
            response = {"success": "no", "error": str(e)}
        return jsonify(response)
    return 'null'


@main.route('/modify', methods=['GET', 'POST'])
@login_required
def modify_user():
    if request.method == 'POST':
        try:
            data = json.loads(request.get_data())
            print(data)
            username = data[0]
            per_day = int(data[1])
            per_hour = int(data[2])
            available = data[3]
            user = User.query.filter_by(username=username).first()
            user.modify(per_day, per_hour, available)
            db.session.add(user)
            db.session.commit()
            response = {'success': "OK"}
        except Exception as e:
            print(e)
            response = {'success': 'no', 'error': str(e)}
        return jsonify(response)
    return 'only post'


@main.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        data = request.get_data()
        try:
            data = json.loads(data)
            print(data, type(data[2]), type(data[4]), data[4])
            username = data[0]
            password = data[1]
            per_day = data[2]
            per_hour = data[3]
            available = data[4]
            if username != '' and password != '' and per_day != '' and per_hour != '' and available != '':
                old_user = User.query.filter_by(username=username).first()
                if old_user:
                    response = {'success': 'no', 'error': '用户名已存在'}
                else:
                    per_day = int(per_day)
                    per_hour = int(per_hour)
                    u = User(username, generate_password_hash(password))
                    db.session.add(u)
                    db.session.commit()
                    u.modify(per_day, per_hour, available)
                    db.session.add(u)
                    db.session.commit()
                    response = {'success': 'OK'}
            else:
                response = {'success': 'no', 'error': '字段不能为空'}
        except Exception as e:
            print(e)
            response = {'success': 'no', 'error': str(e)}
        return jsonify(response)
    return 'only post'
