import time
from database.user_dao import UserDao
from cronjob.price_by_time_worker import PriceByTimeWorker
from config import CronJob


if __name__ == "__main__":

  starttime=time.time()
  userDao = UserDao()
  superAdmin = userDao.getSuperAdmin();

  while True:
    clone = PriceByTimeWorker({"user": superAdmin})
    try:
      clone.daemon = True
      clone.start()
    except Exception as ex:
      clone.join(0)
      print ("Error: unable to start thread: ", ex)

    time.sleep(CronJob.PRICE_BY_TIME_INTERVAL)






