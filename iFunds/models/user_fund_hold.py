#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :user_fund_hold.py
# @Time      :4/12/22 5:27 PM
# @Author    :Zhidong R
from datetime import datetime
from iFunds import db
from .base import BaseModel


class UserFundHold(BaseModel, db.Model):
    # 定义表名字
    __tablename__ = "user_fund_hold"
    # 定义字段
    """id(PK)
    user_id(FK)
    fund_id(FK)
    fund_code:
    fund_name:基金名称
    hold_num:持有数量
    buy_price:买入单价
    buy_amount:买入总额
    buy_time: 买入确认时间
    current_price:当前单价
    current_amount:当前总额
    current_profit:当前收益
    lastday_profit上一交易日收益
    update_time：更新时间 ,父类自带
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    fund_id = db.Column(db.Integer, db.ForeignKey('fund.id'), index=True)
    fund_code = db.Column(db.String(64))
    fund_name = db.Column(db.String(64))
    hold_num = db.Column(db.Float)
    cost = db.Column(db.Float)  # 成本

    # --动态数据：随市场更新--#
    last_price = db.Column(db.Float)
    last_time = db.Column(db.DateTime)
    current_price = db.Column(db.Float)
    price_time = db.Column(db.DateTime)
    current_amount = db.Column(db.Float)
    current_profit = db.Column(db.Float)
    lastday_profit = db.Column(db.Float)
    # --动态数据结束--#
    # 这几个用户不关注，可以将user_id和fund_id相同的合并同一条记录中
    buy_price = db.Column(db.Float)
    buy_price_time = db.Column(db.DateTime)  # 买入单价对应的时间点
    buy_amount = db.Column(db.Float)
    buy_time = db.Column(db.DateTime, default=datetime.now())
    # 更新处理标志位， 0不需要处理，1需要处理, 在出售申请和买入确认的时候需要置1；在出售确认或者自动更新后，置0
    deal_flag = db.Column(db.Integer, default=0)

    def to_dict(self):
        re_dict = {}

        if self.fund_code:
            re_dict["fund_code"] = self.fund_code
        if self.fund_name:
            re_dict["fund_name"] = self.fund_name
        if self.hold_num is not None:
            re_dict["hold_num"] = self.hold_num
        if self.cost is not None:
            re_dict["cost"] = self.cost
        if self.current_price is not None:
            re_dict["current_price"] = self.current_price
        if self.price_time:
            re_dict["price_time"] = self.price_time
        if self.current_amount is not None:
            re_dict["current_amount"] = self.current_amount
        if self.current_profit is not None:
            re_dict["current_profit"] = self.current_profit
        if self.lastday_profit is not None:
            re_dict["lastday_profit"] = self.lastday_profit

        if self.buy_price:
            re_dict["buy_price"] = self.buy_price
        if self.buy_price_time:
            re_dict["buy_price_time"] = self.buy_price_time
        if self.buy_amount:
            re_dict["buy_amount"] = self.buy_amount
        if self.buy_time:
            re_dict["buy_time"] = self.buy_time

        if self.deal_flag:
            re_dict["deal_flag"] = self.deal_flag
        return re_dict
