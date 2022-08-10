# coding: utf-8
from email import message
import re
from telethon import TelegramClient,events
import asyncio
import nest_asyncio
import datetime 

import bitget.mix.market_api as market
import bitget.mix.account_api as accounts
import bitget.mix.position_api as position
import bitget.mix.order_api as order
import bitget.mix.plan_api as plan
import bitget.mix.trace_api as trace
import json

from urllib.parse import quote
from pymongo import MongoClient

api_key = 'bg_bf30f9c630e788a57d61c72718fc5114'
secret_key = 'b90cb3744ff36225341676bc3df4e3edd02dc500e9106bf5bd90b83b84223d99'
passphrase = 'Tkwlsqks11'


    # result = positionApi.single_position(symbol, marginCoin='USDT', holdSide='long')
    # print(result)

# result = positionApi.all_position(productType='umcbl', marginCoin='USDT')
# print(result['data'][0]['holdSide']," ",result['data'][0]['averageOpenPrice'])
# print(result['data'][1]['holdSide']," ",result['data'][1]['averageOpenPrice'])

orderApi = order.OrderApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
positionApi = position.PositionApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
result = positionApi.all_position(productType='umcbl', marginCoin='USDT')
print(result)
result = orderApi.fills('BTCUSDT_UMCBL', orderId='940884076363677696')
print(len(result['data']))

# result = pythopositionApi.all_position(productType='umcbl', marginCoin='USDT')
# print(result['data'][0]['holdSide']," ",result['data'][0]['averageOpenPrice'])
# print(result['data'][1]['holdSide']," ",result['data'][1]['averageOpenPrice'])