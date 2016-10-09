#!/bin/env python
import json
import os
from scrapy import signals, Request
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
import time
from twisted.internet import reactor
import multiprocessing as mul
from jstest.spiders.testSpider import TestSpider

reactor.suggestThreadPoolSize(30)
setting = get_project_settings()


class Manager(object):
    spiderCount = 0

    def __init__(self, spider_count=mul.cpu_count()):
        self._spider_count = spider_count

    def setup_crawler(self, spider):
        crawler = Crawler(get_project_settings())
        crawler.signals.connect(self.spider_closed, signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        self.crawler = crawler
        self.crawler.start()

    def setup_spider(self, url):
        if url is not None:
            spider = None
            if isinstance(url, list):
                spider = TestSpider(url_list=url)
            else:
                spider = TestSpider(url=url)
            # driver_pool.init_queue()
            self.setup_crawler(spider)
            self.spiderCount += 1

    def spider_closed(self):
        """
        call when spider closed
        """
        self.spiderCount -= 1
        if self.spiderCount == 0:
            # driver_pool.clean()
            reactor.stop()

    # def spider_idled(self, spider):
    # """
    # call when spider is idle,
    # get new url to crawl when one spider is idle
    #     """
    #
    #     urls = self.redis.blpop(self.url_list, 1)
    #     if urls:
    #         for url in json.loads(urls[1]):
    #             self.crawler.engine.schedule(Request(url), spider = spider)

    def run(self):
        print('%s: spider %d started' % (time.ctime(), os.getpid()))
        run_flag = False
        urls = [
            # 'http://deadspin.com/listen-to-sexual-harasser-isiah-thomas-lie-about-his-se-1702567139',
            # 'http://diply.com/humor-mag/funny-snapchat-screenshots/108708?_escaped_fragment_=',
            # 'http://diply.com/beinglatino/responses-to-suggestive-texts/122520?_escaped_fragment_=',
            # 'http://forum.huskermax.com/vbbs/showthread.php?73631-nebraska-unranked-in-espn-s-early-preseason-rankings/page8',
            # 'http://www.nakedcapitalism.com/2015/05/alicia-garcia-herrero-additional-monetary-easing-china.html',
            # 'http://bossip.com/1138688/bye-ghetto-street-bullies-jonathan-cheban-slams-amber-rose-blac-chyna-for-bullying-kylie/',
            # 'http://www.nationalreview.com/article/417958/how-martin-omalley-created-todays-baltimore-richard-j-douglas',
            # 'http://www.livestrong.com/search/?mode=standard&search=dehydration+symptoms',
            # 'http://la.curbed.com/archives/2015/05/no_one_wants_to_turn_pershing_square_into_an_urban_beach.php',
            # "http://blog.csdn.net/ljsbuct/article/details/8305921",
            # 'http://docs.seleniumhq.org/docs/07_selenium_grid.jsp#quick-start',
            # 'http://sap.ittoolbox.com/Error500.aspx?aspxerrorpath=/groups/technical-functional/sap-dev/sap-business-document-service-236430',
            # 'http://www.ajc.com/news/ap/sports/the-latest-barca-bayern-another-classic-euro-game/nk9r9/',  # 404 error
            # 'http://www.bizjournals.com/atlanta/morning_call/2015/05/cobb-officials-ok-proposed-40m-shopping-center.html',
            # 'http://www.nationalreview.com/article/417958/how-martin-omalley-created-todays-baltimore-richard-j-douglas',
            # 'https://l3com.taleo.net/careersection/l3_ext_us/jobsearch.ftl#',
            # 'http://america.aljazeera.com/articles/2015/5/6/el-salvador-gangs-target-police-after-failed-truce.html',
            # 'http://venturebeat.com/2015/05/06/joybits-launches-doodle-tanks-puzzle-game/',
            # 'http://www.rpp.com.pe/2015-05-05-eeg-revelan-fotos-de-sheyla-jazmin-y-angie-sin-maquillaje-noticia_794423.html',
            # 'http://www.bizjournals.com/atlanta/morning_call/2015/05/cobb-officials-ok-proposed-40m-shopping-center.html',
            # 'http://www.greekrank.com/uni/48/topic/657338/best-freshman-frat-pcs/',
            # 'http://www.wikihow.com/Do-a-Split',
            # 'http://peru.com/futbol/liga-de-campeones/barcelona-vs-bayern-munich-memes-que-dejo-encuentro-noticia-353580-1115221',
            # 'http://www.businessinsider.com/tesla-q1-earnings-report-may-6-2015-5',
            # 'http://angularjs.cn/A1aT',
            # 'http://www.myfoxphilly.com/story/28992925/authorities-find',
            # 'http://www.zdnet.com/article/hybrid-storage-taking-advantage-of-the-cloud/',
            # 'http://www.pcmag.com/article2/0,2817,2470353,00.asp',
            # 'http://www.eweek.com/blogs/storage-station/axcient-speeds-up-data-transfer-in-cloud-storage.html',
            # 'http://blog.seattlepi.com/football/2015/05/05/seattle-seahawks-have-history-of-giving-troubled-players-second-chances/#32769101=0',
            'http://www.cheatsheet.com/automobiles/the-13-fastest-modern-muscle-machines.html/?a=viewall'
        ]
        # with open('urls', 'r') as reader:
        #     for line in reader.readlines():
        #         urls.append(line.strip('\n'))

        self.setup_spider(urls)
        if self.spiderCount >= setting.get('SPIDER_COUNT'):
            run_flag = True
        if run_flag:
            reactor.run()
        print('%s: spider %d finished' % (time.ctime(), os.getpid()))


if __name__ == '__main__':
    manager = Manager(spider_count=setting.get('SPIDER_COUNT'))
    manager.run()