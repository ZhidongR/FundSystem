#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :news.py.py
# @Time      :4/8/22 9:30 PM
# @Author    :Zhidong R

import json, time
from . import api
from flask import current_app, jsonify, request, g, session
from iFunds.utils.commons import REDIS_VERIFY_CODE_EX_TIME
from iFunds import db, redis_store
from iFunds.models import User, Fund, UserFundForce
from iFunds.utils.respond_code import RET, error_map
from iFunds.utils.commons import login_required
from iFunds.utils.newsapi import get_wangyi_news1
from iFunds.utils.transform import str_to_dlt


@api.route("/news", methods=["GET"])
def get_news():
    """
    返回财经的新闻
    :return:
    """
    # 1.redis中是否存在新闻键值对，news_XXX
    # --存在且未超过限制时间，直接获取，
    # --不存在或超过限定时间，更新后获取
    # redis_store.set('key', "value", REDIS_VERIFY_CODE_EX_TIME)
    keys_ls = redis_store.keys(pattern=r'news_*')
    if len(keys_ls) >= 2:
        delete_news_from_redis()
        str_key = write_news_to_redis()
        value = str_to_dlt(redis_store.get(str_key))
        return jsonify(code=RET.OK, msg="OK", data=value)
    if keys_ls:
        # news_20210410155960
        str_key = keys_ls[0]
        time_array = time.strptime(str_key[len(str_key) - 14:len(str_key)], "%Y%m%d%H%M%S")
        key_time = int(time.mktime(time_array))
        now = time.time()
        if now-key_time < 0.5*60*60: #半小时
            value = str_to_dlt(redis_store.get(str_key))
            return jsonify(code=RET.OK, msg="OK", data=value)
        else:
            delete_news_from_redis()
            str_key = write_news_to_redis()
            value = str_to_dlt(redis_store.get(str_key))
            return jsonify(code=RET.OK, msg="OK", data=value)

    else:
        delete_news_from_redis()
        str_key = write_news_to_redis()
        value = str_to_dlt(redis_store.get(str_key))
        return jsonify(code=RET.OK, msg="OK", data=value)


def write_news_to_redis():
    t = time.localtime()
    str_now = time.strftime('%04Y%02m%02d%02H%02M%02S', time.localtime())
    news_key = str.format("news_{}", str_now)
    try:
        news_str = json.dumps(get_wangyi_news1(),ensure_ascii=False)
        redis_store.set(news_key, news_str, REDIS_VERIFY_CODE_EX_TIME)
        return news_key
    except Exception as e:
        return False


def delete_news_from_redis():
    keys_ls = redis_store.keys(pattern=r'news_*')
    for key in keys_ls:
        redis_store.delete(key)


if __name__ == "__main__":
    run_code = 0
