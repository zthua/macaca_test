__author__ = 'sara'

import unittest
from time import sleep

from appium.webdriver.common.touch_action import TouchAction

from testSet import MyDriver
import testSet as Log
from testSet import Element
import readConfig as readConfig
import testSet as bcommon

readConfigLocal = readConfig.ReadConfig()


class TestReceive(unittest.TestCase):

    def setUp(self):
        # get Driver
        self.driver = MyDriver.get_driver()
        # self.caseNo = self.case_name

        # get Log
        self.log = Log.MyLog().get_log()
        self.logger = self.log.get_my_logger()

        self.number_phone = readConfigLocal.getConfigValue("phoneNumber")

        # test Start
        self.log.build_start_line("Test receive bitcoins")

    def testReceive(self):

        isOk = True
        # 如果登陆 先登出
        if Element("me", "me").is_exist():
            bcommon.logout()

        bcommon.login()

        while not Element("Transactions", "Transactions").is_exist():
            sleep(1)

        Element("Transactions", "Transactions").click()

        Element("Transactions", "receive").click()

        phone_number = Element("Transactions", "phone_number").get_attribute("value").replace(" ", "")

        if self.number_phone not in phone_number:
            self.logger.info("phone number is not show")
            isOk = False

        if not Element("Transactions", "qr_code").is_exist():
            self.logger.info("qr code is not show")
            isOk = False

        if not Element("Transactions", "bitcoin_address").is_exist():
            self.logger.info("bitcoin address is not show")
            isOk = False

        # Element("Transactions", "share_icon").click()
        #
        # if not Element("Transactions", "share_apps").is_exist():
        #     self.logger.info("share_apps address is not show")
        #     isOk = False
        # else:
        #     Element("comm", "cancel").click()

        if isOk:
            self.log.write_result("receive bitcoins OK")
        else:
            self.log.write_result("receive bitcoins NG")


    def tearDown(self):

        TouchAction(self.driver).tap(x=28, y=40).perform()
        bcommon.logout()
        # test end
        self.log.build_end_line("Test receive bitcoins")