import time
from database.user_dao import UserDao
from cronjob.get_order_worker import GetOrderWorker
from config import CronJob


if __name__ == "__main__":

  starttime=time.time()
  userDao = UserDao()

  while True:
    superAdmins = userDao.getSuperAdmin()
    if (superAdmins):
      for superAdmin in superAdmins:
        clone = GetOrderWorker({"user": superAdmin})
        try:
          clone.daemon = True
          clone.start()
        except Exception as ex:
          clone.join(0)
          print ("Error: unable to start thread: ", ex)

    time.sleep(CronJob.GET_ORDER_TIME_INTEVAL)






