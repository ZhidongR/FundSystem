#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :tasks.py.py
# @Time      :10/21/21 7:27 PM
# @Author    :Zhidong R

from __future__ import division
import time
import iFunds
from datetime import datetime
from manage import my_celery as celery
from iFunds.models import User, Fund, UserFundForce, TraceRecord, UserFundHold
from iFunds.utils import FundData
from iFunds import db
from flask import current_app, jsonify, request, g, session


@celery.task()
def update_fund_data(fund_data_ls):
    """
    更新fund数据库中的基金信息，存在该基金则则更新，不存在则创建
    :param fund_data_ls:基金代号list ，如["000001", "000002"]
    :return:  True of False
    """

    if not fund_data_ls:
        return False
    fund_data_cls = FundData()
    for fs_code in fund_data_ls:
        # df = self.get_detail_data(fs_code=fs_code)  # 返回数据为pd.DataFrame()类型
        # 更改方案成：有则更新，无则插入操作
        try:
            dict_data = fund_data_cls.get_detail_data(fund_code=fs_code)  # 已修改为dict
            if not dict_data:
                continue
            fund = Fund.query.filter_by(fund_code=dict_data.get("fund_code")).first()
            if fund:
                Fund.query.filter(Fund.fund_code == dict_data.get("fund_code")).update(dict_data)
                db.session.commit()
                current_app.logger.debug("%s:update fund data bt updating %s" % (__name__, fs_code))
            else:
                fund = Fund()
                fund.set_para_from_dict(dict_data)
                db.session.add(fund)
                db.session.commit()
                current_app.logger.debug("%s:update fund data bt adding %s" % (__name__, fs_code))
            del fund
        except Exception as e:
            current_app.logger.error("%s: %s" % (__name__, e))
            current_app.logger.error("%s: %s" % (__name__, "发生异常的Fund_code为%s" % fs_code))
    return True


@celery.task()
def update_all_fund_data():
    """
    更新fund数据库中的基金信息，存在该基金则则更新，不存在则创建
    :param fund_data_ls:基金代号list ，如["000001", "000002"]
    :return:  True of False
    """

    fund_data_cls = FundData()
    fund_data_ls = list(fund_data_cls.get_all_funds(fund_data_cls).keys())
    for fs_code in fund_data_ls:
        dict_data = fund_data_cls.get_detail_data(fund_code=fs_code)  # 已修改为dict
        # 将数据写入数据库中， 存在弊端，不能实现有则更新，无则插入操作
        # pd.io.sql.to_sql(frame=df, name='fund', con=your_connect, schema='fund_system', if_exists='append', index=False) #chunksize=10000
        # 更改方案成：有则更新，无则插入操作
        current_app.logger.info(fs_code)
        try:
            if not dict_data:
                continue
            fund = Fund.query.filter_by(fund_code=dict_data.get("fund_code")).first()
            if fund:
                Fund.query.filter(Fund.fund_code == dict_data.get("fund_code")).update(dict_data)
                db.session.commit()
                current_app.logger.info("%s:update fund data bt updating %s" % (__name__, fs_code))
                current_app.logger.debug("数据库中%s基金更新" % fs_code)
            else:
                fund = Fund()
                fund.set_para_from_dict(dict_data)
                db.session.add(fund)
                db.session.commit()
                current_app.logger.info("%s:update fund data bt adding %s" % (__name__, fs_code))
                current_app.logger.debug("数据库中%s基金新增" % fs_code)
            del fund
        except Exception as e:
            current_app.logger.error("%s: %s" % (__name__, e))
    return True


@celery.task()
def log(message):
    print(message)
    return message


@celery.task()
def use_task_update():
    fund_data_cls = FundData()
    fund_code_dict = FundData.get_all_funds(fund_data_cls)
    # current_app.logger.info("共有{}个基金，将进行更新" % len(fund_code_dict))
    for fund_code in fund_code_dict:
        dict_temp = [fund_code]
        update_fund_data.delay(dict_temp)
    current_app.logger.info("任务发布完毕")


@celery.task()
def deal_sale_record():
    """
    处理用户卖基金的的交易记录，计算卖出金额，并更新用户的余额和收益
    :return:  True of False
    """
    """
    1. 从trace_record表中获取status=0 and buy_or_sale="sale"的行，形成记录list,对list中每个元素做2-5操作
    2. 根据fund_id和user_id从用户持有基金user_fund_hold中获取需要持有基金记录，更新持有基金的收益，持有金额，成本，deal_flag置0
    3. 根据fund_id从fund数据表中获取最新的价格trace_price，price_time
    4. 根据user_id将卖出的金额累加到用户的余额balance中。
    5. 修改trace_record的status=1，更新trace_price，price_time，trace_num，,trace_total,trace_time
    """
    record_ls = TraceRecord.query.filter(TraceRecord.status == 0, TraceRecord.buy_or_sale == "sale").all()
    if not record_ls:
        current_app.logger.info("数据库user_fund_trace中已经无需要处理的出售数据")
        return False
    for record in record_ls:
        fund_id = record.fund_id
        user_id = record.user_id
        record_id = record.id
        try:
            trace_num = record.sale_number
            hold_fund = UserFundHold.query.filter(UserFundHold.user_id == user_id,
                                                  UserFundHold.fund_id == fund_id).first()

            fund = Fund.query.filter(Fund.id == fund_id).first()
            trace_price, price_time = fund.current_price, fund.price_time
            trace_total = trace_price * trace_num
            t_now = datetime.now()
            # 更新Hold_fund
            hold_fund.current_amount = hold_fund.hold_num * hold_fund.current_price
            hold_fund.cost = hold_fund.cost - trace_num * hold_fund.current_price
            hold_fund.current_profit = hold_fund.current_amount - hold_fund.cost
            hold_fund.deal_flag = 0
            # 更新用户余额
            before_balance = User.query.filter(User.id == user_id).first().balance
            after_balance = before_balance + trace_total
            User.query.filter(User.id == user_id).update({"balance": after_balance})
            # 更新record
            TraceRecord.query.filter(TraceRecord.id == record_id).update({"trace_price": trace_price,
                                                                          "trace_num": trace_num,
                                                                          "price_time": price_time,
                                                                          "trace_total": trace_total,
                                                                          "trace_time": t_now,
                                                                          "status": 1})

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("%s: %s" % (__name__, e))


@celery.task()
def deal_buy_record():
    """
    处理用户买基金的的交易记录，计算买入份数，并更新用户的持有基金
    :return:  True of False
    """
    """
    1. 从trace_record表中获取status=0 and buy_or_sale="buy"的行，形成记录list
    2. 遍历记录list，
        根据fund_id从fund数据表中获取最新的价格trace_price，price_time
    3. 修改trace_record的status=1，更新trace_price，price_time，trace_num，trace_time
    4. 往user_hold_fund表中添加或跟新持有基金的表：user_id,fund_id,fund_code,fund_name,hold_num,收益，成本，持有金额等，deal_flag置0
    """
    record_ls = TraceRecord.query.filter(TraceRecord.status == 0, TraceRecord.buy_or_sale == "buy").all()
    if not record_ls:
        current_app.logger.info("数据库user_fund_trace中已经无需要处理的购买数据")
        return False
    for record in record_ls:
        fund_id = record.fund_id
        user_id = record.user_id
        fund_code = record.fund_code
        fund_name = record.fund_name
        record_id = record.id
        application_time = record.application_time
        try:
            buy_money = record.buy_money
            fund = Fund.query.filter(Fund.id == fund_id).first()
            trace_price, price_time = fund.current_price, fund.price_time
            trace_num = buy_money / trace_price
            trace_total = buy_money
            t_now = datetime.now()
            TraceRecord.query.filter(TraceRecord.id == record_id).update({"trace_price": trace_price,
                                                                          "trace_num": trace_num,
                                                                          "price_time": price_time,
                                                                          "trace_total": trace_total,
                                                                          "trace_time": t_now,
                                                                          "status": 1})
            # 查hold_fund表，存在user_id和fund_id的记录，进行update，不存在则增加
            hold_fund = UserFundHold.query.filter(UserFundHold.user_id == user_id,
                                                  UserFundHold.fund_id == fund_id).first()
            if hold_fund:
                # 更新操作
                hold_fund.hold_num += trace_num
                hold_fund.cost += trace_total
                hold_fund.current_amount = hold_fund.hold_num * trace_price
                hold_fund.deal_flag = 1
                hold_fund.update_time = t_now
            else:
                hold_fund = UserFundHold()
                hold_fund.user_id = user_id
                hold_fund.fund_id = fund_id
                hold_fund.fund_code = fund_code
                hold_fund.fund_name = fund_name
                hold_fund.hold_num = trace_num
                hold_fund.cost = trace_total

                hold_fund.current_price = trace_price
                hold_fund.price_time = price_time
                hold_fund.current_amount = hold_fund.hold_num * hold_fund.current_price
                hold_fund.current_profit = hold_fund.current_amount - hold_fund.cost
                hold_fund.deal_flag = 1

                hold_fund.buy_price = trace_price
                hold_fund.buy_price_time = price_time
                hold_fund.buy_amount = buy_money
                hold_fund.buy_time = application_time
                db.session.add(hold_fund)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("%s: %s" % (__name__, e))


@celery.task()
def update_hold_fund_info():
    hold_fund_ls = UserFundHold.query.filter(UserFundHold.hold_num > 0).all()
    for hold_fund in hold_fund_ls:
        try:
            fund_id = hold_fund.fund_id
            fund = Fund.query.filter(Fund.id == fund_id).first()
            current_price, price_time = fund.current_price, fund.price_time

            hold_fund.last_price = hold_fund.current_price
            hold_fund.last_time = hold_fund.price_time
            hold_fund.current_price = current_price
            hold_fund.price_time = price_time
            hold_fund.current_amount = hold_fund.current_price * hold_fund.hold_num
            hold_fund.current_profit = hold_fund.current_amount - hold_fund.cost
            hold_fund.lastday_profit = (hold_fund.current_price - hold_fund.last_price) * hold_fund.hold_num
            hold_fund.update_time = datetime.now()
            hold_fund.deal_flag = 0
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("%s: %s" % (__name__, e))



@celery.task()
def update_user_fund_info():
    user_ls = User.query.all()
    if not user_ls:
        current_app.logger.info("%s: %s" % (__name__, "User表中无用户"))
        return False
    for user in user_ls:
        user_id = user.id
        try:
            hold_fund_ls = UserFundHold.query.filter(UserFundHold.user_id == user_id).all()
            if not hold_fund_ls:
                current_app.logger.info("%s: %s" % (__name__, "用户ID为%s的用户无持有基金" % user_id))
                continue
            sum_last_profit = 0
            sum_hold_fund_amount = 0
            sum_hold_fund_profit = 0
            for hold_fund in hold_fund_ls:
                sum_last_profit += hold_fund.lastday_profit
                sum_hold_fund_amount += hold_fund.current_amount
                sum_hold_fund_profit += hold_fund.current_profit
            user.last_profit = sum_last_profit
            user.hold_fund_amount = sum_hold_fund_amount
            user.hold_fund_profit = sum_hold_fund_profit
            user.current_time = datetime.now()
            user.update_time = datetime.now()
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            current_app.logger.error("%s: %s" % (__name__, e))
    for hold_fund in hold_fund_ls:
        try:
            fund_id = hold_fund.fund_id
            fund = Fund.query.filter(Fund.id == fund_id).first()
            current_price, price_time = fund.current_price, fund.price_time
            hold_fund.current_price = current_price
            hold_fund.price_time = price_time
            hold_fund.lastday_profit = current_price * hold_fund.hold_num - hold_fund.current_amount
            hold_fund.current_amount = current_price * hold_fund.hold_num
            hold_fund.current_profit = hold_fund.current_amount - hold_fund.cost
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("%s: %s" % (__name__, e))



if __name__ == "__main__":
    pass
