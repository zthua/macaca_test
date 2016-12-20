__author__ = 'sara'

import unittest
from time import sleep

from appium.webdriver.common.touch_action import TouchAction

from testSet import MyDriver
import testSet as Log
from testSet import Element
import testSet as bcommon
import comm as common


class TestConvertBetweenWallets(unittest.TestCase):

    def setUp(self):
        # get Driver
        self.driver = MyDriver.get_driver()
        # self.caseNo = self.case_name

        # get Log
        self.log = Log.MyLog().get_log()
        self.logger = self.log.get_my_logger()

        # test Start
        self.log.build_start_line("Test Convert Between the Wallets")

    def testConvertBetweenWallets(self):
        # 如果登陆 先登出
        if Element("me", "me").is_exist():
            bcommon.logout()

        bcommon.login()

        while not Element("Transactions", "Transactions").is_exist():
            sleep(1)

        Element("Transactions", "Transactions").click()
        Element("Transactions", "wallets_icon").click()

        bcommon.delete_wallets(self.driver)

        # 添加wallet
        Element("Transactions", "wallets_add").click()

        # 添加 usd
        Element("Transactions", "USD").click()

        # left slide the bits and convert
        bcommon.convert_bits(Element("Transactions", "bits").get(), self.driver)

        Element("Transactions", "wallet_amount1").click()

        comm.input_number("2000")

        sleep(3)

        Element("comm", "confirm").click()

        while not Element("comm", "close").is_exist():
            sleep(1)
        else:
            if Element("Transactions", "convert_successfully").is_exist():
                self.log.write_result("convert wallet between bits and USD OK")
            else:
                self.log.write_result("convert wallet between bits and USD NG")

            Element("comm", "close").click()

        Element("Transactions", "wallets_add").click()
        Element("Transactions", "CNY").click()

        sleep(3)
        AppNameHold = TouchAction(self.driver).press(Element("Transactions", "bits").get()).wait(2000)

        element = Element("Transactions", "CNY").get()
        location_y = element.location.get('y')-100
        location_x = element.location.get('x')
        AppNameHold.move_to(x=location_x, y=location_y).perform()

        Element("Transactions", "wallet_amount1").click()

        comm.input_number("1")

        error_msg = Element("Transactions", "convert_error_msg").get_attribute("value")

        # confirm_enable = Element("comm", "confirm").get_attribute("enable")

        if "Amount lower then min(10 bits)" == error_msg:
            self.log.write_result("check input amount can't less than 10 bits OK")
        else:
            self.log.write_result("check input amount can't less than 10 bits NG")

        comm.input_number("000")

        sleep(3)

        Element("comm", "confirm").click()

        while not Element("comm", "close").is_exist():
            sleep(1)
        else:
            if Element("Transactions", "convert_successfully").is_exist():
                self.log.write_result("convert wallet between bits and CNY OK")
            else:
                self.log.write_result("convert wallet between bits and CNY NG")

            Element("comm", "close").click()

        # 添加wallet
        Element("Transactions", "wallets_add").click()

        # 添加 usd
        Element("Transactions", "EUR").click()
        sleep(3)

        AppNameHold = TouchAction(self.driver).press(Element("Transactions", "USD").get()).wait(2000)

        element = Element("Transactions", "EUR").get()
        location_y = element.location.get('y')-100
        location_x = element.location.get('x')
        AppNameHold.move_to(x=location_x, y=location_y).perform()

        Element("Transactions", "wallet_amount1").click()

        comm.input_number("1")

        sleep(3)

        Element("comm", "confirm").click()

        while not Element("comm", "close").is_exist():
            sleep(1)
        else:
            if Element("Transactions", "convert_successfully").is_exist():
                self.log.write_result("convert wallet between USD and EUR OK")
            else:
                self.log.write_result("convert wallet between USD and EUR NG")

            Element("comm", "close").click()

        bcommon.convert_wallet(Element("Transactions", "CNY").get(), self.driver)

        Element("Transactions", "wallet_amount1").click()

        comm.input_number("1")

        sleep(3)

        Element("comm", "confirm").click()

        while not Element("comm", "close").is_exist():
            sleep(1)
        else:
            if Element("Transactions", "convert_successfully").is_exist():
                self.log.write_result("convert wallet between CNY and bits OK")
            else:
                self.log.write_result("convert wallet between CNY and bits NG")

            Element("comm", "close").click()

        bcommon.delete_wallets(self.driver)

    def tearDown(self):

        TouchAction(self.driver).tap(x=28, y=40).perform()
        self.log.take_shot("Test Convert Between the Wallets")

        bcommon.logout()
        # test end
        self.log.build_end_line("Test Convert Between the Wallets")