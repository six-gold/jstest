"""
phantomJs driver pool
Use a Queue store all the driver, after the driver used it will be put back to the Queue
The best way to do this is: when the crawler start sent a signal to driver pool, then start
initial the drive pool, when the crawler closed sent a signal to driver pool close the driver
pool.
"""
import random
from scrapy import signals
from scrapy.utils.project import get_project_settings
import Queue
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scrapy.xlib.pydispatch import dispatcher

project_setting = get_project_settings()


class WebDriverPool(object):
    def __init__(self):
        self.pool_size = project_setting.get('DRIVER_POOL_SIZE')
        self.driver_queue = Queue.Queue(maxsize=self.pool_size)
        dispatcher.connect(self.init_queue, signals.spider_opened)
        dispatcher.connect(self.clean, signals.engine_stopped)

    def init_queue(self):
        '''
        init the driver pool
        :return:
        '''
        for i in range(self.pool_size):
            desire_cap = DesiredCapabilities.PHANTOMJS.copy()
            user_agent = random.choice(project_setting.get('USER_AGENTS'))
            desire_cap["phantomjs.page.settings.userAgent"] = user_agent
            desire_cap['phantomjs.page.customHeaders.User-Agent'] = user_agent
            self.driver_queue.put(webdriver.PhantomJS(desired_capabilities=desire_cap))

    def get_driver(self):
        '''
        get a driver from the driver queue
        :return: a webdriver
        '''
        return self.driver_queue.get()

    def put_driver(self, driver):
        '''
        when a driver used return it to pool queue
        :param driver: a webdriver
        :return:
        '''
        self.driver_queue.put(driver)

    def clean(self):
        '''
        when the spider quit clean the pool
        :return:
        '''
        # print 'clean pool, pool size: %s' % self.pool_size
        for i in range(self.pool_size):
            self.driver_queue.get().quit()

driver_pool = WebDriverPool()