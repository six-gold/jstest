# -*- coding: utf-8 -*-
import time

from twisted.internet import reactor, defer
from selenium.webdriver import PhantomJS
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver


def getDummyData(x):
    d = defer.Deferred()
    reactor.callLater(2, d.callback, x * 3)
    print '------'
    return d


def printData(d):
    print d


class Test():
    pass


if __name__ == '__main__':
    # d = getDummyData(3)
    # d.addCallback(printData)
    # reactor.callLater(4, reactor.stop)
    # reactor.run()
    # print '======'
    driver = globals()["PhantomJS"]()
    print isinstance(driver, PhantomJS)
    try:
        driver.get('http://fanyi.baidu.com/')
        time.sleep(30)
        RemoteWebDriver.quit(driver)
        driver.get('http://stackoverflow.com/questions/7634715/python-decoding-unicode-is-not-supported')
        time.sleep(30)
        RemoteWebDriver.quit(driver)
    finally:
        driver.service.stop()