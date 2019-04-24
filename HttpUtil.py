#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-23
# @Author  : YY

import requests
import json
import urllib
import urllib.parse
import urllib.request

#代理服务器
PROXY_DICT = {}

#HTTP GET
def http_get_request(url, params, add_to_headers=None):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = urllib.parse.urlencode(params)
    try:
        response = requests.get(url, postdata, headers=headers, timeout=30, proxies=PROXY_DICT)
        if response.status_code == 200:
            return response.text
        else:
            return
    except BaseException as e:
        print("httpGet failed, %s" % str(e))
        return

#HTTP POST
def http_post_request(url, params, add_to_headers=None):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }
    if add_to_headers:
        headers.update(add_to_headers)

    try:
        response = requests.post(url, params, headers=headers, timeout=30, proxies=PROXY_DICT)
        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        print("httpPost failed, " % str(e))
        return

#HTTP POST
def http_post_request_json(url, params, add_to_headers=None):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = json.dumps(params)

    try:
        response = requests.post(url, postdata, headers=headers, timeout=30, proxies=PROXY_DICT)
        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        print("httpPost failed, " % str(e))
        return