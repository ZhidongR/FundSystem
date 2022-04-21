# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: ZhidongR
@software: PyCharm
@file: __init__.py
@time: 2021/10/14 20:57
"""
import redis
import config
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from logging.handlers import RotatingFileHandler
from iFunds import celery_config


def init_log():
    """初始化日志"""
    logging.basicConfig(level=logging.DEBUG) #调试Debug级别
    #创建日志记录器，指明日志保存的路径，每个文件最大大小，保存日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/logs", maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录格式
    formatter = logging.Formatter("%(levelname)s %(filename)s:%(lineno)d %(message)s")
    file_log_handler.setFormatter(formatter)

    # 为全局的日志工具对象（flask app） 添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


# 初始化日志
init_log()

# 创建数据库
db = SQLAlchemy()

# my_celery = make_celery(__name__)

# 创建redis链接对象
redis_store = None

# 为flask补充 csrf防护机制
csrf = CSRFProtect()

# 工厂模式
def create_app(config_name, **kwargs):
    """
    创建flask的应用对象
    :param config_name:str,配置模式的名字，可选值“develop”,"product"
    :return: flask的Flask对象
    """
    from . import models
    app = Flask(__name__)
    # 根据配置模式的名字获取获取配置参数的类
    config_class = config.config_map.get(config_name)
    app.config.from_object(config_class)

    # 使用app初始化db
    # from iFunds.models import User, Fund, user_fund
    db.init_app(app)

    # initial celery
    if kwargs.get('celery'):
        init_celery(kwargs['celery'], app)

    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT,
                                    decode_responses=config_class.REDIS_DECODE_RESPONSES,
                                    charset=config_class.REDIS_CAHRSET, encoding=config_class.REDIS_ENCODING)

    # 为flask补充csrf防护机制
    csrf.init_app(app)

    # 利用flask的session,将redis的数据保存在session中
    Session(app)

    # 自定义转换器加入到默认转换器列表中
    from .utils.commons import RegexConverter
    app.url_map.converters['re'] = RegexConverter

    # 注册蓝图
    from . import api_1_0
    from .static_html import static_html
    app.register_blueprint(api_1_0.api)
    app.register_blueprint(blueprint=static_html)
    return app

def init_celery(celery, app):
    """
    initial celery object wraps the task execution in an application context
    :param celery: Celery()
    :param app: Flask
    :return: None
    """
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask

