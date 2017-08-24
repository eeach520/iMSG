# -*- coding: utf-8 -*-
from flask import Flask
from os import path
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

basedir = path.abspath(path.dirname(__file__))

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.index'
bootstrap = Bootstrap()
moment = Moment()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(basedir, 'data.sqlite')
    app.config['ALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SECRET_KEY'] = 'hard to guess string'
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    from .api import api as api_blueprint
    from .weixin import weixin as weixin_blueprint
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(weixin_blueprint, url_prefix='/weixin')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)
    login_manager.init_app(app)
    return app
