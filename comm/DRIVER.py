# -*- coding: utf-8 -*-

import os
import re
import threading
import requests
import unittest
from requests.exceptions import ReadTimeout
from multiprocessing.pool import Pool
from time import sleep
from macaca import WebDriver
import comm

get_element = comm.get_element
DRIVER = comm.DRIVER


class InitDevice:
    """
    获取连接的设备的信息
    """
    def __init__(self):
        self.GET_ANDROID = "adb devices"
        self.GET_IOS = "instruments -s devices"

    def get_device(self):
        value = os.popen(self.GET_ANDROID)

        device = []

        for v in value.readlines():
            android = {}
            s_value = str(v).replace("\n", "").replace("\t", "")
            if s_value.rfind('device') != -1 and (not s_value.startswith("List")) and s_value != "":
                android['platformName'] = 'Android'
                android['udid'] = s_value[:s_value.find('device')].strip()
                android['package'] = 'com.btcc.mobi'
                android['activity'] = 'com.btcc.mobi.module.welcome.LaunchActivity'
                device.append(android)

        value = os.popen(self.GET_IOS)

        for v in value.readlines():
            iOS = {}

            s_value = str(v).replace("\n", "").replace("\t", "").replace(" ", "")

            if v.rfind('Simulator') != -1:
                continue
            if v.rfind("(") == -1:
                continue

            iOS['platformName'] = 'iOS'
            iOS['platformVersion'] = re.compile(r'\((.*)\)').findall(s_value)[0]
            iOS['deviceName'] = re.compile(r'(.*)\(').findall(s_value)[0]
            iOS['udid'] = re.compile(r'\[(.*?)\]').findall(s_value)[0]
            iOS['bundleId'] = 'com.btcc.mobiEntStaging'

            device.append(iOS)

        return device

def is_using(port):
    """
    判断端口号是否被占用
    :param port:
    :return:
    """
    cmd = "netstat -an | grep %s" % port

    if os.popen(cmd).readlines():
        return True
    else:
        return False


def get_port(count):
    """
    获得3456端口后一系列free port
    :param count:
    :return:
    """
    port = 3456
    port_list = []
    while True:
        if len(port_list) == count:
            break

        if not is_using(port) and (port not in port_list):
            port_list.append(port)
        else:
            port += 1

    return port_list


def _clear_country(udid):
    """
    发送删除命令
    :return:
    """

    os.popen("adb -s %s shell input keyevent KEYCODE_MOVE_END"% udid)

    cmd = "adb -s %s shell input keyevent KEYCODE_DEL" % udid

    for i in range(5):
        os.popen(cmd)

    os.popen("adb -s %s shell input keyevent KEYCODE_MOVE_END"% udid)


class macacaServer():
    def __init__(self, devices):

        self.devices = devices
        self.count = len(devices)
        self.cmd = 'macaca server -p %s --verbose'
        self.url = 'http://127.0.0.1:%s/wd/hub/status'

    def start_server(self):

        pool = Pool(processes=self.count)
        port_list = get_port(self.count)

        for i in range(self.count):
            pool.apply_async(self.run_server, args=(self.devices[i], port_list[i]))

        pool.close()
        pool.join()

    def run_server(self, device, port):

        r = RunServer(port)
        r.start()

        while not self.is_running(port):
            sleep(1)

        server_url = {
            'hostname': "ununtrium.local",
            'port': port,
        }
        driver = WebDriver(device, server_url)
        driver.init()

        DRIVER.set_driver(driver)
        DRIVER.set_OS(device.get("platformName"))

        if device.get("platformName") == "Android":

            while get_element("common", "permission_allow") is None:
                sleep(1)

            get_element("common", "permission_allow").click()

            sleep(5)
            get_element("Login", "country_code").click()
            _clear_country(device.get("udid"))
            driver.element("id", "com.btcc.mobi:id/country_code").send_keys("86")

        self.run_test()

    def run_test(self):
        """运行测试
        """
        all_test = AllTests()
        all_test.run_case()

    def is_running(self, port):
        """Determine whether server is running
        :return:True or False
        """
        url = self.url % port
        response = None
        try:
            response = requests.get(url, timeout=0.01)

            if str(response.status_code).startswith('2'):

                # data = json.loads((response.content).decode("utf-8"))

                # if data.get("staus") == 0:
                return True

            return False
        except requests.exceptions.ConnectionError:
            return False
        except ReadTimeout:
            return False
        finally:
            if response:
                response.close()


class RunServer(threading.Thread):

    def __init__(self, port):
        threading.Thread.__init__(self)
        self.cmd = 'macaca server -p %s --verbose' % port

    def run(self):
        os.system(self.cmd)


class AllTests:

    def __init__(self):
        self.cases_list_path = os.path.join(comm.prjDir, "config", "caseList.txt")
        self.case_path = os.path.join(comm.prjDir, "testSet")

    def get_case_list(self):
        """
        从caseList.txt 中获取
        :return:
        """
        case_list = []
        fp = open(self.cases_list_path)

        for data in fp.readlines():

            s_data = str(data)
            if s_data != '' and not s_data.startswith("#"):
                case_list.append(s_data.replace("\n", ""))
        fp.close()

        return case_list

    def create_suite(self):
        """from the caseList,get caseName,According to the caseName to search the testSuite
        :return:test_suite
        """
        case_list = self.get_case_list()
        test_suite = unittest.TestSuite()
        suite_module_list = []

        for case_name in case_list:

            discover = unittest.defaultTestLoader.discover(self.case_path, pattern=case_name+'.py', top_level_dir=None)
            suite_module_list.append(discover)

        for suite in suite_module_list:
            for test_name in suite:
                test_suite.addTest(test_name)

        return test_suite

    def run_case(self):

        suite = self.create_suite()

        runner = unittest.TextTestRunner()
        runner.run(suite)


if __name__ == "__main__":

    # try:
    #     response = requests.get("http://127.0.0.1:3456/wd/hub/status", timeout=0.01)
    # except requests.exceptions.ConnectionError:
    #
    #     print("error")

    i = InitDevice()

    m = macacaServer(i.get_device())
    m.start_server()