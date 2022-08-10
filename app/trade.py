# coding: utf-8
from email import message
import time
import datetime
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

mongo_uri = "mongodb://polystone:" + quote("Tkwlsqks00") + "@localhost:27017/"
dbclient = MongoClient(mongo_uri)
 
database = dbclient['order_db']
collection = database['orderlist']

api_key = 'bg_bf30f9c630e788a57d61c72718fc5114'
secret_key = 'b90cb3744ff36225341676bc3df4e3edd02dc500e9106bf5bd90b83b84223d99'
passphrase = 'Tkwlsqks11'

api_id = '16316634'
api_hash = '453f9fe430c885d2b0b0582bbf064ba3'
client = TelegramClient('bitget', api_id, api_hash)

orderApi = order.OrderApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
positionApi = position.PositionApi(api_key, secret_key, passphrase, use_server_time=False, first=False)

async def Run_Telethon():    
    await client.start()
    await client.run_until_disconnected()
 
@client.on(events.NewMessage)
async def handler(event):
    temp = str(event)
    msgs = event.text
    result = msgs.replace(" " , "")
    orderprice = ''
    ordertype = ''
    multiple = ''
    amountrate = ''
    now = datetime.datetime.now()
    try:
        channel_id = re.search('channel_id\=(.+?)\)', temp).group(1)
    except ValueError as m:
        print(m)
    else:
        print('Server Channel_ID:',channel_id)
    finally:
        #if '추세돌파' in result:
            #print(now,' Order:추세돌파 스킵')
            
        if '추세돌파' not in result:
            if '숏진입' in result:
                orderprice = re.search('\[(.+?)\]', result).group(1)
                ordertype = 'short'
                multiple = re.search('레버리지\:(.+?)설정', result).group(1)
                amountrate = re.search('시드머니(.+?)진입', result).group(1)
                print(now,' Order:', ordertype, 'Price:',orderprice, ' Multiple',multiple,' AmountRate:',amountrate)
                BitGetOrder(ordertype)
                #await event.reply('OrderMessage:'+ordertype+'Price:'+orderprice+' Multiple'+multiple+' AmountRate:'+amountrate)
            elif '롱진입' in result:
                orderprice = re.search('\[(.+?)\]', result).group(1)
                ordertype = 'long'
                multiple = re.search('레버리지\:(.+?)설정', result).group(1)
                amountrate = re.search('시드머니(.+?)진입', result).group(1)
                print(now,' Order:', ordertype, 'Price:',orderprice, ' Multiple',multiple,' AmountRate:',amountrate)
                BitGetOrder(ordertype)
                #await event.reply('OrderMessage:'+ordertype+'Price:'+orderprice+' Multiple'+multiple+' AmountRate:'+amountrate)
            elif '시장가청산' in result:
                ordertype = 'close'
                print(now,' Order:', ordertype)
                BitGetOrder(ordertype)
                #await event.reply('OrderMessage:'+ordertype)
            else:
                orderprice = '0'
                ordertype = 'Wait' 

def BitGetOrder(ordertype=None):   

    try:
        symbol = 'BTCUSDT_UMCBL'
        account = 'polystone'
        db = dbclient.trade_setup
        col = db.setup
        symbol = 'BTCUSDT_UMCBL'
        account = 'polystone'
        query = {'$and':[{"symbol": symbol}, {"account": account}]}
        result = col.find_one(query)
        leverage = result['leverage']
        maginmode = result['maginmode']
        accountbalance = result['balance']
        amount_rate = result['amount_rate']
        if result['amountcal'] == 'fixed':
            amount = result['amount'] 
        else:
            amount = 0.005 # todo: 계산식 넣을 것 
            #accountbalance * rate
        #ticker = exchange.fetch_ticker(symbol)
        if ordertype == "long":
            result = orderApi.place_order(symbol, marginCoin='USDT', size=amount,side='open_long', orderType='market', price=None, timeInForceValue='normal')
            orderId = result["data"]["orderId"]
            insert_db(symbol, orderId, 'long')

        elif ordertype == "short":
            result = orderApi.place_order(symbol, marginCoin='USDT', size=amount,side='open_short', orderType='market', price=None, timeInForceValue='normal')
            orderId = result["data"]["orderId"]
            insert_db(symbol, orderId, 'short')

        elif ordertype == "close":
            order_state = orderstate(symbol)
            if order_state['posSide'] == 'long':
                result = orderApi.place_order(symbol, marginCoin='USDT', size=order_state['size'], side='close_long', orderType='market', price=None, timeInForceValue='normal')
                orderId = result["data"]["orderId"]
                update_db(symbol, orderId, 'long')
            elif order_state['posSide'] == 'short':
                result = orderApi.place_order(symbol, marginCoin='USDT', size=order_state['size'], side='close_short', orderType='market', price=None, timeInForceValue='normal')
                orderId = result["data"]["orderId"]
                update_db(symbol, orderId, 'short')
            else:
                print('order empty')  
            #{'code': '00000', 'msg': 'success', 'requestTime': 1659852166077, 'data': {'clientOid': '940053607791362048', 'orderId': '940053607736836096'}}  


        else:
            print(f'당신은 {telecom} 사용자입니다.')

    except Exception as e:
        print(f'Exception: \n{e}')

def insert_db(symbol, orderId, posSide):
    while True:
        result = orderApi.fills(symbol, orderId)
        if len(result['data']) >= 1:
            break;
        time.sleep(0.05)    
    if result['msg'] == 'success':
        collection.insert_one({"orderId": result['data'][0]['orderId']
                                , "symbol": result['data'][0]['symbol']
                                , "posSide": posSide
                                , "fillAmount": result['data'][0]['fillAmount']
                                , "openprice": result['data'][0]['price']
                                , "size": result['data'][0]['sizeQty']
                                , "cur_status": "open"
                                , "closeprice": 0
                                , "profit": result['data'][0]['profit']
                                , "opentime": datetime.datetime.now()
                                , "closetime": ""
                                })   
        print('db ',posSide, ' inserted!')    
    else:
        print("insert error!")

def select_trade_setup(symbol, accoount):
    query = {'$and':[{"symbol": symbol}, {"account": accoount}]}
    collection.update_one({'posSide':'open'},{'$set':{'posSide':'close'}})

def update_db(symbol, orderId, posSide):
    while True:
        result = orderApi.fills(symbol, orderId)
        if len(result['data']) >= 1:
            break;
        time.sleep(0.05) 

    closeprice = result['data'][0]['price']
    profit = result['data'][0]['profit']
    closetime = datetime.datetime.now()
    collection.update_one({'$and':[{'posSide':posSide},{'cur_status':'open'}]}
    ,{'$set':{'cur_status':'close','closeprice':closeprice,'profit':profit,'closetime':closetime}})
    print('update ',posSide,' OK!')

def orderstate(symbol):
    order_state = {'size':'0.000', 'posSide':'empty'}
    query = {'$and':[{"symbol": symbol}, {"cur_status": "open"}]}
    orderresult = collection.find(query).limit(1)
    for item in orderresult:
        if item['posSide'] == 'long':
            order_state['posSide'] = 'long'
            order_state['size'] = item['size'] 
            break;  
        elif item['posSide'] == 'short':
            order_state['posSide'] = 'short'
            order_state['size'] = item['size']
            break;  
        else:
            order_state['posSide'] = 'empty' 
            order_state['size'] = '0.000' 
            break; 
    
    return order_state      
'''
def cal_amount(usdt_balance, cur_price):
    portion = 0.1 
    usdt_trade = usdt_balance * portion
    amount = math.floor((usdt_trade * 1000000)/cur_price) / 1000000
    return amount 
'''
nest_asyncio.apply()
asyncio.run(Run_Telethon())