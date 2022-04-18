#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :profile.py
# @Time      :10/29/21 10:44 AM
# @Author    :Zhidong R

from . import api
from flask import current_app, g, session, jsonify
from iFunds import db, redis_store
from iFunds.utils.commons import login_required
from iFunds.utils.respond_code import RET
from iFunds.models import *


@api.route('/user', methods=["GET"])
@login_required
def get_user_info():
    """获取用户信息:
    1.登录校验  @login_required
    2.g变量中获取user_id
    3.查询user
    :return: 返回响应，用户信息
    """
    user_id = g.user_id
    if not user_id:
        return jsonify(code=RET.USERERR, msg="用户未登录")
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error("%s:%s" % (__name__, e))
        return jsonify(code=RET.DBERR, msg="查询用户信息异常失败")
    if not user:
        return jsonify(re_code=RET.NODATA, msg='用户不存在')
    user_info = user.to_dict()
    return jsonify(code=RET.OK, msg="获取用户信息成功", data=user_info)
