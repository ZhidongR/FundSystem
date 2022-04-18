#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :user.py.py
# @Time      :10/16/21 12:44 AM
# @Author    :Zhidong R

from datetime import datetime
from iFunds import db
from .base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel, db.Model):
    # 定义表名字
    __tablename__ = "user"
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    phone = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(1024))

    balance = db.Column(db.Float, default=100000.00)
    last_profit = db.Column(db.Float, default=0)
    hold_fund_amount = db.Column(db.Float, default=0) # 持有基金金额
    hold_fund_profit = db.Column(db.Float, default=0)
    current_time = db.Column(db.DateTime)

    @property
    def password_hash(self):
        raise AttributeError(u'不能访问该属性')

    @password_hash.setter
    def password_hash(self, value):
        # 生成hash密码
        self.password = generate_password_hash(value)

    def check_password(self, password):
        # 校验密码是否正确
        return check_password_hash(self.password, password)

    def to_dict(self):
        # 返回一个用户信息字典接口，使外界方便调用
        user_info = {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'balance': self.balance,
            'last_profit': self.last_profit,
            'hold_fund_amount': self.hold_fund_amount,
            'hold_fund_profit': self.hold_fund_profit,
            'current_time': self.current_time,
        }
        return user_info
