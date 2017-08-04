from . import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, nullable=False)


class Wechat_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String, nullable=True)
    openID = db.Column(db.String, nullable=False)


class Temp_token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp_access_token = db.Column(db.String, nullable=False)


@login_manager.user_loader
def user_load(user_id):
    return User.query.get(int(user_id))
