from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from login import Login
from register import Register
from comment import Comment

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.set_window_position(0, 0)
    driver.set_window_size(720, 1100)

    account = {
        'email': "lazada1243@gmail.com",
        'name': "Nguyen Hoang Long",
        'password': "nguyenhoanglong89"
    }
    commentData = {
        'rating': 5,
        'title': "Excited!!!",
        'comment': "This product is very great!!!"
    }
    product = {
        'site': "https://www.lazada.vn/apple-iphone-7-32gb-hong-hang-nhap-khau-7629048.html?spm=a2o4n.home.sku-feed-slider-with-banner_452505.12.1cFAdR"
    }

    login = Login()
    register = Register()
    comment = Comment()

    resutl = login.performLogin(driver, account)
    if resutl is not None:
        resutl = register.performRegister(driver, account)
        if resutl is None:
            comment.giveComment(driver, account, product, commentData)
    else:
        comment.giveComment(driver, account, product, commentData)

