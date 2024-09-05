"""全局变量 配置文件"""
from utils.load_yaml import config

httpport = config.get("http",{}).get("port")
tcpport = config.get("tcp",{}).get("port")


mysqlhost = "127.0.0.1"
mysqlport = 3306
mysqluser = "root"
mysqlpassword = ""
mysqldatabase = "sportinfo"

sqlhost = "127.0.0.1"
# sqlport = 3306
sqluser = "sa"
sqlpassword = "008541"
sqldatabase = "test2"
tds_version = "7.0"

query_new_interval=3600
query_main_score_interval=3600
query_odds_interval=3600

# db2_mysqlhost = "47.115.38.13"
# db2_mysqlport = 3306
# db2_mysqluser = "root"
# db2_mysqlpassword = "008541"
# db2_mysqldatabase = "dailyreportsdb"

