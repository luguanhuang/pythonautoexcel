# -*- coding: utf-8 -*-

from fastapi import FastAPI,Request,Response
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from config import setting 
from utils.log import sportlogger
import json
import sys
sys.path.append('..')
import requests

from dao import sportinfo
from bs4 import BeautifulSoup
import time
app = FastAPI()
from requests.exceptions import Timeout

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

headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding':'gzip, deflate, br, zstd',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control':'no-cache'
}

def getprematchbriefingdata():
    print("getprematchbriefingdata: func begin")
    data =  {
            "newsTypeId": "721",
            "newsId": "",
            "pageNumber": "1",
            "hotTagId": ""
        }
    
    # {newsTypeId: "601", pageSize: "24", pageNumber: "1", hotTagId: ""}
    proxyMeta = 'socks5://customer-c7590e:13c780cc@proxy.ipipgo.com:31212'
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta
    }
    
    try:
        # xml_data = res.content
        # print("Content-Type=", res.headers['Content-Type'])
        print("getprematchbriefingdata: func begin11")       
        print("data0=", data)
        res = requests.post("https://www.macauslot.com/infoApi/cn/D/FB/newsdlist", json=data,headers=headers, proxies=proxies, timeout=10)
        print("getprematchbriefingdata: status_code=", res.status_code)
        if res.status_code==200:
            data = res.json()['data']
            # print("data=",data['total'], " page=", data['pages'])
            # print("listinfo=",data['list'])
            # print("listlen=", len(data['list']))
            listinfo = data['list']
            sportinfo.insert_news_info(listinfo, res.json()['sysTime'])
            pagenum = 2
            totalcnt = 1
            while True:
                fChkTime = data['fChkTime']
                fNewsId = data['fNewsId']
                fRptTime = data['fRptTime']
                data =  {
                "newsTypeId": "721",
                "newsId": "",
                "pageNumber": str(pagenum),
                "hotTagId": "",
                "fChkTime":fChkTime,
                'fNewsId':fNewsId,
                "fRptTime":fRptTime
                }

                print("getprematchbriefingdata:data1=", data)
                if fChkTime == "-1" or fRptTime == "-1":
                    break;
                totalcnt = totalcnt + 1
                if totalcnt >= 1000:
                    break
                try:
                    res = requests.post("https://www.macauslot.com/infoApi/cn/D/FB/newsdlist", json=data,headers=headers, proxies=proxies, timeout=10)
                    if res.status_code==200:
                        
                        data = res.json()['data']
                        listinfo = data['list']
                        sportinfo.insert_news_info(listinfo, res.json()['sysTime'])
                except Timeout:
                    # 请求超时处理
                    print("getprematchbriefingdata: 请求超时，请重试！")
                    time.sleep(1)
                    # totalcnt = totalcnt + 1
                    continue
                except Exception as exc:
                    print("getprematchbriefingdata: There was a problem: %s" %(exc))
                    # totalcnt = totalcnt + 1
                    time.sleep(1)
                    continue
                time.sleep(0.3)
                # totalcnt = totalcnt + 1
                pagenum = pagenum+1
            # with open("news.txt","w",encoding="utf-8") as file:
            #     # 将每页网页的内容存进listpage文件夹中
            #     file.write(res.text)
    except Timeout:
        # 请求超时处理
        print("getprematchbriefingdata: 请求超时，请重试！")
    except Exception as exc:
        print("getprematchbriefingdata: There was a problem: %s" %(exc))

def getpostmatchbriefingdata():
    print("getpostmatchbriefingdata: func begin")
    data = {
        "newsTypeId": "761", 
        "pageNumber": "1", 
        "newsId": "", 
        "hotTagId": "", 
        "fRptTime": "", 
        "fNewsId": "", 
        "fChkTime": ""
        }
    
    # {newsTypeId: "601", pageSize: "24", pageNumber: "1", hotTagId: ""}
    proxyMeta = 'socks5://customer-c7590e:13c780cc@proxy.ipipgo.com:31212'
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta
    }
    
    try:
        # xml_data = res.content
        # print("Content-Type=", res.headers['Content-Type'])
            
        print("getpostmatchbriefingdata: data0=", data)
        
                            
        res = requests.post("https://www.macauslot.com/infoApi/cn/D/FB/newsdlist", json=data,headers=headers, proxies=proxies, timeout=10)
        print("getpostmatchbriefingdata: status_code=", res.status_code)
        if res.status_code==200:
            data = res.json()['data']
            # print("data=",data['total'], " page=", data['pages'])
            # print("listinfo=",data['list'])
            # print("listlen=", len(data['list']))
            listinfo = data['list']
            sportinfo.insert_news_info(listinfo, res.json()['sysTime'])
            pagenum = 2
            totalcnt = 1
            while True:
                fChkTime = data['fChkTime']
                fNewsId = data['fNewsId']
                fRptTime = data['fRptTime']

                data = {
                    "newsTypeId": "761", 
                    "pageNumber": str(pagenum), 
                    "newsId": "", 
                    "hotTagId": "", 
                    "fRptTime": fRptTime, 
                    "fNewsId": fNewsId, 
                    "fChkTime": fChkTime
                    }

                # data =  {
                # "newsTypeId": "721",
                # "newsId": "",
                # "pageNumber": str(pagenum),
                # "hotTagId": "",
                # "fChkTime":fChkTime,
                # 'fNewsId':fNewsId,
                # "fRptTime":fRptTime
                # }

                print("getpostmatchbriefingdata: data1=", data)
                if fChkTime == "-1" or fRptTime == "-1":
                    break;
                totalcnt = totalcnt + 1
                if totalcnt >= 1000:
                    break
                try:
                    res = requests.post("https://www.macauslot.com/infoApi/cn/D/FB/newsdlist", json=data,headers=headers, proxies=proxies, timeout=10)
                    if res.status_code==200:
                        data = res.json()['data']
                        listinfo = data['list']
                        sportinfo.insert_news_info(listinfo, res.json()['sysTime'])
                except Timeout:
                    # 请求超时处理
                    print("getpostmatchbriefingdata: 请求超时，请重试！")
                    time.sleep(1)
                    # totalcnt = totalcnt + 1
                    continue
                except Exception as exc:
                    print("getpostmatchbriefingdata: There was a problem: %s" %(exc))
                    # totalcnt = totalcnt + 1
                    time.sleep(1)
                    continue
                time.sleep(0.3)
                # totalcnt = totalcnt + 1
                pagenum = pagenum+1
            # with open("news.txt","w",encoding="utf-8") as file:
            #     # 将每页网页的内容存进listpage文件夹中
            #     file.write(res.text)
    except Timeout:
        # 请求超时处理
        print("getpostmatchbriefingdata: 请求超时，请重试！")
    except Exception as exc:
        print("getpostmatchbriefingdata: There was a problem: %s" %(exc))

def getnewshighlightsdata():
    print("getnewshighlightsdata: func begin")
    data = {
        "newsTypeId": "601", 
        "pageNumber": "1", 
        "newsId": "", 
        "hotTagId": "", 
        "fRptTime": "", 
        "fNewsId": "", 
        "fChkTime": ""
        }
    
    # {newsTypeId: "601", pageSize: "24", pageNumber: "1", hotTagId: ""}
    proxyMeta = 'socks5://customer-c7590e:13c780cc@proxy.ipipgo.com:31212'
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta
    }
    
    try:
        # xml_data = res.content
        # print("Content-Type=", res.headers['Content-Type'])
            
        print("getnewshighlightsdata: data0=", data)
        
                            
        res = requests.post("https://www.macauslot.com/infoApi/cn/D/FB/newsdlist", json=data,headers=headers, proxies=proxies, timeout=10)
        print("getnewshighlightsdata: status_code=", res.status_code)
        if res.status_code==200:
            data = res.json()['data']
            # print("data=",data['total'], " page=", data['pages'])
            # print("listinfo=",data['list'])
            # print("listlen=", len(data['list']))
            listinfo = data['list']
            sportinfo.insert_news_info(listinfo, res.json()['sysTime'])
            pagenum = 2
            totalcnt = 1
            while True:
                fChkTime = data['fChkTime']
                fNewsId = data['fNewsId']
                fRptTime = data['fRptTime']

                data = {
                    "newsTypeId": "761", 
                    "pageNumber": str(pagenum), 
                    "newsId": "", 
                    "hotTagId": "", 
                    "fRptTime": fRptTime, 
                    "fNewsId": fNewsId, 
                    "fChkTime": fChkTime
                    }

                # data =  {
                # "newsTypeId": "721",
                # "newsId": "",
                # "pageNumber": str(pagenum),
                # "hotTagId": "",
                # "fChkTime":fChkTime,
                # 'fNewsId':fNewsId,
                # "fRptTime":fRptTime
                # }

                print("getnewshighlightsdata: data1=", data)
                if fChkTime == "-1" or fRptTime == "-1":
                    break;
                totalcnt = totalcnt + 1
                if totalcnt >= 1000:
                    break
                try:
                    res = requests.post("https://www.macauslot.com/infoApi/cn/D/FB/newsdlist", json=data,headers=headers, proxies=proxies, timeout=10)
                    if res.status_code==200:
                        data = res.json()['data']
                        listinfo = data['list']
                        sportinfo.insert_news_info(listinfo, res.json()['sysTime'])
                except Timeout:
                    # 请求超时处理
                    print("getnewshighlightsdata: 请求超时，请重试！")
                    time.sleep(1)
                    # totalcnt = totalcnt + 1
                    continue
                except Exception as exc:
                    print("getnewshighlightsdata: There was a problem: %s" %(exc))
                    # totalcnt = totalcnt + 1
                    time.sleep(1)
                    continue
                time.sleep(0.3)
                # totalcnt = totalcnt + 1
                pagenum = pagenum+1
            # with open("news.txt","w",encoding="utf-8") as file:
            #     # 将每页网页的内容存进listpage文件夹中
            #     file.write(res.text)
    except Timeout:
        # 请求超时处理
        print("getnewshighlightsdata: 请求超时，请重试！")
    except Exception as exc:
        print("getnewshighlightsdata: There was a problem: %s" %(exc))

def getscoreinfo():
    data =  {
        }
        
    proxyMeta = 'socks5://customer-c7590e:13c780cc@proxy.ipipgo.com:31212'
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta
    }

    # print("proxies=", proxies)
    try:
        res = requests.post("https://www.macauslot.com/infoApi/cn/D/FB/matchs/results", json=data,headers=headers, proxies=proxies, timeout=10)
        print("getscoreinfo: json=", res.json())
        # # print("Content-Type=", res.headers['Content-Type'])
        # # print("data=",data['total'], " page=", data['pages'])
        # # # print("listinfo=",data['list'])
        # # # print("listlen=", len(data['list']))
        if res.status_code==200:
            data = res.json()['data']
            listinfo = data['list']
            tmptimeinfo = res.json()['sysTime']
            sportinfo.insert_score_maindata(listinfo, tmptimeinfo)
            
            for data in listinfo:
                print("getscoreinfo: currentPeriodStart=", data['currentPeriodStart'], " currentscore=", data['score']['current'], ' hometeamName=', data['hometeamName'], 
                ' awayteamName=', data['awayteamName'], " matchId=", data['matchId'])
                if data['score']['current'] == "0:0":
                    continue;
                try:
                    datainfo =  {
                        "matchId": data['matchId'], 
                        "type": "ft"
                        }
                    
                    print("datainfo=", datainfo)
                    resgoalcard = requests.post("https://www.macauslot.com/infoApi/cn/D/FB/matchs/goalcard", json=datainfo,headers=headers, proxies=proxies, timeout=10)
                    if resgoalcard.status_code==200:
                        print("getscoreinfo:resgoalcard=", resgoalcard.json())
                        data = resgoalcard.json()['data']
                        datalist = data['list'];
                        sysTime = resgoalcard.json()['sysTime']
                        sportinfo.insert_score_info(datalist, sysTime)
                    time.sleep(0.3)
                except Timeout:
                    # 请求超时处理
                    print("getscoreinfo:请求超时，请重试！")
                    time.sleep(1)
                except Exception as exc:
                    print("getscoreinfo:There was a problem: %s" %(exc))
                    time.sleep()
        
        # with open("news.txt","w",encoding="utf-8") as file:
        #     # 将每页网页的内容存进listpage文件夹中
        #     file.write(res.text)
    except Timeout:
        # 请求超时处理
        print("请求超时，请重试！")
    except Exception as exc:
        print("There was a problem: %s" %(exc))
    
def getOddsdata():
    print("getOddsdata: func begin")
    proxyMeta = 'socks5://customer-c7590e:13c780cc@proxy.ipipgo.com:31212'
    proxies = {
    "http": proxyMeta,
    "https": proxyMeta
}
    data =  {
        "nocache":1720833165134
        }


    print("proxies=", proxies)
    arrhomeawayinfo = []
    try:
        res = requests.post("https://www.macauslot.com/soccer/json/realtime/threeinone_event_cn_fb.json", 
                            json=data,headers=headers, proxies=proxies, timeout=10)
        if res.status_code==200:
            # print("json=", res.json())
            for data in res.json()['data']:
                event = data['event']
                print("home_team=", event['home_team'], " away_team=", event['away_team'], " eventname=", event['eventType']['name'], " ev_id=", event['ev_id'])
                homeawayinfo = {
                    "home_team":event['home_team'],
                    "away_team":event['away_team'],
                    "eventname":event['eventType']['name'],
                    "ev_id":event['ev_id'],
                    "start_time":event['start_time'],
                    "systime":res.json()['systime']
                }

                arrhomeawayinfo.append(homeawayinfo)
    except Timeout:
        # 请求超时处理
        print("请求超时，请重试！")
    except Exception as exc:
        print("There was a problem: %s" %(exc))

    # return

    try:
        res = requests.post("https://www.macauslot.com/soccer/json/realtime/threeinone_odds_cn_fb.json", 
                            json=data,headers=headers, proxies=proxies, timeout=10)
        # print("json=", res.json())
        
        
        
        allodddata = []
        for data in res.json()['data']:
            markets = data['markets']
            ev_id = data['ev_id']
            StandardHomeRate = ""
            StandardawayRate = ""
            StandarddrawRate = "" #平局

            HandicapHomeRate = ""
            HandicapawayRate = ""
            Handicapawayhcapdisp = ""

            UpperlowerplateHomeRate = ""
            UpperlowerplateawayRate = ""
            Upperlowerawayhcapdisp = ""
            HomeName = ""
            AwayName = ""
            for marketsinfo in markets:
                # print("marketsinfo11=", marketsinfo, "  name123=", marketsinfo['name'])
                if "標準盤" == marketsinfo['name']:
                    print("have 標準盤 marketsinfo=", marketsinfo)
                    outcomes = marketsinfo['outcomes']
                    for outcomesinfo in outcomes:
                        if outcomesinfo['type'] == "H":
                            StandardHomeRate = outcomesinfo['rate']
                        elif outcomesinfo['type'] == "D":
                            StandarddrawRate =  outcomesinfo['rate']
                        elif outcomesinfo['type'] == "A":
                            StandardawayRate = outcomesinfo['rate']
                    
                elif "讓球盤" == marketsinfo['name']:
                    print("have 讓球盤 marketsinfo=", marketsinfo)
                    for outcomesinfo in outcomes:
                        if outcomesinfo['type'] == "H":
                            HandicapHomeRate = outcomesinfo['rate']
                            HomeName = outcomesinfo['desc']
                        elif outcomesinfo['type'] == "A":
                            HandicapawayRate = outcomesinfo['rate']
                            AwayName = outcomesinfo['desc']
                    Handicapawayhcapdisp = marketsinfo['away_hcap_disp']
                elif "上/下盤" == marketsinfo['name']:
                    print("have 上/下盤 marketsinfo=", marketsinfo)
                    for outcomesinfo in outcomes:
                        if outcomesinfo['type'] == "H":
                            UpperlowerplateHomeRate = outcomesinfo['rate']
                        elif outcomesinfo['type'] == "A":
                            UpperlowerplateawayRate = outcomesinfo['rate']
                    Upperlowerawayhcapdisp = marketsinfo['away_hcap_disp']
            iteminfo = {
                "ev_id":ev_id,
                "StandardHomeRate":StandardHomeRate,
                "StandardawayRate":StandardawayRate,
                "StandarddrawRate":StandarddrawRate,
                "HandicapHomeRate":HandicapHomeRate,
                "HandicapawayRate":HandicapawayRate,
                "Handicapawayhcapdisp":Handicapawayhcapdisp,
                "UpperlowerplateHomeRate":UpperlowerplateHomeRate,
                "UpperlowerplateawayRate":UpperlowerplateawayRate,
                "Upperlowerawayhcapdisp":Upperlowerawayhcapdisp,
                "HomeName":HomeName,
                "AwayName":AwayName,
                "eventname":"", 
                "start_time":"",
                "systime":""
            }

            for tmpdata in arrhomeawayinfo:
                if tmpdata['ev_id'] == ev_id:
                    iteminfo["HomeName"] = tmpdata["home_team"]
                    iteminfo["AwayName"] = tmpdata["away_team"]
                    iteminfo["eventname"] = tmpdata["eventname"]
                    iteminfo["start_time"] = tmpdata["start_time"]
                    iteminfo["systime"] = tmpdata["systime"]
                    break
                
            allodddata.append(iteminfo)

        sportinfo.insert_odds_data(allodddata)
            # print("data=", data)
    except Timeout:
        # 请求超时处理
        print("请求超时，请重试！")
    except Exception as exc:
        print("There was a problem: %s" %(exc))

def odds_start():
   print("query_odds_interval=", setting.query_odds_interval, 
         " query_new_interval=", setting.query_new_interval,
         " query_main_score_interval=", setting.query_main_score_interval)
    # getOddsdata()
    # getscoreinfo()
    # getprematchbriefingdata()
    # getpostmatchbriefingdata()
#    getnewshighlightsdata()