#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :user_fund_force.py
# @Time      :10/16/21 11:19 AM
# @Author    :Zhidong R

import datetime
from iFunds import db
from .base import BaseModel


class UserFundForce(BaseModel, db.Model):
    # 定义表名字
    __tablename__ = "user_fund_force"
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    fund_id = db.Column(db.Integer, db.ForeignKey('fund.id'), index=True)
    fund_code = db.Column(db.String(64))
    fund_name = db.Column(db.String(64))
