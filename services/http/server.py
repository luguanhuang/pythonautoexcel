# -*- coding: utf-8 -*-

from fastapi import FastAPI,Request,Response
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from config import setting 

from utils.log import httplogger
import json
import sys
sys.path.append('..')

from dao import datascreen

app = FastAPI()

# 这里配置支持跨域访问的前端地址
origins = [
    "*",     # 带端口的
]

# 将配置挂在到app上
app.add_middleware(
    CORSMiddleware,
    # 这里配置允许跨域访问的前端地址
    allow_origins="*",
    # 跨域请求是否支持 cookie， 如果这里配置true，则allow_origins不能配置*
    allow_credentials=True,
    # 支持跨域的请求类型，可以单独配置get、post等，也可以直接使用通配符*表示支持所有
    allow_methods=["*"],
    allow_headers=["*"],
)

# # app.include_router(ctwing_api,prefix="",tags=['签名', '认证'])

# @app.middleware('http')
# async def sign(request:Request,call_next):
#     try:
#         pass
#         # 校验签名
#         # 
#     except BaseException as e:
#         logger.error(e)
#         response= Response(json.dumps({
#                     "errorcode":"9001",
#                     "message":"pwfailure"
#                 }),200,)
#         logger.info(f'【{request.method}】【{request.client.host}:{request.client.port}】【{response.status_code}】【{request.url}】')
#     return response

# @app.post("/test")  
# def nbdataMessage(data:dict): 
#     httplogger.info(f"test data={data}")
#     result = apis.aep_device_command.CreateCommand('HY0lo5y1pdf','qAtI0mOLLw', '08d4f9289d9a407993f255c0a67028d8', '{\"content\":{\"params\":{\"data_download\":\"345678\"},\"serviceIdentifier\":\"8001\"},\"deviceId\":\"e5459e56135f48bcabfe458a93931731\",\"operator\":\"lu\",\"productId\":17045165}')
#     print('result='+str(result))
    
#     return {
#             "errorcode":"0000",
#             "message":"success"
#         }

# @app.post("/Keywordpopularity")  
# def getKeywordpopularity(): 
#     httplogger.info(f"Keywordpopularity data=")
    
#     arrkeyinfo = datascreen.select_Keyword_popularity()
#     # categorynum, subcnt = datascreen.select_Category_info("112")
#     return {
#             "errorcode":"0000",
#             "message":"success",
#             'keydata':arrkeyinfo
#         }

# @app.post("/Servicepopularity")  
# def getServicepopularity(): 
#     httplogger.info(f"Servicepopularity data=")
    
#     arrresdata = datascreen.select_Service_popularity()
#     return {
#             "errorcode":"0000",
#             "message":"success",
#             'keydata':arrresdata
#         }

# @app.post("/Servproductdata")  
# def getServproductdata(): 
#     httplogger.info(f"Servproductdata data=")
#     arrdata = datascreen.select_Category_info()
#     return {
#             "errorcode":"0000",
#             "message":"success",
#             "data": arrdata
#         }

# @app.post("/ServiceRanking")  
# def getServiceRanking(): 
#     httplogger.info(f"ServiceRanking data=")
#     arrServRanking = datascreen.select_Service_Ranking()
#     return {
#             "errorcode":"0000",
#             "message":"success",
#             'ServRanking':arrServRanking
#         }

# @app.post("/getnews")  
# def getnews(data:dict): 
#     httplogger.info(f"ServiceRanking data={data}")
#     newinfo = datascreen.select_news(data['times'])
#     return {
#             "errorcode":"0000",
#             "message":"success",
#             'newinfo':newinfo
#         }
#     return newinfo

# @app.post("/DialogueData")  
# def getDialogueData(): 
#     httplogger.info(f"getDialogueData data=")
#     resdata = datascreen.select_Comm_Info()
#     return {
#             "errorcode":"0000",
#             "message":"success",
#             'resdata':resdata
#         }

# @app.post("/UserLogin")  
# def getUserLogin(data:dict): 
#     httplogger.info(f"getUserLogin data={data}")
#     ret = datascreen.select_Login_Info(data['username'], data['passwd'])
#     if ret > 0:
#         return {
#             "errorcode":"0000",
#             "message":"success"
#         }
#     else:
#         return {
#             "errorcode":"0001",
#             "message":"username or passwd error"
#         }

# @app.post("/DataOverview")  
# def getDataOverview(): 
#     httplogger.info(f"getDataOverview data=")
#     totalcnt, totalincrementpercent, yesterdaytotalcnt,\
#     yesterdayincrement, totalincrement, incrementpercent,\
#     yesterdayrate, ratediff, twodaysagorate   = datascreen.select_Data_verview()
#     # return newinfo
#     return {
#             "errorcode":"0000",
#             "message":"success",
#             'totalcnt':totalcnt,
#             'totalincrementpercent':totalincrementpercent,
#             'yesterdaytotalcnt':yesterdaytotalcnt,

#             'yesterdayincrement':yesterdayincrement,
#             'totalincrement':totalincrement,
#             'incrementpercent':incrementpercent,

#             'yesterdayrate':yesterdayrate,
#             'ratediff':ratediff,
#             'twodaysagorate':twodaysagorate,
#         }
    
# @app.post("/KeywordProdRelat")  
# def getKeywordProdRelat(): 
#     httplogger.info(f"getKeywordProdRelat: func begin")
#     allresdata = datascreen.select_Keyword_Prod_Relat()
#     return {
#             "errorcode":"0000",
#             "message":"success",
#             'data':allresdata
#         }

# @app.post("/ScriptsCategoryRelat")  
# def getScriptsCategoryRelat(): 
#     httplogger.info(f"ScriptsCategoryRelat: func begin")
#     allresdata = datascreen.select_Scripts_Category_Relat()
#     return {
#             "errorcode":"0000",
#             "message":"success",
#             'data':allresdata
#         }

# def htttp_start():
#     print("listen httpport=", setting.httpport)
#     # uvicorn.run(app = 'services.http.server:app', reload=True,host="0.0.0.0",port=setting.httpport)
#     uvicorn.run(app = 'services.http.server:app', reload=False,host="0.0.0.0",port=setting.httpport)


