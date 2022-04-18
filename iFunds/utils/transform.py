#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :transform.py
# @Time      :11/4/21 9:23 PM
# @Author    :Zhidong R

from ast import literal_eval

def str_to_dlt(string):
    """
    将具备“[a,b,c,d]”格式的字符串转化为list
    :param string:
    :return: list或tuple或dict或者None(出异常)
    """
    try:
        if string and isinstance(string, str):
            data = literal_eval(string.replace("null", "None"))
            return data
        elif isinstance(string, dict) or isinstance(string, list):
            return string
        else:
            return None
    except Exception as e:
        return None