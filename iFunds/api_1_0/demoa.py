# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: ZhidongR
@software: PyCharm
@file: demoa.py.py
@time: 2021/10/14 21:26
"""

from . import api
from flask import current_app
from iFunds import db
from iFunds.models import User


# @api.route('/')
# def index():
#     current_app.logger.error("error msg")
#     current_app.logger.warn("warn msg")
#     current_app.logger.debug("debug msg")
#     return 'Hello Index'

@api.route('/1')
def index1():
    with current_app.app_context():
        # db.drop_all()
        # db.create_all()
        # user = User(name="hello 大佬22223333")
        # db.session.add(user)
        # db.session.commit()
        current_app.logger.debug("data added1")
    current_app.logger.debug("before return")
    return 'Hello Flask'
