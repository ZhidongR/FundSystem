#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :__init__.py.py
# @Time      :10/16/21 12:44 AM
# @Author    :Zhidong R

from .base import db
from .user import User
from .fund import Fund
from .user_fund_force import UserFundForce
from .trace_record import TraceRecord
from .user_fund_hold import UserFundHold

def init_app(app):
    db.init_app(app)
