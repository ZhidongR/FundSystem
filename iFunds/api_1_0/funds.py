#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :funds.py.py
# @Time      :10/18/21 11:31 PM
# @Author    :Zhidong R

import json, time
from . import api
from flask import current_app, jsonify, request, g, session
from iFunds import db, redis_store
from iFunds.models import User, Fund, UserFundForce, UserFundHold
from iFunds.utils.respond_code import RET, error_map
from iFunds.utils.fund_data import FundData
from iFunds.utils.commons import login_required, REDIS_VERIFY_CODE_EX_TIME
from iFunds.utils.transform import str_to_dlt


@api.route("/funds", methods=["POST"])
def get_funds_info():
    """
    获取多个基金信息的接口
    输入参数：基金的list列表，如{fs_code_ls: ["0000001", "0000002",......]}或者{fs_name_ls:[“某某基金1”，“某某基金2”]}
    :return: 状态码code,msg请求信息，基金数据
    data=[
    {"fund_code": "000001", "fund_name":"某某基金"....},
    {"fund_code": "000002", "fund_name":"某某基金"....},
    {"fund_code": "000003", "fund_name":"某某基金"....}
    ]
    """
    # 1.获取参数
    json_data = json.loads(request.data)
    fund_code_ls = json_data.get("fund_code_ls")
    fund_name_ls = json_data.get("fund_name_ls")

    # 2.检查参数
    if (not fund_code_ls) and (not fund_name_ls):
        return jsonify(code=RET.PARAMERR, msg=error_map.get(RET.PARAMERR))
    # 3.校验参数:Nothing can do
    # 4.操作数据库，redis,session
    re_data_ls = []
    error_ls = []
    not_data_ls = []
    if fund_code_ls:
        for fund_code in fund_code_ls:
            try:
                db.session.commit()
                fund = Fund.query.filter_by(fund_code=fund_code).first()
                if not fund:
                    not_data_ls.append(fund_code)
                    continue
                re_data_ls.append(fund.to_dict())
            except Exception as e:
                db.session.rollback()
                error_ls.append(fund_code)
                current_app.logger.error("%s:读取fund_code[%s]出现异常:%s" % (__name__, fund_code, e))


    if fund_name_ls:
        for fund_name in fund_name_ls:
            try:
                db.session.commit()
                fund = Fund.query.filter_by(fund_name=fund_name).first()
                if not fund:
                    if not fund:
                        not_data_ls.append(fund_name)
                        continue
                re_data_ls.append(fund.to_dict())
            except Exception as e:
                db.session.rollback()
                error_ls.append(fund_name)
                current_app.logger.error("%s:读取fund_name[%s]出现异常%s" % (__name__, fund_name, e))
    # 5.返回结果
    return jsonify(code=RET.OK, msg="获取数据成功", data=re_data_ls, error_ls=error_ls, not_data_ls=not_data_ls)


@api.route("/funds/shishi", methods=["POST"])
def get_fund_guzhi():
    """
    获取估值，输入参数Demo为{“fund_code_ls”：["000001,"000002"]}
    :return: [{},{}]类型的数据列表
    """
    # 1.获取参数
    json_data = json.loads(request.data)
    fund_code_ls = json_data.get("fund_code_ls")
    fund_name_ls = json_data.get("fund_name_ls")

    # 2.检查参数
    if (not fund_code_ls) and (not fund_name_ls):
        return jsonify(code=RET.PARAMERR, msg=error_map.get(RET.PARAMERR))
    # 3.校验参数:Nothing can do
    fund_data = FundData()
    re_ls = []
    for fund_code in fund_code_ls:
        dict_data = fund_data.get_real_fund_data(fund_code)
        if dict_data:
            re_ls.append(re_ls)
    return jsonify(code=RET.OK, msg="OK", data=re_ls)


@api.route("/funds/favourite", methods=["GET"])
@login_required
def get_favourite_funds_info():
    """
    用与获取用户已关注，喜爱的基金信息
    :return: [{}，{}]类型数据列表，每个字典为一个基金信息
    """
    user_id = g.user_id
    try:
        db.session.commit()
        user_fund_force_ls = UserFundForce.query.filter_by(user_id=user_id).all()
        if user_fund_force_ls:
            dict_ls = []
            for user_fund_force in user_fund_force_ls:
                fund_id = user_fund_force.fund_id
                fund = Fund.query.filter_by(id=fund_id).first()
                dict_ls.append(fund.to_dict())
            return jsonify(code=RET.OK, msg="获取用户喜爱的基金信息成功", data=dict_ls)
        else:
            return jsonify(code=RET.OK, msg="用户没有关注/喜爱的基金")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error("%s:出现异常%s" % (__name__, e))
        return jsonify(code=RET.DBERR, msg="读取数据出现异常")


@api.route("/funds/favourite", methods=["POST"])
@login_required
def set_favourite_funds():
    """
    添加用户的喜爱基金
    :return:
    """
    # 1. 获取参数并检查
    user_id = g.user_id
    data_dict = json.loads(request.data)
    favourite_fund_ls = data_dict.get("favourite_fund_ls")
    if not favourite_fund_ls:
        return jsonify(code=RET.PARAMERR, msg="参数不对，请检查")

    # 2.校验参数，并进行数据写入
    success_ls = []
    fail_ls = []
    exist_ls =[]
    not_fund_ls = []
    re_data = {}
    for fund_code in favourite_fund_ls:
        db.session.commit()
        fund = Fund.query.filter_by(fund_code=fund_code).first()
        if fund:
            fund_id = fund.id
            check_exist = UserFundForce.query.filter_by(user_id=user_id, fund_id=fund_id).first()
            if check_exist:
                exist_ls.append(fund_code)
                continue
            user_fund_force = UserFundForce(user_id=user_id, fund_id=fund_id,fund_code=fund_code,fund_name=fund.fund_name)
            try:
                db.session.add(user_fund_force)
                db.session.commit()
                success_ls.append(fund_code)
            except Exception as e:
                db.session.rollback()
                current_app.logger.error("将基金%s添加到数据库user_fund_force出现异常" % fund_code)
                fail_ls.append(fail_ls)
                return jsonify(code=RET.DBERR, msg="操作数据出现异常")
        else:
            not_fund_ls.append(fund_code)
            current_app.logger.info("添加喜爱基金，数据库不存在fund_code=%s的基金" % fund_code)

    success_ls = []
    fail_ls = []
    exist_ls = []
    not_fund_ls = []
    re_data["success"] = success_ls
    re_data["fail"] = fail_ls
    re_data["exist"] = exist_ls
    re_data["not_fund"] = not_fund_ls
    return jsonify(code=RET.OK, msg="success", data=re_data)

@api.route("/funds/favourite", methods=["DELETE"])
@login_required
def remove_favourite_funds():
    """
    删除用户的喜爱基金
    :return:
    """
    # 1. 获取参数并检查
    user_id = g.user_id
    data_dict = json.loads(request.data)
    favourite_fund_ls = data_dict.get("delete_fund_ls")
    if not favourite_fund_ls:
        return jsonify(code=RET.PARAMERR, msg="参数不对，请检查")

    # 2.校验参数，并进行数据操作
    for fund_code in favourite_fund_ls:
        db.session.commit()
        fund = Fund.query.filter_by(fund_code=fund_code).first()
        if fund:
            fund_id = fund.id
            try:
                user_fund_force = UserFundForce.query.filter_by(user_id=user_id, fund_id=fund_id).first()
                if not user_fund_force:
                    continue
                db.session.delete(user_fund_force)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                current_app.logger.error("将基金%s从数据库user_fund_force删除出现异常" % fund_code)
                return jsonify(code=RET.DBERR, msg="操作数据出现异常")
        else:
            current_app.logger.info("添加喜爱基金，数据库不存在fund_code=%s的基金" % fund_code)
    return jsonify(code=RET.OK, msg="success")


@api.route("/funds/hold", methods=["GET"])
@login_required
def get_hold_funds():
    """
    获取用户持有的基金信息
    :return:
    """
    user_id = g.user_id
    try:
        db.session.commit()
        hold_fund_ls = UserFundHold.query.filter(UserFundHold.user_id == user_id,
                                                 UserFundHold.hold_num > 0).all()
        if hold_fund_ls:
            dict_ls = []
            for hold_fund in hold_fund_ls:
                dict_ls.append(hold_fund.to_dict())
            return jsonify(code=RET.OK, msg="获取用户持有的基金信息成功", data=dict_ls)
        else:
            return jsonify(code=RET.OK, msg="用户没有持有的基金",data=[])
    except Exception as e:
        db.session.rollback()
        current_app.logger.error("%s:出现异常%s" % (__name__, e))
        return jsonify(code=RET.DBERR, msg="读取数据出现异常")


def write_redis_time(keyword, str_value):
    t = time.localtime()
    str_now = time.strftime('%04Y%02m%02d%02H%02M%02S', time.localtime())
    key = str.format("{}_{}", keyword, str_now)
    try:
        redis_store.set(key, str_value, REDIS_VERIFY_CODE_EX_TIME)
        return key
    except Exception as e:
        return False


def delete_redis_time(keyword):
    keys = redis_store.keys(keyword + "_*")
    try:
        for key in keys:
            redis_store.delete(key)
    except Exception as e:
        return False


@api.route("/funds/generate", methods=["GET"])
def get_generate_fund_data():
    """
    返回大盘数据
    :return:json
    """
    # 1. 获取参数并检查
    # 2. 校验redis中是否存在未超过的数据？超时时间初步为600s
    #   -是，则直接获取return数据。
    #   -否，删除旧数据，redis增加新数据，return疏浚
    redis_keys = redis_store.keys("generate_fund_*")
    if len(redis_keys) == 1:
        str_key = redis_keys[0]
        time_array = time.strptime(str_key[len(str_key) - 14:len(str_key)], "%Y%m%d%H%M%S")
        key_time = int(time.mktime(time_array))
        now = time.time()
        if now - key_time < 600:
            re_data = str_to_dlt(redis_store.get(str_key))
            return jsonify(code=RET.OK, msg="OK", data=re_data)
        else:
            delete_redis_time("generate_fund")
            key = "generate_fund"
            fund1 = FundData()
            str_value = json.dumps(fund1.get_generate_data(), ensure_ascii=False)
            str_key = write_redis_time(key, str_value)
            try:
                re_data = str_to_dlt(redis_store.get(str_key))
                # print(re_data)
                return jsonify(code=RET.OK, msg="OK", data=re_data)
            except Exception as e:
                return jsonify(code=RET.DATAERR, msg="数据库redis存在错误")
    else:
        delete_redis_time("generate_fund")
        key = "generate_fund"
        fund1 = FundData()
        str_value = json.dumps(fund1.get_generate_data(), ensure_ascii=False)
        str_key = write_redis_time(key, str_value)
        try:
            re_data = str_to_dlt(redis_store.get(str_key))
            # print(re_data)
            return jsonify(code=RET.OK, msg="OK", data=re_data)
        except Exception as e:
            return jsonify(code=RET.DATAERR, msg="数据库redis存在错误")
