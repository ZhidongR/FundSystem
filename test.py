#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test.py
# @Time      :10/16/21 6:37 PM
# @Author    :Zhidong R

import unittest
from iFunds import create_app, db
from iFunds.models import User,Fund,UserFundTrace,UserFundForce
from flask_migrate import Migrate
from iFunds.utils.fund_data import FundData
# 自定义测试类，setUp方法和tearDown方法会分别在测试前后执行。以test_开头的函数就是具体的测试代码。

class DatabaseTestCase(unittest.TestCase):
    app = None

    def setUp(self):
        app = create_app("develop")
        Migrate(app, db)
        self.app = app


    def tearDown(self):
        with self.app.app_context():
            db.session.remove()

    # 测试代码
    def test_append_data(self, user_name="基金大佬"):
        with self.app.app_context():
            fund_data = FundData()
            fund_data.update_database(fund_code_ls=["379010", "379020", "260108", "161725"])

if __name__ == "__main__" :
    run_code = 0