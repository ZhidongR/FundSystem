#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :register.py
# @Time      :10/17/21 10:30 PM
# @Author    :Zhidong R

import json
import os.path
import random
from . import api
from flask import current_app, jsonify, request, g, session, make_response
from iFunds import db, redis_store
from iFunds.models import User
from iFunds.utils.respond_code import RET, error_map
from iFunds.utils.commons import *
from iFunds.utils import create_verify_img


@api.route('/user', methods=["POST"])
def register():
    """
    接受用户的注册请求
    返回结果： 返回登录信息{ 'code':'0','msg':'注册成功'}
    """
    # 1. 获取参数
    json_data = json.loads(request.data)
    user_name = json_data.get("name")
    phone = json_data.get("phone")
    password1 = json_data.get("password1")
    password2 = json_data.get("password2")
    client_verify_code = json_data.get("image_code")
    uuid = json_data.get("uuid") # 用于获取redis中图片验证码

    # 2. 检查数据
    if not all([user_name, phone, password1, password2, client_verify_code]):
        return jsonify(code=RET.PARAMERR, msg=error_map.get(RET.PARAMERR))
    if password1 != password2:
        return jsonify(code=RET.PARAMERR, msg="两次密码不一致")

    # 3. 校验数据
    try:
        db.session.commit()
        user = User.query.filter_by(phone=phone).first()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, msg=error_map.get(RET.DBERR))
    if user:
        return jsonify(code=RET.USERERR, msg="该手机号用户已注册")
    del user
    # 验证码校验
    try:
        server_verify_code = redis_store.get('ImageCode_' + uuid)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, msg=error_map.get(RET.DBERR))
    if not server_verify_code:
        return jsonify(code=RET.USERERR, msg="图片验证码已过期,请刷新图片验证码")
    if client_verify_code != server_verify_code:
        current_app.logger.debug("client_verify_code:%s  server_verify_code:%s" % (client_verify_code, server_verify_code))
        return jsonify(code=RET.USERERR, msg="验证码不对")

    # 4. 数据库、redis、session的处理
    user = User()
    user.name = user_name
    user.phone = phone
    user.password_hash = password1
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, msg=error_map.get(RET.DBERR))

    # 5. 返回结果
    return jsonify(code=RET.OK, msg="用户注册成功")


@api.route("/verify_img", methods=["GET"])
def get_image_code():
    """
    接受用户的请求,用户需要给uuid,
    接收请求，获取UUID和上一个uuid。
    return: 验证码图片
    """
    # 用于提供客户端图片验证码
    # 1.接收请求，获取uuid和上一个uuid
    uuid = request.args.get("uuid")
    last_uuid = request.args.get("last_uuid")
    if not uuid:
        return jsonify(code=RET.PARAMERR, msg=error_map.get(RET.PARAMERR))
    # 2.生成图片验证码
    verify_code, image_jpeg = create_verify_img.create_verify_code_and_img()
    # 3.检查上一个uuid是否存在，存在则删除；保存新的uuid，对应的图片文本信息
    try:
        if last_uuid:
            redis_store.delete('ImageCode_' + last_uuid)
        # 3.保存UUID对应的验证码文字信息,设置时长
        redis_store.set('ImageCode_' + uuid, verify_code, REDIS_VERIFY_CODE_EX_TIME)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(code=RET.DBERR, msg='保存图片验证码失败')

    # 返回验证码图片
    # data = base64.b64encode(image_jpeg.getvalue()).decode()
    response = make_response(image_jpeg.getvalue())
    response.headers['Content-Type'] = 'image/jpeg'
    return response


# @api.route('/verify_code', methods=["GET"])
# def get_verfiy_code():
#     """
#     接受用户的手机验证码
#     返回结果： 返回验证码{ 'code':'0','msg':'获取验证码成功',verify_code':'123456'}
#     """
#     # http://127.0.0.1:5000?phone=xxx&uuid=xxxx
#
#     # 1. 获取参数
#     phone = request.args.get("phone")
#     uuid = request.args.get("uuid")# uuid是用于检查图片验证码的，但当前没做，所以预留
#
#     # 2. 检查参数
#     if not all([phone, uuid]):
#         return jsonify(code=RET.PARAMERR, msg=error_map.get(RET.PARAMERR))
#     try:
#         user = User.query.filter(User.phone == phone).first()
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(code=RET.DBERR, msg=error_map.get(RET.DBERR))
#
#     # 3. 校验参数:检查数据库是否存在该用户
#     if user:
#         return jsonify(code=RET.USERERR, msg=u"用户已注册")
#     del user
#
#     # 4. 生成验证码，发送验证码，并写入redis
#     verify_code = "%06d" % random.randint(0, 999999)
#     current_app.logger.debug("验证码是%s" % verify_code)
#     uuid_str = "verify_code_%s" % phone
#
#     # TODO 发送验证码，并检查是否成功？
#     try:
#         # redis_store.add(uuid_str, verify_code, REDIS_VERIFY_CODE_EX_TIME)
#         redis_store.set(uuid_str, verify_code, REDIS_VERIFY_CODE_EX_TIME)
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(code=RET.DBERR, msg=error_map.get(RET.DBERR))
#
#     # 5. 返回结果
#     return jsonify(code='0', msg=u"获取验证码成功", data={"verify_code": verify_code})





