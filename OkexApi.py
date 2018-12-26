#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-22
# @Author  : QiaoYing

import base64
import hashlib
import hmac
import uuid
import datetime

from HttpUtil import *

API_HOST = 'https://www.okex.com'
PASS_PHRASE = 'xxxxxxxxx'
API_KEY = 'xxxxxxxxx'
SECRET_KEY = 'xxxxxxxxx'

# granularity必须是[60 180 300 900 1800 3600 7200 14400 21600 43200 86400 604800]中的任一值
# 这些值分别对应的是[1min 3min 5min 15min 30min 1hour 2hour 4hour 6hour 12hour 1day 1week]的时间段
CURRENCY = 'btc'
INSTRUMENT_ID = 'btc-usd'
GRANULARITY = 14400
METHOD_GET = "GET"
METHOD_POST = "POST"
SIDE_BUY = 'buy'
SIDE_SELL = 'sell'
MARGIN_TRADING = '1'

HEADERS = {
    "Content-type": "application/json",
    "OK-ACCESS-KEY": API_KEY,
    "OK-ACCESS-SIGN": '',
    "OK-ACCESS-TIMESTAMP": '',
    "OK-ACCESS-PASSPHRASE": PASS_PHRASE
}


def set_sign(method, request_path, headers, body=''):
    timestamp = get_time()
    data = (timestamp + method + request_path + body).encode(encoding='UTF8')
    secret_key = SECRET_KEY.encode(encoding='UTF8')
    digest = hmac.new(secret_key, data, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    headers['OK-ACCESS-TIMESTAMP'] = timestamp
    headers['OK-ACCESS-SIGN'] = signature


# 获取okcoin系统时间戳
def get_time():
    res = http_get_request(API_HOST + '/api/general/v3/time', '')
    if res and 'iso' in res:
        return res['iso']
    else:
        date_now = datetime.datetime.now()  # 获取现在时间
        date_str = str(date_now)
        date_str = date_str.replace(' ','T')
        date_str = date_str[:-3]+'Z'
        return date_str


# 获取币对信息
def get_instruments():
    res = http_get_request(API_HOST + '/api/spot/v3/instruments', '')
    return res


# 获取账户信息
def get_account():
    request_path = '/api/spot/v3/accounts/' + CURRENCY
    headers = HEADERS.copy()
    set_sign(METHOD_GET, request_path, headers, '')
    return http_get_request(API_HOST + request_path, '', headers)


# 获取K线数据
def get_kline():
    request_path = '/api/spot/v3/instruments/' + INSTRUMENT_ID + '/candles?granularity=14400'
    headers = HEADERS.copy()
    set_sign(METHOD_GET, request_path, headers, '')
    return http_get_request(API_HOST + request_path, '', headers)


# 获取行情数据
def get_ticker():
    request_path = '/api/spot/v3/instruments/' + INSTRUMENT_ID + '/ticker'
    headers = HEADERS.copy()
    set_sign(METHOD_GET, request_path, headers, '')
    return http_get_request(API_HOST + request_path, '', headers)


# 获取行情数据
def get_tickers():
    request_path = '/api/spot/v3/instruments/ticker'
    headers = HEADERS.copy()
    set_sign(METHOD_GET, request_path, headers, '')
    return http_get_request(API_HOST + request_path, '', headers)


# 获取深度数据
def get_book(instrument_id=INSTRUMENT_ID):
    request_path = '/api/spot/v3/instruments/' + instrument_id + '/book'
    headers = HEADERS.copy()
    set_sign(METHOD_GET, request_path, headers, '')
    return http_get_request(API_HOST + request_path, '', headers)


# 创建订单
def create_order(side, price, size, instrument_id=INSTRUMENT_ID):
    request_path = '/api/spot/v3/orders'
    client_oid = str(uuid.uuid1())
    params = {"client_oid": client_oid,
              "type": 'limit',
              "side": side,
              "instrument_id": instrument_id,
              "margin_trading": MARGIN_TRADING,
              "size": size,
              "price": price}
    headers = HEADERS.copy()
    set_sign(METHOD_POST, request_path, headers, json.dumps(params))
    return http_post_request_json(API_HOST + request_path, params, headers)


# 获取所有未成交订单
def get_orders_pending(data_from='0', data_to='100', data_limit='100', instrument_id=INSTRUMENT_ID):
    request_path = '/api/spot/v3/orders_pending'
    params = "?from=" + data_from + "&to=" + data_to + "&limit=" + data_limit + "&instrument_id=" + instrument_id
    headers = HEADERS.copy()
    set_sign(METHOD_GET, request_path, headers, params)
    return http_get_request(API_HOST + request_path + params, '', headers)


# 批量取消订单
def cancel_batch_orders(order_ids, instrument_id=INSTRUMENT_ID):
    request_path = '/api/spot/v3/cancel_batch_orders'
    params = [{"order_id": order_ids,
               "instrument_id": instrument_id}]
    headers = HEADERS.copy()
    set_sign(METHOD_POST, request_path, headers, json.dumps(params))
    print(json.dumps(params))
    return http_post_request_json(API_HOST + request_path, params, headers)


if __name__ == '__main__':
    # print(create_order(SIDE_BUY, 3526.63, 0.01, INSTRUMENT_ID))
    # print(cancel_batch_orders(['7fd89f8ds9']))
    print(get_instruments())
