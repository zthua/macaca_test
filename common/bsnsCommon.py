import logging
from time import sleep
from appium.webdriver.common.touch_action import TouchAction
from .common import get_element
from .common import ReadConfig
from .common import input_number

logger = logging.getLogger()
get_element = get_element


def login():
    """
    login app
    :param email:
    :param password:
    :return:
    """
    number = ReadConfig.get_value("config", "phoneNumber")
    pin = ReadConfig.get_value("config", "pin")

    logger.debug("Begin login the app")

    get_element("common", "clear").click()

    input_number(number)

    get_element("Login", "next").click()

    while not get_element("Login", "SMS_verification") is None or not get_element("Login", "input_pin") is None:
        sleep(1)

    if get_element("Login", "SMS_verification") is not None:
        input_number("214638")

        while not get_element("Login", "input_pin") is None:
            sleep(1)

    # input pin
    input_number(pin)

    while get_element("me", "me") is None:
        sleep(1)

    logger.debug("End login the app")


def logout():
    """
    logout the app
    :return:
    """
    while get_element("me", "Settings") is None:

        get_element("me", "me").click()
        sleep(1)

    get_element("me", "Settings").click()

    get_element("me", "Sign_out").click()


def delete_wallets(driver):
        # 判断当前是否存在我们将要添加的wallet 若有 删除
        wallets = get_element("Transactions", "wallets").get_element_list()

        for wallet in wallets:

            wallet_name = wallet.get_attribute("name")
            # self.logger.info(wallet_name)

            # 将bits 移到第一个
            if wallet_name == "bits":

                AppNameHold = TouchAction(driver).press(wallet).wait(2000)

                element = get_element("Transactions", "wallets_add").get()
                AppNameHold.move_to(element).perform()
                break

        # 删除bits后面所有的wallet
        while get_element("Transactions", "wallets_second").is_exist():

            delete_wallet(get_element("Transactions", "wallets_second").get(), driver)


def delete_wallet(element, driver):
    location_y = swipe_wallet(element, driver)

    TouchAction(driver).tap(x=370, y=location_y+30).perform()

    if get_element("common", "confirm").is_exist():
        get_element("common", "confirm").click()

        sleep(3)


def convert_bits(element, driver):
    location_y = swipe_wallet(element, driver)

    TouchAction(driver).tap(x=370, y=location_y+30).perform()


def convert_wallet(element, driver):
    location_y = swipe_wallet(element, driver)

    TouchAction(driver).tap(x=280, y=location_y+30).perform()


def swipe_wallet(element, driver):
    location_y = element.location.get('y')

    driver.swipe(350, location_y+30, 80, location_y+30)

    return location_y


def back_index(driver):

    while not get_element("me", "me").is_exist():

        TouchAction(driver).tap(x=28, y=40).perform()
        sleep(1)
