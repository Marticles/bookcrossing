from flask import Flask
from app.models.book import db
from flask_login import LoginManager
from flask_mail import Mail
from app.models import *

login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)


    mail.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'web.login'#这两句是未登录情况下重定向到登录页面
    login_manager.login_message = '请先登录或注册'
    db.init_app(app)  #db与核心对象app关联
    db.create_all(app=app) #生成数据表
    # with app.app_context():#生成数据表
    #     db.create_all()#生成数据表
    return app

def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)