__author__ = 'sara'

import unittest
from time import sleep

from testSet import MyDriver
import testSet as Log
from testSet import get_element, get_elements
import readConfig as readConfig
import testSet as bcommon

readConfigLocal = readConfig.ReadConfig()

get_element = get_element
get_elements = get_elements


class TestConvert(unittest.TestCase):

    def setUp(self):
        # get Driver
        self.driver = MyDriver.get_driver()
        # self.caseNo = self.case_name

        # get Log
        self.log = Log.MyLog().get_log()
        self.logger = self.log.get_my_logger()

        self.number_phone = readConfigLocal.getConfigValue("phoneNumber")
        self.pin = readConfigLocal.getConfigValue("pin")

        # test Start
        self.log.build_start_line("Test convert")

    def testSend(self):

        sleep(2)
        if get_element("me", "me") is not None:
            bcommon.logout()

        bcommon.login()

        while get_element("wallets", "wallets") is None:
            sleep(1)

        get_element("wallets", "convert").click()

        get_element("wallets", "icon_convert").click()

        # while not get_element("common", "confirm").is_enabled():
        sleep(2)

        get_element("common", "confirm").click()
        sleep(1)

        self.check_result("convert bits to cny")

        get_element("common", "close").click()

    def check_result(self, result_msg):

        if get_element("wallets", "convert_successfully") is not None:
            self.log.write_result(result_msg+" OK")
        else:
            self.log.write_result(result_msg+" NG")

    def tearDown(self):

        get_element("wallets", "convert").click()

        get_element("wallets", "icon_convert").click()

        # while not get_element("common", "confirm").is_enabled():
        sleep(2)

        get_element("common", "confirm").click()
        sleep(1)

        get_element("common", "close").click()

        bcommon.logout()
        # test end
        self.log.build_end_line("Test convert")
