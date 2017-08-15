# import datetime
# import time
# import schedule
# from schedule import every
# from lazada_api.lazada_order_api import LazadaOrderApi
# from managers.order_manager import OrderManager
# from managers.constant_manager import ConstantManager

# if __name__ == "__main__":

#   def job():
#     print("Update Failed Order Automatically")

#     orderManager = OrderManager()
#     userDao = UserDao()
#     constantManager = ConstantManager()

#     users = userDao.getAllUser()
#     for user in users:
#       constant = constantManager.getConstantWithUserId(user['lazada_user_id'])
#       orderManager.insertOrderFromLazadaWithOneUser(user, constant)



#   schedule.every().day.at("20:55").do(job)
#   while True:
#       schedule.run_pending()
#       time.sleep(1)






