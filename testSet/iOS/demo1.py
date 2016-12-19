__author__ = 'tongshan'

import unittest

from testSet import MyDriver
import testSet as Log


class Demo1(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        global log, logger
        self.driver = MyDriver.get_driver()
        log = Log.MyLog.get_log()
        logger = log.get_my_logger()

        logger.info("start test demo1")

    def test_01(self):
        element = self.driver.find_element_by_name("Clear")
        element.click()

        element = self.driver.find_element_by_name("1")
        element.click()

        log.take_shot("test")


    # 退出时的清理工作 e.g.删除产生的环境垃圾，退出登陆的用户
    def tearDown(self):
        logger.info("end test demo1")

