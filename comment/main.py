from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from login import Login
from register import Register
from comment import Comment
from increase_view import IncreaseView
from importer.excel import ImportExcel

if __name__ == "__main__":

    commentData = {
        'rating': 5,
        'title': "Excited!!!",
        'comment': "This product is very great!!!"
    }
    product = {
        'site': "http://www.lazada.vn/thuoc-kich-thich-moc-long-may-rau-toc-snor-x3-thai-lan-10309753.html?spm=a2o4n.seller-37384.0.0.42ImOD&ff=1&sc=KwiS&mp=1&rs=37384"
    }

    # Read account
    importExcel = ImportExcel()
    accounts = importExcel.getAccounts()
    comments = importExcel.getComments()

    # Simple comment logic
    driver = webdriver.Chrome()
    driver.set_window_position(0, 0)
    driver.set_window_size(720, 1100)

    login = Login()
    register = Register()
    comment = Comment()
    increaseView = IncreaseView()

    j = 0;
    for i in range(13, 25):
        resutl = login.performLogin(driver, accounts[i])
        if resutl is not None:
            resutl = register.performRegister(driver, accounts[i])
            if resutl is None:
                # comment.giveComment(driver, accounts[i], product, comments[j])
                j = j + 1
        else:
            # comment.giveComment(driver, accounts[i], product, comments[j])
            increaseView.performIncrease(driver, account[i], product)
            j = j + 1

        if j == 2:
            break

