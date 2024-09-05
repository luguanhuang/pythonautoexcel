from utils.sql_helper import sql_helper
from utils.sql_helper import db2_sql_helper
from utils.log import httplogger
import time

def select_Category_info():
    sql = """
    SELECT COUNT(DISTINCT SupplierID ) AS SupplierNum, COUNT(DISTINCT SubcategoryID) AS SubcategoryNum, Area, count(CleanedID) as TotalNum FROM CleanedServiceProducts group by Area
    """
    resdata = sql_helper.fetch_all_noparam(sql)
    cnt = 0
    if resdata is not None and resdata != False:
        cnt = len(resdata)
    
    SupplierNum = 0
    alldata = [];
    if (cnt > 0):
        for row in resdata:
            # print("row=", row)
            datainfo = {
                'servpartnersnum':row['SupplierNum'],
                'subcategorynum':row['SubcategoryNum'],
                'categorynum':0,
                'proservnum':row['TotalNum'],
                'Area':row['Area']
            }
            alldata.append(datainfo)

    sql = """
    SELECT CategoryID, SubcategoryID FROM Subcategories;
    """
    resdata = sql_helper.fetch_all_noparam(sql)
    cnt = 0
    if resdata is not None and resdata != False:
        cnt = len(resdata)

    arrCategory = []
    for row in resdata:
        tmpdata = {
            'CategoryID':row['CategoryID'],
            'SubcategoryID':row['SubcategoryID']
        }

        arrCategory.append(tmpdata);

    sql = """
    SELECT DISTINCT SubcategoryID AS SubcategoryID, Area FROM CleanedServiceProducts
    """
    resdata = sql_helper.fetch_all_noparam(sql)
    cnt = 0
    if resdata is not None and resdata != False:
        cnt = len(resdata)
    
    arrSubcategoryInfo = []
    if (cnt > 0):
        for row in resdata:
            if row['Area'] == None:
                continue
            tmpdata = {
                'SubcategoryID':row['SubcategoryID'],
                'Area':row['Area']
            }
            # print("tmpdata=", tmpdata)
            arrSubcategoryInfo.append(tmpdata);

    arrcalcCategory = {}
    categorycnt = 0
    for data in arrSubcategoryInfo:
        # print("111=", data['Area'])
        if data['Area']+str(data['SubcategoryID']) in arrcalcCategory.keys():
            continue
        for j in arrCategory:
            if j['SubcategoryID'] == data['SubcategoryID']:
                for k in alldata:
                    if k['Area'] == data['Area']:
                        k['categorynum']=k['categorynum']+1
                        # break
                        categoryID = j['CategoryID'];
                        resdata = k['Area']+str(categoryID)
                        # print("resdata=", resdata)
                        arrcalcCategory[k['Area']+str(categoryID)] = 1
                # categorycnt = categorycnt+1
                break

    return alldata;

def select_Keyword_popularity():
    sql = """
        WITH KeywordCategory AS (
        SELECT
            cks.CategoryKeywordID,
            cks.CategoryName,
            ks.KeywordID,
            ks.Keyword
        FROM
            CategoryKeywords cks
            JOIN Keywords ks ON cks.CategoryKeywordID = ks.CategoryKeywordID
        ),
        KeywordViews AS (
        SELECT
            kc.CategoryKeywordID,
            kc.CategoryName,
            kc.KeywordID,
            kc.Keyword,
            SUM(CAST(COALESCE(NULLIF(csp.Views, ''), '0') AS UNSIGNED)) AS sumview
        FROM
            KeywordCategory kc
            JOIN CleanedServiceProducts csp ON kc.KeywordID = csp.KeywordID
        GROUP BY
            kc.CategoryKeywordID,
            kc.CategoryName,
            kc.KeywordID,
            kc.Keyword
        ),
        RankedKeywordViews AS (
        SELECT
            kv.*,
            ROW_NUMBER() OVER (PARTITION BY kv.CategoryKeywordID ORDER BY kv.sumview DESC) AS rn
        FROM
            KeywordViews kv
        )
        SELECT
        CategoryKeywordID,
        CategoryName,
        KeywordID,
        Keyword,
        sumview
        FROM
        RankedKeywordViews
        WHERE
        rn <= 20
        ORDER BY
        CategoryKeywordID,
        sumview DESC;
    """
    resdata = sql_helper.fetch_all_noparam(sql)
    cnt = 0
    if resdata is not None and resdata != False:
        cnt = len(resdata)

    return resdata
    

def select_Service_popularity():
    sql = """
        WITH SubcategoryCategory AS (
        SELECT
        c.CategoryID,
        c.CategoryName,
        sb.SubcategoryID,
        sb.SubcategoryName
        FROM
        Categories c
        JOIN Subcategories sb ON c.CategoryID = sb.CategoryID
        ),
        SubcategoryViews AS (
        SELECT
        sc.CategoryID,
        sc.CategoryName,
        sc.SubcategoryID,
        sc.SubcategoryName,
        SUM(CAST(COALESCE(NULLIF(csp.Views, ''), '0') AS UNSIGNED)) AS sumview
        FROM
        SubcategoryCategory sc
        JOIN CleanedServiceProducts csp ON sc.SubcategoryID = csp.SubcategoryID
        GROUP BY
        sc.CategoryID,
        sc.CategoryName,
        sc.SubcategoryID,
        sc.SubcategoryName
        ),
        RankedSubcategoryViews AS (
        SELECT
        sv.*,
        ROW_NUMBER() OVER (PARTITION BY sv.CategoryID ORDER BY sv.sumview DESC) AS rn
        FROM
        SubcategoryViews sv
        )
        SELECT
        CategoryID,
        CategoryName,
        SubcategoryID,
        SubcategoryName,
        sumview
        FROM
        RankedSubcategoryViews
        WHERE
        rn <= 20
        ORDER BY
        CategoryID,
        sumview DESC
    """
    resdata = sql_helper.fetch_all_noparam(sql)
    cnt = 0
    if resdata is not None and resdata != False:
        cnt = len(resdata)
    return resdata

def select_Service_Ranking():
    sql = """
    SELECT ProductName, CreatedAt, Area, Views 
        FROM CleanedServiceProducts 
        WHERE Area IS NOT NULL AND Area != ''
        ORDER BY CAST(Views AS UNSIGNED) DESC 
        LIMIT 50
    """
    resdata = sql_helper.fetch_all_noparam(sql)
    cnt = 0
    if resdata is not None and resdata != False:
        cnt = len(resdata)
    arrServRanking = []
    if (cnt > 0):
        for row in resdata:
            servRanking = {
                'ProductName': row['ProductName'],
                'CreatedAt': row['CreatedAt'],
                'Area': row['Area'],
                'Views': row['Views']
            }
            arrServRanking.append(servRanking)            

    return arrServRanking 

def select_news(times):
    timebegin = ""
    timeend = ""
    if times == "today":
        timebegin = time.strftime('%Y-%m-%d 00:00:00', time.localtime())
        timeend = time.strftime('%Y-%m-%d 23:59:59', time.localtime())
    elif times == "yesterday":
        today = time.localtime()
        yesterday_timestamp = time.mktime(today) - 86400
        yesterday = time.localtime(yesterday_timestamp)
        timebegin = time.strftime('%Y-%m-%d 00:00:00', yesterday)
        timeend = time.strftime('%Y-%m-%d 23:59:59', yesterday)
    elif times == "recentlythreedays":
        today = time.localtime()
        threedays_timestamp = time.mktime(today) - 3*86400
        threedays = time.localtime(threedays_timestamp)
        timebegin = time.strftime('%Y-%m-%d 00:00:00', threedays)
        timeend = time.strftime('%Y-%m-%d 23:59:59', today)
    elif times == "recentlyoneweek":
        today = time.localtime()
        week_timestamp = time.mktime(today) - 7*86400
        week = time.localtime(week_timestamp)
        timebegin = time.strftime('%Y-%m-%d 00:00:00', week)
        timeend = time.strftime('%Y-%m-%d 23:59:59', today)
    elif times == "recentlyonemonth":
        today = time.localtime()
        month_timestamp = time.mktime(today) - 30*86400
        month = time.localtime(month_timestamp)
        timebegin = time.strftime('%Y-%m-%d 00:00:00', month)
        timeend = time.strftime('%Y-%m-%d 23:59:59', today)

    print("timebegin=", timebegin, " timeend=", timeend)
    
    sql = """
    SELECT  Title, NewTitle, GPTSummary , Content FROM AIGC_DailyReport_Info where DailyReportDate>=%s and DailyReportDate<= %s limit 20;
    """
    resdata = db2_sql_helper.fetch_all(sql, (timebegin, timeend))
    cnt = 0
    if resdata is not None and resdata != False:
        cnt = len(resdata)
    arrNews = []
    if (cnt > 0):
        for row in resdata:
            # print("Content=", row['Content'], " NewTitle=", row['NewTitle'])
            Newsinfo = {
                'Title': row['Title'],
                'Content': row['Content'],
                'Summary': row['GPTSummary']
            }
            arrNews.append(Newsinfo)            

    return arrNews

def select_Comm_Info():
    sql = """
    SELECT CommunicationResult FROM Communications;
    """
    resdata = sql_helper.fetch_all_noparam(sql)
    cnt = 0
    if resdata is not None and resdata != False:
        cnt = len(resdata)
    arrCommInfo = []
    replynum = 0
    contractnum = 0
    if (cnt > 0):
        for row in resdata:
            if row['CommunicationResult'] == "success":
                contractnum = contractnum+1
            elif row['CommunicationResult'] != "no_reply":
                replynum = replynum + 1
    resdata = {
        'sndnum':cnt,
        'replynum':replynum,
        'contactnum':contractnum
    }
    return resdata 

def select_Login_Info(username, passwd):
    sql = """
    SELECT * FROM Register where Username=%s and Passwd=%s;
    """
    resdata = sql_helper.fetch_all(sql, (username, passwd))
    cnt = 0
    if resdata is not None and resdata != False:
        cnt = len(resdata)
    return cnt

def select_Data_verview():
    today = time.localtime()
    yesterday_timestamp = time.mktime(today) - 86400
    yesterday = time.localtime(yesterday_timestamp)
    timebegin = time.strftime('%Y-%m-%d 00:00:00', yesterday)
    timeend = time.strftime('%Y-%m-%d 23:59:59', yesterday)
    print("timebegin=", timebegin, " timeend=", timeend)
    sql = """
    SELECT count(CleanedID) as TotalNum FROM CleanedServiceProducts where CreatedAt <= %s
    """
    resdata = sql_helper.fetch_one(sql, (timeend))
    yesterdaytotalcnt = 0
    if resdata is not None and resdata != False:
        yesterdaytotalcnt = len(resdata)
        
    if yesterdaytotalcnt > 0:
        yesterdaytotalcnt = resdata['TotalNum'];
        print("yesterdaytotalcnt=", yesterdaytotalcnt)

    sql = """
    SELECT count(CleanedID) as TotalNum FROM CleanedServiceProducts where CreatedAt >= %s and CreatedAt <= %s
    """
    resdata = sql_helper.fetch_one(sql, (timebegin, timeend))
    yesterdaycnt = 0
    if resdata is not None and resdata != False:
        yesterdaycnt = len(resdata)

    if yesterdaycnt > 0:
        yesterdaycnt = resdata['TotalNum'];
        print("yesterdaycnt=", yesterdaycnt)

    twodaysago_timestamp = time.mktime(today) - 2*86400
    twodaysago = time.localtime(twodaysago_timestamp)
    timebegin = time.strftime('%Y-%m-%d 00:00:00', twodaysago)
    timeend = time.strftime('%Y-%m-%d 23:59:59', twodaysago)
    print("timebegin=", timebegin, " timeend=", timeend)
    sql = """
    SELECT count(CleanedID) as TotalNum FROM CleanedServiceProducts where  CreatedAt <= %s
    """
    resdata = sql_helper.fetch_one(sql, (timeend))
    twodaysagocnt = 0
    if resdata is not None and resdata != False:
        twodaysagocnt = len(resdata)

    if twodaysagocnt > 0:
        twodaysagocnt = resdata['TotalNum'];
        print("twodaysagocnt=", twodaysagocnt)

    threedaysago_timestamp = time.mktime(today) - 3*86400
    threedaysago = time.localtime(threedaysago_timestamp)
    timebegin = time.strftime('%Y-%m-%d 00:00:00', threedaysago)
    timeend = time.strftime('%Y-%m-%d 23:59:59', threedaysago)
    print("timebegin=", timebegin, " timeend=", timeend)
    sql = """
    SELECT count(CleanedID) as TotalNum FROM CleanedServiceProducts where  CreatedAt <= %s
    """
    resdata = sql_helper.fetch_one(sql, (timeend))
    threedaysagocnt = 0
    if resdata is not None and resdata != False:
        threedaysagocnt = len(resdata)

    if threedaysagocnt > 0:
        threedaysagocnt = resdata['TotalNum'];
        print("threedaysagocnt=", threedaysagocnt)

    sql = """
    SELECT count(CleanedID) as TotalNum FROM CleanedServiceProducts
    """
    resdata = sql_helper.fetch_one_noparam(sql)
    totalcnt = 0
    if resdata is not None and resdata != False:
        totalcnt = len(resdata)

    if totalcnt > 0:
        totalcnt = resdata['TotalNum'];

    yesterdayrate = 0
    if twodaysagocnt != 0:
        yesterdayrate = (yesterdaytotalcnt-twodaysagocnt)*100/twodaysagocnt
    twodaysagorate = 0
    if twodaysagocnt != 0:
        twodaysagorate = (twodaysagocnt-threedaysagocnt)*100 / twodaysagocnt

    totalincrementpercent = 0
    if yesterdaytotalcnt != 0:    
        totalincrementpercent = (totalcnt-yesterdaytotalcnt)*100/yesterdaytotalcnt

    incrementpercent = 0
    if (yesterdaytotalcnt-twodaysagocnt) != 0:
        incrementpercent = (totalcnt-yesterdaytotalcnt)*100 / (yesterdaytotalcnt-twodaysagocnt)-1

    return totalcnt, totalincrementpercent, yesterdaytotalcnt, yesterdaytotalcnt-twodaysagocnt, totalcnt-yesterdaytotalcnt, incrementpercent, yesterdayrate, yesterdayrate-twodaysagorate,twodaysagorate

def select_Keyword_Prod_Relat():
    sql = """
       WITH RankedProducts AS (
        SELECT
            csp.KeywordID,
            ks.Keyword,
            CAST(COALESCE(NULLIF(csp.Views, ''), '0') AS UNSIGNED) AS Views,
            csp.Price,
            csp.Area,
                    csp.ProductName,
            ROW_NUMBER() OVER (PARTITION BY csp.KeywordID ORDER BY CAST(COALESCE(NULLIF(csp.Views, ''), '0') AS UNSIGNED) DESC) AS rn
        FROM
            CleanedServiceProducts csp
        JOIN
            Keywords ks ON csp.KeywordID = ks.KeywordID
        WHERE
            csp.Price IS NOT NULL
            AND csp.Views IS NOT NULL AND csp.Views != ''
            AND csp.Area IS NOT NULL AND csp.Area != ''
    )
    SELECT
        KeywordID,
        Keyword,
        Views,
        Price,
        Area,
            ProductName
    FROM
        RankedProducts
    WHERE
        rn <= 3
    ORDER BY
        KeywordID,
        Views DESC;
    """
    resdata = sql_helper.fetch_all_noparam(sql)
    cnt = 0
    if resdata is not None and resdata != False:
        cnt = len(resdata)
    return resdata
    # sql = """
    # select KeywordID, ProductName,Views, Price, Area from CleanedServiceProducts ORDER BY CAST(Views AS UNSIGNED) DESC 
    # """
    # tmpdata = sql_helper.fetch_all_noparam(sql)
    # cnt = 0
    # if tmpdata is not None and tmpdata != False:
    #     cnt = len(tmpdata)
    # alldata = []
    # if (cnt > 0):
    #     for row in tmpdata:
    #         alldata.append(row)
            

    # allresdata = []
    
    # sql = """
    # SELECT KeywordID, Keyword FROM Keywords;
    # """
    # resdata = sql_helper.fetch_all_noparam(sql)
    # cnt = 0
    # if resdata is not None and resdata != False:
    #     cnt = len(resdata)
    
    # if (cnt > 0):
    #     for row in resdata:
    #         tmpcnt = 0
    #         # print("KeywordID=", row['KeywordID'])
    #         for j in alldata:
    #             if j['KeywordID'] == row['KeywordID']:
    #                 # print("keyword=", j['KeywordID'])
    #                 tmpresdata = {
    #                     'Keyword':row['Keyword'],
    #                     'ProductName':j['ProductName'],
    #                     'Views':j['Views'],
    #                     'Price':j['Price'],
    #                     'Area':j['Area']
    #                 }

    #                 allresdata.append(tmpresdata)
    #                 tmpcnt = tmpcnt+1
    #                 if tmpcnt >=2:
    #                     break

    # return allresdata 

def select_Scripts_Category_Relat():
    sql = """
    SELECT csp.SubcategoryID, sb.SubcategoryName, cks.CategoryKeywordID, cks.CategoryName, st.ScriptID,st.ChatUpLine as ScriptName FROM CleanedServiceProducts csp INNER JOIN Subcategories sb on csp.SubcategoryID = sb.SubcategoryID INNER join CategoryKeywords cks on sb.CategoryID=cks.CategoryKeywordID  INNER JOIN Scripts st on csp.ScriptID= st.ScriptID 
    """
    resdata = sql_helper.fetch_all_noparam(sql)
    cnt = 0
    if resdata is not None and resdata != False:
        cnt = len(resdata)
    arrkeyinfo = []
    # httplogger.info(f"sql={sql}")
    if (cnt > 0):
        for row in resdata:
            # httplogger.info(f"KeywordID={row['KeywordID']}, sumview={row['sumview']}")
            # keyinfo = {
            #     'Keyword': row['Keyword'],
            #     'sumview': row['sumview'],
            #     'CategoryKeywordID':row['CategoryKeywordID'],
            #     'CategoryName':row['CategoryName']
            # }

            # arrkeyinfo.append(keyinfo)
            arrkeyinfo.append(row)
    return arrkeyinfo
    sql = """
    select ScriptID, SubcategoryID from CleanedServiceProducts limit 1000
    """
    tmpdata = sql_helper.fetch_all_noparam(sql)
    cnt = 0
    if tmpdata is not None and tmpdata != False:
        cnt = len(tmpdata)
    alldata = []
    if (cnt > 0):
        for row in tmpdata:
            tmpdata = {
                'ScriptID':row['ScriptID'],
                'SubcategoryID':row['SubcategoryID'],
                'ScriptName':"",
                'SubcategoryName':"",
                'CategoryName':"",
                'CategoryID':0
            }
            alldata.append(tmpdata)
            
    sql = """
    SELECT CategoryID, SubcategoryID, SubcategoryName FROM Subcategories;
    """
    resdata = sql_helper.fetch_all_noparam(sql)
    cnt = 0
    if resdata is not None and resdata != False:
        cnt = len(resdata)

    arrSubCategory = []
    if (cnt > 0):
        for row in resdata:
            tmpdata = {
                'CategoryID':row['CategoryID'],
                'SubcategoryID':row['SubcategoryID'],
                'SubcategoryName':row['SubcategoryName']
            }

            arrSubCategory.append(tmpdata);
    

    sql = """
    SELECT CategoryID, CategoryName FROM Categories;
    """
    resdata = sql_helper.fetch_all_noparam(sql)
    cnt = 0
    if resdata is not None and resdata != False:
        cnt = len(resdata)

    if (cnt > 0):
        arrCategory = []
        for row in resdata:
            tmpdata = {
                'CategoryID':row['CategoryID'],
                'CategoryName':row['CategoryName']
            }

            arrCategory.append(tmpdata);

    sql = """
    SELECT ScriptID, ChatUpLine FROM Scripts;
    """
    resdata = sql_helper.fetch_all_noparam(sql)
    cnt = 0
    if resdata is not None and resdata != False:
        cnt = len(resdata)

    arrScripts = []
    if (cnt > 0):
        for row in resdata:
            tmpdata = {
                'ScriptID':row['ScriptID'],
                'ScriptName':row['ChatUpLine']
            }

            arrScripts.append(tmpdata);

    arrexistScript = {}
    arrresdata = []
    for data in alldata:
        for j in arrSubCategory:
            if data['SubcategoryID'] == j['SubcategoryID']:
                data['Subcategoryname'] = j['SubcategoryName']
                data['CategoryID'] = j['CategoryID']
    for data in alldata:
        for j in arrCategory:
            if data['CategoryID'] == j['CategoryID']:
                data['CategoryName'] = j['CategoryName']

    for data in alldata:
        for j in arrScripts:
            if data['ScriptID'] == j['ScriptID']:
                data['ScriptName'] = j['ScriptName']

    return alldata 

def select_mqtt_aiot_by_id(clientid, imei, pw_mqtt):
    sql = """
    select token_num,expires_in from mqtt_aiot where imei=%s and clientid=%s and pw_mqtt=%s
    """
    print("sql=", sql, " imei=", imei, " clientid=", clientid, " pw_mqtt=", pw_mqtt)
    resdata = sql_helper.fetch_one(sql, (imei, clientid, pw_mqtt))
    return resdata
