#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :newsapi.py
# @Time      :4/8/22 5:51 PM
# @Author    :Zhidong R

import time
import requests
import re
from iFunds.utils.transform import str_to_dlt

def get_url_response_text(url):
    """
    封裝爬蟲函數，多次訪問，穩定爬到數據
    :param url:
    :return: str,或者失敗False
    """
    # 循环保持访问的稳定性
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    for loop in range(20):
        try:
            response = requests.get(url=url, headers=headers)
        except Exception as e:
            time.sleep(0.05)
        else:
            time.sleep(0.05)
            break
    if str(response.status_code) != "200":
        return False
    context = response.text
    return context

# url =https://3g.163.com/touch/reconstruct/article/list/BA8EE5GMwangning/0-10.html     url不全
# url =https://money.163.com/special/00259BVP/news_flow_index.js?callback=data_callback   url全，但为简介
def get_wangyi_news():
    url = r"https://3g.163.com/touch/reconstruct/article/list/BA8EE5GMwangning/0-10.html"
    content = get_url_response_text(url)
    if not content:
        return False

    pattern = r'(?<="BA8EE5GMwangning":)(.*?)(?=}\))'  # fS_code = "379010"
    search_ls = re.findall(pattern, content)
    print(search_ls[0])
    ls_temp =str_to_dlt(search_ls[0])
    print(ls_temp)

def get_wangyi_news1():
    url = r"https://money.163.com/special/00259BVP/news_flow_index.js?callback=data_callback"
    content = get_url_response_text(url)
    if not content:
        return False
    content = content.replace("data_callback", "")
    ls = str_to_dlt(content)
    for i in ls:
        for k,v in i.items():
            if "url" in k and "||" in v:
                # bigimg||http://dingyue.ws.126.net/2022/0409/55b05a4aj00ra1sdh002xd000v900fmp.jpg||||||||
                temp_ls = v.split("||")
                for temp in temp_ls:
                    if "http" in temp:
                        i[k] = temp
                        break
    # for i in ls:
    #     print(i)
    # for k, v in ls[0].items():
    #     print(k, v)
    return ls



if __name__ == "__main__":
    run_code = 0
    ls = get_wangyi_news1()
    for k,v in ls[0].items():
        print(k, v)