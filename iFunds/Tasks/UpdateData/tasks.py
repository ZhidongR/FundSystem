#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :tasks.py.py
# @Time      :10/21/21 2:36 AM
# @Author    :Zhidong R
import time
from celery.schedules import crontab
from flask import current_app, jsonify, request, g, session
from celery import current_app as app
# from iFunds import db, celery_app
from manage import my_celery as celery_app
from iFunds.models import User, Fund, UserFundForce
from iFunds.utils import FundData


@celery_app.task
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
        dict_data = fund_data_cls.get_detail_data(fund_code=fs_code)  # 已修改为dict
        # 将数据写入数据库中， 存在弊端，不能实现有则更新，无则插入操作
        # pd.io.sql.to_sql(frame=df, name='fund', con=your_connect, schema='fund_system', if_exists='append', index=False) #chunksize=10000

        # 更改方案成：有则更新，无则插入操作
        print(fs_code)
        print("准备进入Text")
        print("已进入Text")
        with app.app_context:
            try:
                print("已进入Try")
                if not dict_data:
                    continue
                fund = Fund.query.filter_by(fund_code=dict_data.get("fund_code")).first()
                if fund:
                    Fund.query.filter(Fund.fund_code == dict_data.get("fund_code")).update(dict_data)
                    db.session.commit()
                    current_app.logger.info("%s:update fund data bt updating %s" % (__name__, fs_code))
                    current_app.logger.debug("数据库中%s基金更新" % fs_code)
                    print("数据库中%s基金更新" % fs_code)
                else:
                    fund = Fund()
                    fund.set_para_from_dict(dict_data)
                    db.session.add(fund)
                    db.session.commit()
                    print("commit")
                    current_app.logger.info("%s:update fund data bt adding %s" % (__name__, fs_code))
                    current_app.logger.debug("数据库中%s基金新增" % fs_code)
                    print("数据库中%s基金新增" % fs_code)
                del fund
                print("Try结尾")
            except Exception as e:
                print("异常%s" %e)
                current_app.logger.error("%s: %s" % (__name__, e))
                # return False
    print("结尾")
    return True


@celery_app.task
def update_all_fund_data():
    """
    更新fund数据库中的基金信息，存在该基金则则更新，不存在则创建
    :param fund_data_ls:
    :return:  True of False
    """
    from iFunds.utils.fund_data import FundData
    fund_data = FundData()
    fund_data_ls = list(fund_data.get_all_funds().keys())
    fund_data.update_database(fund_data_ls)
    return True
    print("上下文有问题")
    return False
    print(" i am update_all_fund_data")
    time.sleep(1)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls add(1, 2) every 10 seconds.
    sender.add_periodic_task(10.0, add.s(1, 2), name='add every 10')

    # Calls add(3, 4) every 30 seconds
    sender.add_periodic_task(30.0, add.s(3, 4), )

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        add.s(1, 2),
    )


@celery_app.task
def add(x, y):
    print(x+y)
    return x + y