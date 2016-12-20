__author__ = 'sara'

import unittest
from time import sleep

from testSet import MyDriver
import comm as common
import testSet as Log
from testSet import get_element, get_elements
import readConfig as readConfig
import testSet as bcommon

readConfigLocal = readConfig.ReadConfig()

get_element = get_element
get_elements = get_elements


class TestSend(unittest.TestCase):

    def setUp(self):
        # get Driver
        self.driver = MyDriver.get_driver()
        # self.caseNo = self.case_name

        # get Log
        self.log = Log.MyLog().get_log()
        self.logger = self.log.get_my_logger()

        self.number_phone = readConfigLocal.getConfigValue("phoneNumber")
        self.pin = readConfigLocal.getConfigValue("pin")

        self.send_number = "13764538998"
        self.send_address = "15DXAqZHZuDwXoKR3Q7Gr2Qny5UZKybvRx"

        # test Start
        self.log.build_start_line("Test send bitcoins")

    def testSend(self):

        sleep(2)
        if get_element("me", "me") is not None:
            bcommon.logout()

        bcommon.login()

        while get_element("wallets", "wallets") is None:
            sleep(1)

        get_element("wallets", "send").click()

        get_element("wallets", "phone_number").click()

        sleep(1)

        get_element("wallets", "phone_input").send_keys(self.send_number)

        get_element("comm", "continue").click()

        self.send_numbers("10")
        get_element("comm", "continue").click()
        sleep(2)

        get_elements("comm", "send")[2].click()

        get_element("comm", "confirm").click()

        comm.input_number(self.pin)

        self.check_result("Send bitcoins with phone number")

        get_element("comm", "close").click()

    def check_result(self, result_msg):

        if get_element("wallets", "transaction_successful") is not None:
            self.log.write_result(result_msg+" OK")
        else:
            self.log.write_result(result_msg+" NG")

    def send_numbers(self, number):

        sleep(1)
        number_list = list(number)

        int_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

        xpath = "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]" \
                "/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]" \
                "/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]" \
                "/XCUIElementTypeOther[1]/XCUIElementTypeButton[%s]"

        for a in number_list:
            if a == "0":
                s_xpath = xpath % "11"
                self.driver.element("xpath", s_xpath).click()
            if a in int_list:
                s_xpath = xpath % a
                self.driver.element("xpath", s_xpath).click()
            else:
                continue

    def tearDown(self):

        bcommon.logout()
        # test end
        self.log.build_end_line("Test send bitcoins")