# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: ZhidongR
@software: PyCharm
@file: __init__.py.py
@time: 2021/10/14 21:23
"""

from flask import Blueprint

# 创建蓝图对象
# api = Blueprint("api_1_0", __name__)
api = Blueprint('api_1_0', __name__, url_prefix='/api/1.0')

# 导入蓝图的视图
from . import demoa, register, session, funds, profile, trace, news

