#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :main_app.py
# @Time      :10/21/21 4:56 PM
# @Author    :Zhidong R

from iFunds import db, celery_app
from iFunds.Tasks import celery_config
from iFunds import db, celery_app

celery_app.config_from_object(celery_config)
# celery_app.conf.update(celery_config)
celery_app.autodiscover_tasks(['iFunds.Tasks.UpdateData'], force=True)
celery_app.start()
