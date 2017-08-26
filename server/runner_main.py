import time
import threading
from database.user_dao import UserDao
from runners.auto_price_worker import AutoPriceWorker
from config import RunnerConfig


if __name__ == "__main__":

  starttime=time.time()
  userDao = UserDao();

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

    time.sleep(60.0 - ((time.time() - starttime) % 60.0))






