# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: ZhidongR
@software: PyCharm
@file: config.py
@time: 2021/10/14 19:40
"""
import redis
from celery.schedules import crontab

class Config(object):
    """配置信息"""
    DEBUG = True

    SECRET_KEY = "11111xxxxfsagdsgD"
    """mysql://username:password@server/db"""
    mysql_user = "root"
    mysql_password = "123456"
    mysql_ip = "127.0.0.1"
    mysql_port = "3306"
    mysql_database_name = "fund_system"

    SQLALCHEMY_DATABASE_URI = r'mysql+pymysql://root:123456@127.0.0.1:3306/fund_system'
    # SQLALCHEMY_DATABASE_URI = r'mysql+pymysql://%s:%s@%s：%s/%s' %\
    #                           (mysql_user, mysql_password, mysql_ip, mysql_port, mysql_database_name)
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_DECODE_RESPONSES = True  # 需要设置decode_responses为True才能redis操作能正常解码
    REDIS_CAHRSET= 'UTF-8'
    REDIS_ENCODING ='UTF-8'

    # flask-session配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏
    PERMANENT_SESSION_LIFETIME = 86400  # session数据有效期一天 86400s

    # 是否支持开启多线程，默认为False，不开启
    threaded = True

    # processes，进程数量，默认为1，多线程和多进程只能同时开启一个
    # processes = 5

    # celery的配置
    from datetime import timedelta
    broker_url = r"redis://127.0.0.1:6379/3"
    # 结果存储地址
    # CELERY_RESULT_BACKEND = r"redis://127.0.0.1:6379/3"
    result_backend = r"redis://127.0.0.1:6379/4"
    # 任务序列化方式, 4.0版本后默认为json
    # CELERY_TASK_SERIALIZER ='json'
    task_serializer = "json"

    #  任务执行结果序列化方式
    serializer = 'json'
    #  任务结果保存时间，超过这个会删除结果
    result_expires = 60 * 60 * 5
    # 指定任务接受的内容类型(序列化),默认值：Default: {'json'} (set, list, or tuple). 按需要可以变成['application/json']
    accept_content = {'json'}
    # 时区
    timezone = "Asia/Shanghai"
    enable_utc = True
    worker_concurrency = 5  # celery worker并发数
    worker_max_tasks_per_child = 5  # 每个worker最大执行任务数

    # 避免返回前端数据自动排序
    JSON_SORT_KEYS = False
    # 设置定时任务
    beat_schedule = {
        'add-every-30-seconds': {
            'task': 'iFunds.tasks.use_task_update',
            'schedule': crontab(hour=23, minute=52, day_of_week=2),  # 10.0
            'args': None
        }
    }


class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    DEBUG = True


class ProductConfig(Config):
    """生产环境配置信息"""
    DEBUG = False


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductConfig
}
