import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from logger import getLogger
from mail import send_email
from sql import get_data

logger = getLogger()


def run(browser, data):
    try:
        if not data.miqaatList:
            logger.info("No miqaats to proccess")
            time.sleep(30)
            return

        browser.get('https://www.its52.com')
        login(browser, data.user)
        enter_miqaat(browser)
        process_all_miqaat(browser, data.miqaatList)
        logout(browser)
    except Exception as e:
        logger.error("Exception occured in run: " + str(e))


def init_chrome_browser():
    op = webdriver.ChromeOptions()
    op.add_argument('--headless')
    op.add_argument('--no-sandbox')
    op.add_argument("--disable-setuid-sandbox")
    op.add_argument('--disable-dev-shm-usage')
    op.add_argument('--disable-gpu')

    return webdriver.Chrome(options=op)


def init_firefox():
    op = webdriver.FirefoxOptions()
    op.add_argument('--headless')
    return webdriver.Firefox(options=op)


def login(browser, user):
    logger.info("logging in for: " + user.its)
    time.sleep(5)
    username_input = browser.find_element(by=By.NAME, value="txtUserName")
    username_input.send_keys(user.its)
    pwd_input = browser.find_element(by=By.NAME, value="txtPassword")
    pwd_input.send_keys(user.pwd)
    login_btn = browser.find_element(by=By.ID, value="btnLogin")
    login_btn.click()
    time.sleep(5)
    logger.info("logged in successfully")


def enter_miqaat(browser):
    miqaat_button = browser.find_element(by=By.CSS_SELECTOR, value=".lnkbtn.text-center")
    miqaat_button.click()
    time.sleep(6)
    logger.info("entered in miqaat list successfully")


def process_all_miqaat(browser, miqaatList):
    try:
        for miqaat in miqaatList:
            process_each_miqaat(browser, miqaat)
    except Exception as e:
        logger.error("Exception occured while proccessing miqaat \n" + str(e))


def process_each_miqaat(browser, miqaat):
    logger.info('Start Processing miqaat: ' + miqaat.name)
    get_element(browser, miqaat).click()
    time.sleep(6)
    check_if_miqaat_open(browser, miqaat)
    logger.info("Finished Processing miqaat: " + miqaat.name)


def check_if_miqaat_open(browser, miqaat):
    body = browser.find_element(by=By.TAG_NAME, value='body')
    html_txt = body.text.lower()
    if check_if_in_contains_string(html_txt, miqaat.contains_string.split(',')):
        logger.info('Pass has opend for miqaat' + miqaat.name)
        send_email(miqaat)
    else:
        logger.info('Pass has not opened for miqaat' + miqaat.name)


def check_if_in_contains_string(html_txt, contains_arr):
    for str in contains_arr:
        if str.lower() in html_txt:
            return True
    return False


def get_element(browser, miqaat):
    if miqaat.css_type == 'class':
        return browser.find_element(by=By.CLASS_NAME, value=miqaat.css_class)
    if miqaat.css_type == 'id':
        return browser.find_element(by=By.ID, value=miqaat.css_class)
    if miqaat.css_type == 'name':
        return browser.find_element(by=By.NAME, value=miqaat.css_class)
    if miqaat.css_type == 'value':
        xPathStr = "//input[@value='" + miqaat.css_class + "']"
        return browser.find_element(by=By.XPATH, value=xPathStr)


def logout(browser):
    browser.get('https://miqaat.its52.com/Logout.aspx')
    time.sleep(5)
    logger.info("logged out success")


def start():
    try:
        browser = init_firefox()
        dataDao = get_data()
        run(browser, dataDao)
    except Exception as e:
        logger.error("Exception occurred " + str(e))
    finally:
        browser.quit()


if __name__ == '__main__':
    while True:
        logger.info("\n---------------------------------------------------------------\n")
        try:
            start()
        except Exception as e:
            logger.error("Exception occured " + str(e))
        logger.info("\n---------------------------------------------------------------\n")
