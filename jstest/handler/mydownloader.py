import random

import time
import chardet
from scrapy.utils.defer import mustbe_deferred
from scrapy.utils.project import get_project_settings
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
from twisted.internet import reactor
from scrapy.xlib.tx import HTTPConnectionPool
from scrapy.utils.misc import load_object
from scrapy.http import HtmlResponse
import traceback
from twisted.internet.threads import deferToThread
from jstest.handler.webdriverpool import driver_pool

project_setting = get_project_settings()


class SeleniumLogicDownloader(object):

    def __init__(self, agent=None):
        self._agent = agent

    def download(self, request):
        begintime = time.time()
        d = self._download(request)

        d.addCallback(self.parseData, request, begintime)
        return d

    def _download(self, request):
        d = deferToThread(self.phantom_download, request.url)

        def getOutput(result):
            return result

        d.addCallback(getOutput)
        # is it need error call back
        return d

    def parseData(self, htmldoc, request, begintime):
        request.meta['download_latency'] = time.time() - begintime
        return HtmlResponse(request.url, body=htmldoc, request=request, encoding='utf-8')

    def ajax_complete(self, web_driver, *args, **kwargs):
        try:
            return 0 == web_driver.execute_script("return jQuery.active") or \
                0 == web_driver.execute_script("return Ajax.activeRequestCount") or \
                0 == web_driver.execute_script("return dojo.io.XMLHTTPTransport.inFlight.length")
        except WebDriverException:
            pass

    def phantom_download(self, url, *args, **kwargs):
        desire_cap = DesiredCapabilities.PHANTOMJS.copy()
        user_agent = random.choice(project_setting.get('USER_AGENTS'))
        desire_cap["phantomjs.page.settings.userAgent"] = user_agent
        desire_cap['phantomjs.page.customHeaders.User-Agent'] = user_agent
        driver = webdriver.PhantomJS(desired_capabilities=desire_cap)
        # driver = driver_pool.get_driver()
        try:
            driver.set_page_load_timeout(project_setting.get('WAIT_PAGE_LOAD'))
            driver.set_window_size(1366, 768)
            print url, time.ctime()
            driver.get(url)
            print url, time.ctime()
        except Exception as e:
            print '%s %s' % (url, e.__class__.__name__)
            raise
        else:
            try:
                WebDriverWait(driver, project_setting.get('WAIT_JS_LOAD'))\
                    .until(self.ajax_complete, "Wait For JS Load Timeout")
                if project_setting.get("SCREEN_SHOT_SAVE_PATH"):
                    driver.save_screenshot(u'%s%s%s.png' %
                                           (project_setting.get("SCREEN_SHOT_SAVE_PATH"), '\\',
                                            url.replace(':', '').replace('/', '').replace('?', '')))
                try:
                    page = driver.page_source
                    return page
                except TypeError:
                    traceback.print_exc()
            except TimeoutException as e:
                raise LoadJsTimeoutException
        finally:
            # driver_pool.put_driver(driver)
            driver.quit()


class SeleniumDownloadHandler(object):
    """
    download interface
    """

    def __init__(self, settings):
        self._pool = HTTPConnectionPool(reactor, persistent=True)
        self._pool.maxPersistentPerHost = settings.getint('CONCURRENT_REQUESTS_PER_DOMAIN')
        self._pool._factory.noisy = False
        self._contextFactoryClass = load_object(settings['DOWNLOADER_CLIENTCONTEXTFACTORY'])
        self._contextFactory = self._contextFactoryClass()
        self._disconnect_timeout = 1

    def download_request(self, request, spider):
        myDownloader = SeleniumLogicDownloader()
        return myDownloader.download(request)

    def close(self):
        return self._pool.closeCachedConnections()


class LoadJsTimeoutException(WebDriverException):
    '''
    when load js timeout raise
    '''
    pass