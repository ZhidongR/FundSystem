#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :trace.py.py
# @Time      :4/12/22 12:27 PM
# @Author    :Zhidong R

from __future__ import division
import json, time
from . import api
from flask import current_app, jsonify, request, g, session
from datetime import datetime
from sqlalchemy import or_, and_
from iFunds import db, redis_store
from iFunds.models import User, Fund, TraceRecord, UserFundHold
from iFunds.utils.respond_code import RET, error_map
from iFunds.utils.fund_data import FundData
from iFunds.utils.commons import login_required, REDIS_VERIFY_CODE_EX_TIME
from iFunds.utils.transform import str_to_dlt


@api.route("/trace", methods=["POST"])
@login_required
def post_fund_trace():
    """
    接受用户的基金购买或出售的交易请求
    输入参数：基金代号，购买出售标志位，购买金额，出售份数，
            例子，购买000001基金10000.55元，{"fund_code":"320007","buy_flag":"1","buy_money":5555.99}
            出售000001基金10000.55元，{"fund_code":"320007","sale_flag":"1","sale_num":8999.56}
    :return: 状态码code,msg请求信息，记录数据data,一下为两个例子
    data={"fund_code":"165525","buy_money":10000.99,"accept_time":"20220101 14:50:00"}
    data={"fund_code":"165525","sale_num":8999.56,"accept_time":"20220101 14:50:00"}
    """
    # 1.获取参数
    json_data = json.loads(request.data)
    fund_code = json_data.get("fund_code")
    buy_flag = json_data.get("buy_flag")
    buy_money = json_data.get("buy_money")
    sale_flag = json_data.get("sale_flag")
    sale_num = json_data.get("sale_num")
    user_id = g.user_id
    re_data = {}  # 返回的数据字典
    # 检查数据库中是否存在该基金
    db.session.commit()
    fund = Fund.query.filter_by(fund_code=fund_code).first()
    fund_id, fund_code, fund_name = fund.id, fund.fund_code, fund.fund_name

    if not fund_id:
        return jsonify(code=RET.NODATA, msg="基金代号%s不存在" % fund_code)

    # 2.检查参数并处理购买操作
    if buy_flag and buy_flag == "1":
        if not all([fund_code, buy_flag, buy_money]):
            return jsonify(code=RET.PARAMERR, msg=error_map.get(RET.PARAMERR))

        # 数据库事务操作
        try:
            # 用户余额获取，进行用户余额的扣除
            user = User.query.filter_by(id=user_id).first()
            balance_after_buy = user.balance - buy_money
            if balance_after_buy < 0:  #
                return jsonify(code=RET.DATAERR, msg="用户余额不足")
            trace_record = TraceRecord()
            trace_record.user_id = user_id
            trace_record.fund_id = fund_id
            trace_record.fund_code = fund_code
            trace_record.fund_name = fund_name
            trace_record.buy_or_sale = "buy"
            trace_record.buy_money = buy_money
            t_now = datetime.now()
            trace_record.application_time = t_now
            User.query.filter(User.id == user_id).update({User.balance: balance_after_buy})
            db.session.add(trace_record)
            db.session.commit()
            re_data["fund_code"] = fund_code
            re_data["buy_money"] = buy_money
            re_data["accept_time"] = t_now
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, msg=error_map.get(RET.DBERR))
        return jsonify(code=RET.OK, msg="OK", data=re_data)

    # 3.检查参数并处理出售操作
    if sale_flag and sale_flag == "1":
        if not all([fund_code, sale_flag, sale_num]):
            return jsonify(code=RET.PARAMERR, msg=error_map.get(RET.PARAMERR))
        # 数据库事务操作
        db.session.commit()
        try:
            hold_fund = UserFundHold.query.filter(UserFundHold.hold_num > 0,
                                                  UserFundHold.user_id == user_id,
                                                  UserFundHold.fund_id == fund_id).first()
            if not hold_fund:
                return jsonify(code=RET.DATAERR, msg="当前用户没有持有该基金")
            hold_num = hold_fund.hold_num
            if hold_num-sale_num < 0:
                return jsonify(code=RET.DATAERR, msg="当前持有量为%s，要求卖出量为%s,持有量<要求卖出量" % (hold_num, sale_num))
            hold_fund.hold_num = hold_num-sale_num
            hold_fund.deal_flag = 1

            trace_record = TraceRecord()
            trace_record.user_id = user_id
            trace_record.fund_id = fund_id
            trace_record.fund_code = fund_code
            trace_record.fund_name = fund_name
            trace_record.buy_or_sale = "sale"
            trace_record.sale_number = sale_num
            t_now = datetime.now()
            trace_record.application_time = t_now.now()
            db.session.add(trace_record)
            db.session.commit()
            re_data["fund_code"] = fund_code
            re_data["sale_num"] = sale_num
            re_data["accept_time"] = t_now
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return jsonify(code=RET.DBERR, msg=error_map.get(RET.DBERR))

        return jsonify(code=RET.OK, msg="OK", data=re_data)

    if buy_flag != "1" or sale_flag != "1":
        return jsonify(code=RET.DATAERR, msg='buy_flag或sale_flag为非"1",请修改好参数再访问')

@api.route("/trace", methods=["GET"])
@login_required
def get_fund_trace():
    """
    获取用户的基金购买或出售的交易记录请求
    输入参数：天数，默认七天内
    :return: 状态码code,msg请求信息，记录数据data,一下为两个例子
    data={'fund_code': '信诚中证基建工程指数(LOF)A', 'fund_name': '信诚中证基建工程指数(LOF)A', 'buy_money': None, 'sale_number': None, 'application_time': datetime.datetime(2022, 4, 12, 19, 26, 54), 'status': '0', 'trace_price': None, 'price_time': None, 'trace_amount': None, 'trace_time': None}
    }
    """
    # 1.获取参数
    days = request.args.get("days", 7)
    user_id = g.user_id
    re_data = []  # 返回的列表，元素为字典
    db.session.commit()
    ls_trace_record = TraceRecord.query.filter((TraceRecord.user_id == user_id)).all()
    if not ls_trace_record:
        return jsonify(code=RET.NODATA, msg="数据库不存在满足的数据")
    for record in ls_trace_record:
        re_data.append(record.to_dict())
    return jsonify(code=RET.OK, msg="OK", data=re_data)
