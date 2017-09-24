import time
from database.user_dao import UserDao
from cronjob.get_order_worker import GetOrderWorker
from config import CronJob


if __name__ == "__main__":

  userDao = UserDao()
  superAdmin = userDao.getSuperAdmin()

  while True:
    if (superAdmin):
      clone = GetOrderWorker({"user": superAdmin})
      try:
        clone.daemon = True
        clone.start()
      except Exception as ex:
        clone.join(0)
        print ("Error: unable to start thread: ", ex)

    time.sleep(CronJob.GET_ORDER_TIME_INTEVAL)






