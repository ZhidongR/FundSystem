# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: ZhidongR
@software: PyCharm
@file: manage.py
@time: 2021/10/14 19:32
"""
import os
import config
from iFunds import create_app, db, celery_config
from flask_migrate import Migrate
from celery import Celery


def make_celery(app_name):
    # broker = getattr(config[os.getenv('FLASK_ENV') or 'default'], "broker_url")
    # backend = getattr(config[os.getenv('FLASK_ENV') or 'default'], "result_backend")
    broker = celery_config.broker_url
    backend = celery_config.result_backend

    celery = Celery(
        app_name,
        # broker=broker,
        # backend=backend
    )
    celery.autodiscover_tasks(["iFunds.tasks"])
    celery.config_from_object(celery_config)
    return celery


my_celery = make_celery(__name__)

# 创建Flask对象
app = create_app("product", celery=my_celery)
app.app_context().push()

# 让迁移时，app和db建立关联
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()
