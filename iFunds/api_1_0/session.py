#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :session.py.py
# @Time      :10/18/21 8:46 PM
# @Author    :Zhidong R

import json
from . import api
from flask import current_app, jsonify, request, g, session
from iFunds import db
from iFunds.models import User
from iFunds.utils.respond_code import RET, error_map
from iFunds.utils.commons import login_required


@api.route('/sessions', methods=["POST"])
def login():
    """
    接受用户的登录请求
    返回结果： 返回登录信息{ 'code':'0','msg':'登录成功'}
    """
    # 1.获取参数
    json_data = json.loads(request.data)
    phone = json_data.get("phone")
    password = json_data.get("password")
    # 2.检查参数
    if not all([phone, password]):
        current_app.logger.error("参数不全")
        return jsonify(code=RET.NODATA, msg=error_map.get(RET.NODATA))

    # 3. 校验参数
    try:
        user = User.query.filter_by(phone=phone).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, msg=error_map.get(RET.DBERR))
    if not user:
        current_app.logger.error("%s: not user:%s" % (__name__, phone))
    if not (user and user.check_password(password)):
        current_app.logger.error("error msg")
        return jsonify(code=RET.PARAMERR, msg='存在账号或密码错误')

    # 4. 数据库，redis，session处理
    try:
        session['user_id'] = user.id
        session['name'] = user.name
        session['phone'] = user.phone
    except Exception as e:
        current_app.logger.error("%s:%s" % (__name__, e) )
    # 5. 返回结果
    return jsonify(code=RET.OK, msg='登录成功')


@login_required
@api.route('/sessions', methods=['GET'])
def check_login_status():
    """
    获取用户登录的状态
    """
    name = session.get("name")
    if name is not None:
        return jsonify(code=RET.OK, msg='已登录', data={"name": name})
        current_app.logger.info("当前登录的name为%s" % name)
    else:
        current_app.logger.info("当前没有用户登录")
        return jsonify(code=RET.SESSIONERR, msg="用户未登录")


@api.route('/sessions', methods=['DELETE'])
@login_required
def logout():
    """
    接受用户的退出登录请求
    返回结果： 返回退出登录信息{ 'code':'0','msg':'退出登录成功'}
    """
    try:
        session.pop("user_id", None)
        session.pop('name')
        session.pop('phone')
        session.clear()
    except Exception as e:
        current_app.logger.error("%s:%s" % (__name__, e))
        return jsonify(code=RET.DBERR, msg='操作session出现异常')
    # 5. 返回结果
    return jsonify(code=RET.OK, msg='退出登录成功')
