#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :celery_config.py
# @Time      :10/21/21 5:09 PM
# @Author    :Zhidong R


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

# 设置定时任务
beat_schedule = {
    'add-every-30-seconds': {
        'task': 'iFunds.Tasks.UpdateData.tasks.update_fund_data',
        'schedule': timedelta(seconds=10),  # 10.0
        'args': ([["379010", "379020", "260108", "161725"]])
    },
}