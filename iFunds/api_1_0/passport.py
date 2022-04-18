#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :passport.py
# @Time      :10/17/21 9:17 PM
# @Author    :Zhidong R
# 废弃的函数，没用的
# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: ZhidongR
@software: PyCharm
@file: demoa.py.py
@time: 2021/10/14 21:26
"""

from . import api
from flask import current_app, jsonify, request, g, session
from iFunds import db
from iFunds.models import User
from iFunds.utils.respond_code import RET, error_map


@api.route('/login', methods=["POST"])
def login():
    """
    接受用户的登录请求
    返回结果： 返回登录信息{ 're_code':'0','msg':'登录成功'}
    """
    # 1.获取参数
    json_data = request.json
    phone = json_data.get("user")
    password = json_data.get("password")
    # 2.检查参数
    if not all([phone, password]):
        current_app.logger.error("参数不全")
        return jsonify(rs_code=RET.NODATA, msg=error_map.get(RET.NODATA))

    # 3. 校验参数
    try:
        user = User.query.filter(User.phone == phone).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(rs_code=RET.DBERR, msg=error_map.get(RET.DBERR))
    if not (user and user.check_password(user.password)):
        current_app.logger.error("error msg")
        return jsonify(re_code=RET.PARAMERR, msg='存在账号或密码错误')

    # 4. 数据库，redis，session处理
    session['user_id'] = user.id
    session['name'] = user.name
    session['phone'] = user.phone

    # 5. 返回结果
    return jsonify(re_code='0', msg='登录成功')

