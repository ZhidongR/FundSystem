#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :trace_record.py
# @Time      :10/16/21 10:58 AM
# @Author    :Zhidong R


from datetime import datetime
from iFunds import db
from .base import BaseModel


class TraceRecord(BaseModel, db.Model):
    # 定义表名字
    __tablename__ = "user_fund_trace"
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    fund_id = db.Column(db.Integer, db.ForeignKey('fund.id'), index=True)
    fund_code = db.Column(db.String(64))
    fund_name = db.Column(db.String(64))
    buy_or_sale = db.Column(db.String(64))
    buy_money = db.Column(db.Float)
    sale_number = db.Column(db.Float)
    application_time = db.Column(db.DateTime)
    status = db.Column(db.Integer, default=0) # 0-待处理，1-已处理

    trace_price = db.Column(db.Float)  #交易单价
    price_time = db.Column(db.DateTime) # 交易单价对应的时间点
    trace_num = db.Column(db.Float) #交易数量
    trace_total = db.Column(db.Float)  # 交易数量
    trace_time = db.Column(db.DateTime)
    #
    # buy_price = db.Column(db.Integer)
    # count = db.Column(db.Integer)
    # buy_time = db.Column(db.DateTime, default=datetime.now())
    # status = db.Column(db.String(64), index=True)
    # amount = db.Column(db.Float)
    # current_price = db.Column(db.Float)
    # all_profit = db.Column(db.Float)
    # last_day_profit = db.Column(db.Float)
    # sale_price = db.Column(db.Float)
    # sale_time = db.Column(db.DateTime)
    # agrent_time = db.Column(db.DateTime)
    # # update_time = db.Column(db.Time, default=datetime.now())

    def to_dict(self):
        """
        将用户和
        :return:
        """
        dict_temp = dict()
        dict_temp["id"] = self.id
        dict_temp["fund_code"] = self.fund_code
        dict_temp["fund_name"] = self.fund_name
        dict_temp["buy_or_sale"] = self.buy_or_sale
        dict_temp["buy_money"] = self.buy_money
        dict_temp["sale_number"] = self.sale_number
        dict_temp["application_time"] = self.application_time
        dict_temp["status"] = self.status
        dict_temp["trace_price"] = self.trace_price
        dict_temp["price_time"] = self.price_time
        dict_temp["trace_num"] = self.trace_num
        dict_temp["trace_total"] = self.trace_total
        dict_temp["trace_time"] = self.trace_time
        return dict_temp
