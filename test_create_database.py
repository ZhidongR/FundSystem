#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :test_create_database.py
# @Time      :10/19/21 3:14 PM
# @Author    :Zhidong R

import unittest
from iFunds import create_app, db
from iFunds.models import User,Fund,UserFundHold,UserFundForce
from flask_migrate import Migrate
from iFunds.tasks import *

# 自定义测试类，setUp方法和tearDown方法会分别在测试前后执行。以test_开头的函数就是具体的测试代码。

class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app("develop")
        Migrate(app, db)
        self.app = app

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            # db.drop_all()

    # 测试代码
    def test_append_data(self, user_name="基金大佬"):
        with self.app.app_context():
            db.create_all()


if __name__ == "__main__":
    run_code = 0
