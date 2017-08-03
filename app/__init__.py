# -*- coding: utf-8 -*-
from flask import Flask
from os import path
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager

basedir = path.abspath(path.dirname(__file__))

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(basedir, 'data.sqlite')
    app.config['ALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SECRET_KEY'] = 'hard to guess string'
    db.init_app(app)
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    login_manager.init_app(app)
    return app
