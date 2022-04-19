#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :self.py.py
# @Time      :10/16/21 12:45 AM
# @Author    :Zhidong R

import json
from datetime import datetime
from iFunds import db
from .base import BaseModel
from sqlalchemy.databases import mysql
from iFunds.utils.commons import str2list


class Fund(BaseModel, db.Model):
    # 定义表名字
    __tablename__ = "fund"
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fund_code = db.Column(db.String(64), unique=True, index=True)
    fund_name = db.Column(db.String(64), unique=True, index=True)
    current_price = db.Column(db.Float)
    price_time = db.Column(db.DateTime)
    source_rate = db.Column(db.Float)
    rate = db.Column(db.Float)
    min_pn = db.Column(db.Float)  # 最小购买数字
    stock_codes = db.Column(mysql.MSMediumText)# 持有股票代码
    syl_1y = db.Column(db.Float)
    syl_6m = db.Column(db.Float)
    syl_3m = db.Column(db.Float)
    syl_1m = db.Column(db.Float)
    # mysql 数据库长文本存储改用TEXT，可存65535个Byte
    shares_positions = db.Column(mysql.MSMediumText) # 仓位测算图
    net_worth_trend = db.Column(mysql.MSMediumText) # 单位净值走势
    ac_worth_trend = db.Column(mysql.MSMediumText) # 累计净值走势
    grand_total = db.Column(mysql.MSMediumText) # 累计收益走势
    rate_in_similar_type = db.Column(mysql.MSMediumText) # 同类型基金排名
    rate_in_similar_present = db.Column(mysql.MSMediumText) # 同类型基金排名百分比
    fluctuation_scale = db.Column(mysql.MSMediumText) # 规模变动
    holder_structure = db.Column(mysql.MSMediumText) # 持有人结构
    asset_allocation = db.Column(mysql.MSMediumText)  # 资产分配
    performance_evaluation = db.Column(mysql.MSMediumText)  # 业绩评价
    current_fund_manager = db.Column(mysql.MSMediumText)  # 基金经理
    buy_sedemption = db.Column(mysql.MSMediumText)  # 申赎购汇
    swithSameType = db.Column(mysql.MSMediumText)  # 同类型基金涨幅榜

    def to_dict(self):
        """
        将数据转化为字典输出,并将value部分为dict或list格式的字符串转化为dict或list
        :return: dict
        """
        dict_temp = {
            "fund_code": self.fund_code,
            "fund_name": self.fund_name,
            "current_price": self.current_price,
            "price_time": self.price_time,
            "source_rate": self.source_rate,
            "rate": self.rate,
            "min_pn": self.min_pn,
            "stock_codes": str2list(self.stock_codes),
            "syl_1y": self.syl_1y,
            "syl_6m": self.syl_6m,
            "syl_3m": self.syl_3m,
            "syl_1m": self.syl_1m,
            "shares_positions": str2list(self.shares_positions),
            "net_worth_trend": str2list(self.net_worth_trend),
            "ac_worth_trend": str2list(self.ac_worth_trend),
            "grand_total": str2list(self.grand_total),
            "rate_in_similar_type": str2list(self.rate_in_similar_type),
            "rate_in_similar_present": str2list(self.rate_in_similar_present),
            "fluctuation_scale": str2list(self.fluctuation_scale),
            "asset_allocation": str2list(self.asset_allocation),
            "holder_structure": str2list(self.holder_structure),
            "performance_evaluation": str2list(self.performance_evaluation),
            "current_fund_manager": str2list(self.current_fund_manager),
            "buy_sedemption": str2list(self.buy_sedemption),
            "swithSameType": str2list(self.swithSameType)
        }
        return dict_temp

    def set_para_from_dict(self, dict_data):
        """
        将dict_data的数据赋值到属性当中
        :param dict_data: 
        :return:
        """
        name_fro_float_ls = ["source_rate","rate","min_pn","syl_1y","syl_1y","syl_6m",
                             "syl_3m", "syl_1m"]

        self.fund_code = dict_data.get("fund_code")
        self.fund_name = dict_data.get("fund_name")
        if dict_data.get("current_price") and dict_data.get("current_price") != "":
            self.current_price = float(dict_data.get("current_price"))
        if dict_data.get("price_time") and dict_data.get("price_time") != "":
            self.price_time = dict_data.get("price_time")
        if dict_data.get("source_rate") and dict_data.get("source_rate") != "":
            self.source_rate = float(dict_data.get("source_rate"))
        if dict_data.get("rate") and dict_data.get("rate") != "":
            self.rate = float(dict_data.get("rate"))
        if dict_data.get("min_pn") and dict_data.get("min_pn") != "":
            self.min_pn = float(dict_data.get("min_pn"))
        self.stock_codes = dict_data.get("stock_codes")
        if dict_data.get("syl_1y") and dict_data.get("syl_1y") != "":
            self.syl_1y = float(dict_data.get("syl_1y"))
        if dict_data.get("syl_6m") and dict_data.get("syl_6m") != "":
            self.syl_6m = float(dict_data.get("syl_6m"))
        if dict_data.get("syl_3m") and dict_data.get("syl_3m") != "":
            self.syl_3m = float(dict_data.get("syl_3m"))
        if dict_data.get("syl_1m") and dict_data.get("syl_1m") != "":
            self.syl_1m = float(dict_data.get("syl_1m"))
        self.shares_positions = dict_data.get("shares_positions")
        self.net_worth_trend = dict_data.get("net_worth_trend")
        self.ac_worth_trend = dict_data.get("ac_worth_trend")
        self.grand_total = dict_data.get("grand_total")
        self.rate_in_similar_type = dict_data.get("rate_in_similar_type")
        self.rate_in_similar_present = dict_data.get("rate_in_similar_present")
        self.fluctuation_scale = dict_data.get("fluctuation_scale")
        self.asset_allocation = dict_data.get("asset_allocation")
        self.holder_structure = dict_data.get("holder_structure")
        self.performance_evaluation = dict_data.get("performance_evaluation")
        self.buy_sedemption = dict_data.get("buy_sedemption")
        self.swithSameType = dict_data.get("swithSameType")
        return True
