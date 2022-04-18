#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :commons.py
# @Time      :10/17/21 10:11 AM
# @Author    :Zhidong R

from flask import session, jsonify, g, current_app
from werkzeug.routing import BaseConverter
from functools import wraps
from ast import literal_eval
from iFunds.utils.respond_code import RET

REDIS_VERIFY_CODE_EX_TIME = 300

class RegexConverter(BaseConverter):
    """自定义静态文件路由转换器"""
    def __init__(self, map, *args):
        super(RegexConverter, self).__init__(map)
        self.regex = args[0]


def login_required(view_func):
    """登录校验装饰器
    :param func:函数名
    :return: 闭包函数名
    """
    # 装饰器装饰一个函数时，会修改该函数的__name__属性
    # 如果希望装饰器装饰之后的函数，依然保留原始的名字和说明文档,就需要使用wraps装饰器，装饰内存函数
    @wraps(view_func)
    def wrapper(*args,**kwargs):
        #从session中或取user_id
        user_id = session.get('user_id')
        if not user_id:
            #用户未登录
            return jsonify(re_code=RET.SESSIONERR, msg='用户未登录')
        else:
            #用户已登录使用g变量保存住user_id，方便被装饰的函数中调用g变量获取user_id。
            g.user_id = user_id # g变量是flask的全局变量
            return view_func(*args, **kwargs)
    return wrapper

def str2list(string):
    """
    将具备“[a,b,c,d]”格式的字符串转化为list
    :param string:
    :return: list或tuple或dict或者None(出异常)
    """
    try:
        if string:
            list_data = literal_eval(string)
            return list_data
        else:
            return None
    except Exception as e:
        current_app.logger.error(e)
        current_app.logger.error("%s:出现转化list异常:str为：%s" % (__name__, string))
        return None