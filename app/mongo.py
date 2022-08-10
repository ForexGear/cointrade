from urllib.parse import quote
from pymongo import MongoClient
 
 
mongo_uri = "mongodb://polystone:" + quote("Tkwlsqks00") + "@localhost:27017/"
client = MongoClient(mongo_uri)

db = client.order_db
col = db.orderlist
# symbol = 'BTCUSDT_UMCBL'
# account = 'polystone'
# query = {'$and':[{"symbol": symbol}, {"account": account}]}
# result = col.find_one(query)
# print(result['leverage'])
result = {"code":"00000","msg":"success","requestTime":1660047363191,"data":[{"tradeId":"940872323009536111","symbol":"BTCUSDT_UMCBL","orderId":"940872322632024064","price":"23252.00","sizeQty":"0.001","fee":"0","side":"open_long","fillAmount":"23.252","profit":"0","cTime":"1660047363044"}]}
print(result['data'][0]['orderId'])
# col.insert_one({"orderId": result['data']['orderId']
#                                 , "symbol": result['data']['symbol']
#                                 , "posSide": posSide
#                                 , "fillAmount": result['data']['fillAmount']
#                                 , "openprice": result['data']['price']
#                                 , "size": result['data']['sizeQty']
#                                 , "cur_status": "open"
#                                 , "closeprice": "0"
#                                 , "profit": result['data']['profit']
#                                 , "opentime": result['data']['cTime']
#                                 })   
 # database = client.order_db
# collection = database.orderlist
# print(client.list_database_names())
# #collection.update_one({'cur_status':'close'},{'$set':{'cur_status':'open'}})
# query = {'$and':[{"symbol": 'BTCUSDT_UMCBL'}, {"cur_status": "open"}]}
# orderresult = collection.find(query)
# #orderresult = collection.find()
# print(list(orderresult))
# for item in orderresult:
#   if item['posSide'] == 'long':
#     print('long 주문 청산')
#     print(item)
#     collection.update_one({'$and':[{'cur_status':'open'},{'posSide':'long'}]},{'$set':{'cur_status':'close'}})
#     break;  
#   elif item['posSide'] == 'short':
#     print('short 주문 청산')
#     collection.update_one({'$and':[{'cur_status':'open'},{'posSide':'short'}]},{'$set':{'cur_status':'close'}})
#     break;  
#   else:
#     print('empty')


