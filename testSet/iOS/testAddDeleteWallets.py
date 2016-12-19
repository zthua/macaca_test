__author__ = 'sara'
import unittest
from time import sleep

from appium.webdriver.common.touch_action import TouchAction

from testSet import MyDriver
import testSet as Log
from testSet import Element
import testSet as bcommon


class TestAddDeleteWallets(unittest.TestCase):

    def setUp(self):
        # get Driver
        self.driver = MyDriver.get_driver()
        # self.caseNo = self.case_name

        # get Log
        self.log = Log.MyLog().get_log()
        self.logger = self.log.get_my_logger()

        # test Start
        self.log.build_start_line("Test add and delete wallets")

    def testAddDeleteWallets(self):
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

        # 添加 cny
        Element("Transactions", "CNY").click()
        Element("Transactions", "wallets_add").click()
        Element("Transactions", "USD").click()
        Element("Transactions", "wallets_add").click()
        Element("Transactions", "EUR").click()
        Element("Transactions", "wallets_add").click()
        Element("Transactions", "GBP").click()

        # 判断wallet添加成功
        w_list = ["CNY", "USD", "EUR", "GBP"]
        wallets = Element("Transactions", "wallets").get_element_list()

        isAddOk = True

        isDeleteOk = True
        name_list = []
        for wallet in wallets:
            wallet_name = wallet.get_attribute("name")
            name_list.append(wallet_name)

        for w in w_list:

            if w not in name_list:
                isAddOk = False
                break

        bcommon.delete_wallets(self.driver)

        wallets = Element("Transactions", "wallets").get_element_list()
        name_list = []

        for wallet in wallets:
            wallet_name = wallet.get_attribute("name")
            name_list.append(wallet_name)

        for w in w_list:

            if w in name_list:
                isDeleteOk = False
                break

        if isAddOk:
            self.log.write_result("Add wallet OK")
        else:
            self.log.write_result("Add wallet NG")

        if isDeleteOk:
            self.log.write_result("Delete wallet OK")
        else:
            self.log.write_result("Delete wallet NG")

    def tearDown(self):

        TouchAction(self.driver).tap(x=28, y=40).perform()

        bcommon.logout()
        # test end
        self.log.build_end_line("Test add wallets")