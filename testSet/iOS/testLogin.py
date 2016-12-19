__author__ = 'sara'

import unittest
import logging
from common import get_element
from common import ReadConfig
from common import bsnsCommon
from time import sleep

logger = logging.getLogger()

get_element = get_element


class TestLogin(unittest.TestCase):

    def setUp(self):

        self.number_phone = ReadConfig.get_value("config", "phoneNumber")

        # test Start
        logger.info("Test login (not first login)")

    def test_login(self):
        sleep(2)
        if get_element("me", "me") is not None:
            bsnsCommon.logout()

        bsnsCommon.login()

        while get_element("me", "me") is None:
            sleep(1)

        get_element("me", "me").click()

        phone_number = get_element("me", "user_phone").get_property("value")

        logger.info("phone_number ===========>"+phone_number)

        self.check_login(phone_number)

        # bcommon.logout()

    def check_login(self, number):
        value = number.replace(" ", "")

        if self.number_phone in value:
            logger.info("login OK")
        else:
            logger.info("login NG")

        # action = TouchAction(self.driver)
        # action.press(5, 358).perform()

    def tearDown(self):
        bsnsCommon.logout()
        # test end
        logger.info("Test login (not first login)")