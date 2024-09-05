
from services.http.oddsservice import odds_start
from utils.task import task
import datetime 
def start():
    # 启动http服务
    # htttp_start()
    # task.add_job(htttp_start, "date", run_date=datetime.datetime.now() + datetime.timedelta(seconds=1))
    # asyncio.get_event_loop().run_forever()
    odds_start()


if __name__ == "__main__":
    start()