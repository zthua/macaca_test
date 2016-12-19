import os
import logging
import configparser
import codecs
from xml.etree import ElementTree as elementTree

from .DRIVER import DRIVER
from . import prjDir

logger = logging.getLogger()
driver = DRIVER.driver
configfile_path = os.path.join(prjDir, "config", "config.ini")

def get_window_size():
    """
    get current windows size mnn
    :return:windowSize
    """
    global windowSize
    windowSize = driver.get_window_size()
    return windowSize


def my_swipe_to_up(during=None):
    """
    swipe UP
    :param during:
    :return:
    """
    # if windowSize == None:
    window_size = get_window_size()

    width = window_size.get("width")
    height = window_size.get("height")
    driver.swipe(width/2, height*3/4, width/2, height/4, during)


def my_swipe_to_down(during=None):
    """
    swipe down
    :param during:
    :return:
    """
    window_size = get_window_size()
    width = window_size.get("width")
    height = window_size.get("height")
    driver.swipe(width/2, height/4, width/2, height*3/4, during)


def my_swipe_to_left(during=None):
    """
    swipe left
    :param during:
    :return:
    """
    window_size = get_window_size()
    width = window_size.get("width")
    height = window_size.get("height")
    driver.swipe(width/4, height/2, width*3/4, height/2, during)


def my_swipe_to_right(during=None):
    """
    swipe right
    :param during:
    :return:
    """
    window_size = get_window_size()
    width = window_size.get("width")
    height = window_size.get("height")
    driver.swipe(width*4/5, height/2, width/5, height/2, during)


def input_number(number):
    """
    input the number
    :param :number
    :return:
    """
    number_list = list(number)

    int_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for a in number_list:
        if a in int_list:

            element = driver.element("name", a)
            element.click()
        else:

            continue


def clear_country(udid):
    """
    发送删除命令
    :return:
    """

    cmd = "adb shell -s %s input keyevent KEYCODE_DEL" % udid

    for i in range(5):
        os.system(cmd)


class ReadConfig:

    cf = None

    @classmethod
    def get_value(cls, section, name):

        if cls.cf == None:
            fd = open(configfile_path)
            data = fd.read()
            # remove BOM
            if data[:3] == codecs.BOM_UTF8:
                data = data[3:]
                file = codecs.open(configfile_path, "w")
                file.write(data)
                file.close()
            fd.close()

            cls.cf = configparser.ConfigParser()
            cls.cf.read(configfile_path)

        return cls.cf.get(section, name)


def back():
    os.popen("adb shell input keyevent 4")


activity = {}


def __set_xml():
    """
    get the xml file's value
    :use:
    a = getXml(path)

    print(a.get(".module.GuideActivity").get("skip").get("type"))
    :param: xmlPath
    :return:activity
    """
    if len(activity) == 0:

        OS = DRIVER.OS
        xml_path = os.path.join(prjDir, "config", "element_android.xml")
        if OS == "iOS":
            xml_path = os.path.join(prjDir, "config", "element_iOS.xml")

        # open the xml file
        per = elementTree.parse(xml_path)
        all_element = per.findall('activity')

        for firstElement in all_element:
            activity_name = firstElement.get("name")

            element = {}

            for secondElement in firstElement.getchildren():
                element_name = secondElement.get("name")

                element_child = {}
                for thirdElement in secondElement.getchildren():

                    element_child[thirdElement.tag] = thirdElement.text

                element[element_name] = element_child
            activity[activity_name] = element


def __get_el_dict(activity_name, element_name):
    """
    According to the activityName and elementName get element
    :param activity_name:
    :param element_name:
    :return:
    """
    __set_xml()
    element_dict = activity.get(activity_name).get(element_name)
    return element_dict

from macaca.webdriverexception import WebDriverException


def get_element(page_name, element_name):
    try:
        element_dict = __get_el_dict(page_name, element_name)
        path_type = element_dict.get("pathtype")
        path_value = element_dict.get("pathvalue")

        return driver.element(path_type, path_value)
    except WebDriverException:
        return None


def get_elements(page_name, element_name):
    try:
        element_dict = __get_el_dict(page_name, element_name)
        path_type = element_dict.get("pathtype")
        path_value = element_dict.get("pathvalue")

        return driver.elements(path_type, path_value)
    except WebDriverException:
        return None


