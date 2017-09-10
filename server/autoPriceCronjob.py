import time
from database.user_dao import UserDao
from cronjob.auto_price_worker import AutoPriceWorker
from config import CronJob


if __name__ == "__main__":

  starttime=time.time()
  userDao = UserDao()

  while True:
    users = userDao.getAll()
    if (users):
      for user in users:
        clone = AutoPriceWorker({"user": user})
        try:
          clone.daemon = True
          clone.start()
        except Exception as ex:
          clone.join(0)
          print ("Error: unable to start thread: ", ex)

    time.sleep(CronJob.AUTO_PRICE_TIME_INTEVAL)






