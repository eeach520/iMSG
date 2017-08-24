from app import db
from flask_login import UserMixin
from . import login_manager
import datetime


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String, nullable=False)
    available = db.Column(db.Boolean, default=True)
    max_day_times = db.Column(db.Integer, default=20)
    max_hour_times = db.Column(db.Integer, default=5)
    member_since = db.Column(db.String, nullable=False)
    last_seen = db.Column(db.String, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, username, password, role_id=2):
        self.username = username
        self.password = password
        self.member_since = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.role_id = role_id

    def modify(self, per_day, per_hour, available):
        self.max_day_times = per_day
        self.max_hour_times = per_hour
        self.available = available

    def __repr__(self):
        return '<User %r>' % self.username

    def ping(self):
        self.last_seen = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.add(self)


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.String(64), index=True)
    ip = db.Column(db.String(), index=True)
    to_user = db.Column(db.String(64), index=True)
    send_method = db.Column(db.String(64), index=True)
    send_result = db.Column(db.Boolean, index=True)
    send_time = db.Column(db.String, index=True)
    content = db.Column(db.String, index=True)
    attachment = db.Column(db.String, nullable=True)
    error_reason = db.Column(db.String, nullable=True)

    def __init__(self, from_user, ip, to_user, method, result, content, reason, attachment=None):
        self.from_user = from_user
        self.ip = ip
        self.to_user = to_user
        self.send_method = method
        self.send_result = result
        self.send_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.content = content
        self.error_reason = reason
        self.attachment = attachment


class Token(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, nullable=False)
    generate_time = db.Column(db.String, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class Wechat(db.Model):
    __tablename__ = 'wechat'
    id = db.Column(db.Integer, primary_key=True)
    openID = db.Column(db.String, nullable=False, unique=True)
    nickname = db.Column(db.String, index=True, nullable=False)

    def __init__(self, openID, nickname):
        self.openID = openID
        self.nickname = nickname


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
