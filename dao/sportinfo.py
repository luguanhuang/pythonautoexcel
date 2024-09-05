from utils.sql_helper import sql_helper
# from utils.sql_helper import db2_sql_helper
from utils.log import sportlogger
import time

def insert_news_info(listinfo, sysTime):
    for data in listinfo:
        print("datatag=", data['tags'], " imageUri=", data['imageUri'], ' title=', data['title'], 
    #   ' reportTime=', data['reportTime'], ' images=', data['images'], ' titleZht=',  data['titleZht'],
            ' reportTime=', data['reportTime'], ' images=', data['images'])
        # print("image=", data['images'])
        titleinfo = data['images'][0]['title']
        # titleinfo = data['images']
        # print("titleinfo****************************=", titleinfo)
        # return
        sql = """
        SELECT * FROM newsinfo where title=%s
        """
        resdata = sql_helper.fetch_one(sql, (data['title']))
        cnt = 0
        if resdata is not None and resdata != False:
            cnt = len(resdata)

        if (cnt > 0):
            # sql = """
            #     update newsinfo set reportTime=%s, imageUri=%s, newsTypeName=%s, content=%s where title=%s
            #     """
            sametitletime = data['reportTime']
            if resdata['sametitletime'] != None:
                if sametitletime in resdata['sametitletime']:
                    sametitletime = resdata['sametitletime']
                else:
                    sametitletime = resdata['sametitletime']  + ","+data['reportTime']
            sql = """
                update newsinfo set reportTime=%s, imageUri=%s, newsTypeName=%s, content=%s, sysTime=%s, subtitle=%s, sametitletime=%s  where title=%s
                """
            print("sql=", sql)
            ret = sql_helper.update(sql, (data['reportTime'], data['imageUri'], data['newsTypeSimpleName'], data['content'],
                                                sysTime, titleinfo, sametitletime, data['title']))
        else:
            # sql = """
            #     insert into newsinfo(title, reportTime, imageUri, images, newsTypeName, content) values(%s, %s, %s, %s, %s, %s)
            #     """
            sql = """
                insert into newsinfo(title, reportTime, imageUri, newsTypeName, content, sysTime, subtitle, sametitletime) values(%s,%s,%s,%s,%s, %s, %s, %s)
                """
            print("sql111=", sql)   
            # ret = sql_helper.update(sql, (data['title'], data['reportTime'], data['imageUri'], 
            #                                     data['images'], data['newsTypeName'], data['content']))
            ret = sql_helper.update(sql, (data['title'], data['reportTime'], data['imageUri'], data['newsTypeSimpleName'], data['content'], sysTime,
                                          titleinfo, data['reportTime']))

   


def insert_score_maindata(listinfo, sysTime):
    for data in listinfo:
        print("currentPeriodStart=", data['currentPeriodStart'], " currentscore=", data['score']['current'], ' hometeamName=', data['hometeamName'], 
            ' awayteamName=', data['awayteamName'], " sysTime=", sysTime)
        sql = """
        SELECT * FROM scoremaindata where currentPeriodStart=%s and hometeamName=%s and awayteamName=%s
        """
        resdata = sql_helper.fetch_one(sql, (data['currentPeriodStart'], data['hometeamName'], 
                                    data['awayteamName']))
        cnt = 0
        if resdata is not None and resdata != False:
            cnt = len(resdata)

        if (cnt > 0):
            sql = """
                update scoremaindata set cornerscore=%s, currentscore=%s, matchId=%s, startDate=%s, lastUpdateTime=%s where currentPeriodStart=%s and hometeamName=%s and awayteamName=%s
                """
            print("sql=", sql)
            ret = sql_helper.update(sql, (data['corner']['current'], data['score']['current'], data['matchId'], data['startDate'], data['lastUpdateTime'],
                                          data['currentPeriodStart'], data['hometeamName'], data['awayteamName']))
        else:
            sql = """
                insert into scoremaindata(currentPeriodStart, currentscore, hometeamName, awayteamName, sysTime, cornerscore, matchId, startDate, lastUpdateTime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            print("sql111=", sql)   
            ret = sql_helper.update(sql, (data['currentPeriodStart'], data['score']['current'], data['hometeamName'], data['awayteamName'], sysTime,
                                            data['corner']['current'], data['matchId'], data['startDate'], data['lastUpdateTime']))
            


def insert_score_info(listinfo, sysTime):
    for data in listinfo:
        print("matchId=", data['matchId'], " teamId=", data['teamId'], ' clock=', data['clock'], ' typeCode=', data['typeCode'])
        sql = """
        SELECT * FROM scoreinfo where matchId=%s and teamId=%s and clock=%s and typeCode=%s
        """
        resdata = sql_helper.fetch_one(sql, (data['matchId'], data['teamId'], 
                                    data['clock'], data['typeCode']))
        cnt = 0
        if resdata is not None and resdata != False:
            cnt = len(resdata)

        if (cnt > 0):
            i=1
            sql = """
                update scoreinfo set teamId=%s, clock=%s, typeCode=%s, sysTime=%s where matchId=%s
                """
            print("sql=", sql)
            ret = sql_helper.update(sql, (data['teamId'], data['clock'], data['typeCode'], sysTime,data['matchId']))
        else:
            sql = """
                insert into scoreinfo(matchId, teamId, clock, typeCode, sysTime) values(%s,%s,%s,%s,%s)
                """
            print("sql111=", sql)   
            ret = sql_helper.update(sql, (data['matchId'], data['teamId'], data['clock'], data['typeCode'], sysTime))



def insert_odds_data(allodddata):
    for data in allodddata:
        # print("matchId=", data['matchId'], " teamId=", data['teamId'], ' clock=', data['clock'], ' typeCode=', data['typeCode'])
        sql = """
        SELECT * FROM oddsdata where ev_id=%s
        """
        resdata = sql_helper.fetch_one(sql, (data['ev_id']))
        cnt = 0
        if resdata is not None and resdata != False:
            cnt = len(resdata)

        if (cnt > 0):
            sql = """
                update oddsdata set HomeName=%s, AwayName=%s, StandardHomeRate=%s, StandardawayRate=%s, StandarddrawRate=%s, HandicapHomeRate=%s, HandicapawayRate=%s, Handicapawayhcapdisp=%s, UpperlowerplateHomeRate=%s, UpperlowerplateawayRate=%s, Upperlowerawayhcapdisp=%s, eventname=%s, start_time=%s, systime=%s where ev_id=%s
                """
            print("sql=", sql)
            ret = sql_helper.update(sql, (data['HomeName'], data['AwayName'], data['StandardHomeRate'], data['StandardawayRate'], data['StandarddrawRate'], data['HandicapHomeRate'], 
                                          data['HandicapawayRate'], data['Handicapawayhcapdisp'], data['UpperlowerplateHomeRate'], data['UpperlowerplateawayRate'], data['Upperlowerawayhcapdisp'], 
                                          data['eventname'], data['start_time'], data['systime'], data['ev_id']))
        else:
            sql = """
                insert into oddsdata(ev_id, HomeName, AwayName, StandardHomeRate, StandardawayRate, StandarddrawRate, HandicapHomeRate, HandicapawayRate, Handicapawayhcapdisp, UpperlowerplateHomeRate, UpperlowerplateawayRate, Upperlowerawayhcapdisp, eventname, start_time, systime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            print("sql111=", sql)   
            ret = sql_helper.update(sql, (data['ev_id'], data['HomeName'], data['AwayName'], data['StandardHomeRate'], data['StandardawayRate'], data['StandarddrawRate'], data['HandicapHomeRate'], 
                                          data['HandicapawayRate'], data['Handicapawayhcapdisp'], data['UpperlowerplateHomeRate'], data['UpperlowerplateawayRate'], data['Upperlowerawayhcapdisp'], 
                                          data['eventname'], data['start_time'], data['systime']))
            


def query_odds_data():
    print("query_odds_data: func begin")
#     sql = """
#    select * from oddsdata od JOIN Keywords ks ON cks.CategoryKeywordID = ks.CategoryKeywordID limit 0, 20
#     """
    
#     sql = """
#    select * from oddsdata limit 0, 20
#     """
    
    sql = """
   select * from oddsdata oa left join scoremaindata sd on oa.HomeName = sd.hometeamName and oa.AwayName=sd.awayteamName and oa.start_time= sd.startDate left join newsinfo ni on oa.HomeName = ni.hometeamName
    """

    resdata = sql_helper.fetch_all_noparam(sql)
    cnt = 0
    if resdata is not None and resdata != False:
        cnt = len(resdata)

    
    arroddsdata = []
    if 0 == cnt:
        return arroddsdata
    for row in resdata:
        currentscore = ""
        if row['currentscore'] is not None:
            currentscore = row['currentscore']
        tmpdata = {
            'start_time':row['start_time'],
            'eventname':row['eventname'],
            'HomeName':row['HomeName'],
            'AwayName':row['AwayName'],
            # 'HandicapHomehcapdisp':row['HandicapHomehcapdisp'],
            'HandicapHomehcapdisp':row['Handicapawayhcapdisp'],
            'HandicapHomeRate':row['HandicapHomeRate'],
            'Handicapawayhcapdisp':row['Handicapawayhcapdisp'],
            'HandicapawayRate':row['HandicapawayRate'],
            "currentscore":currentscore
            # 'eventname':row['eventname'],
            # 'eventname':row['eventname'],
            # 'eventname':row['eventname']
            
        }

        arroddsdata.append(tmpdata);

    return arroddsdata