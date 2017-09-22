import time
from database.user_dao import UserDao
from cronjob.get_product_worker import GetProductWorker
from config import CronJob


if __name__ == "__main__":

  userDao = UserDao()
  superAdmin = userDao.getSuperAdmin()

  isFirstTime = True;
  while True:
    if (superAdmin):
      clone = GetProductWorker({"user": superAdmin, "isFirstTime": isFirstTime})
      try:
        clone.daemon = True
        clone.start()
      except Exception as ex:
        clone.join(0)
        print ("Error: Unable to get products from lazada ", ex)

    isFirstTime = False
    time.sleep(CronJob.GET_PRODUCT_TIME_INTEVAL)






