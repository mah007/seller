import time
from database.user_dao import UserDao
from cronjob.get_product_worker import GetProductWorker
from config import CronJob


if __name__ == "__main__":

  userDao = UserDao()
  superAdmins = userDao.getSuperAdmin()
  if (superAdmins):
    clone = GetProductWorker({"user": superAdmins})
    try:
      clone.daemon = True
      clone.start()
    except Exception as ex:
      clone.join(0)
      print ("Error: unable to start thread: ", ex)



