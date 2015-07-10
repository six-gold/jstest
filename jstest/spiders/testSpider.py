#!/bin/env python
# -*- coding: utf-8 -*-
import re
from lxml import html
from scrapy import Spider

import sys
from jstest.itemloader import PageItemLoader
from jstest.items import JstestItem

reload(sys)
sys.setdefaultencoding("utf8")


class TestSpider(Spider):
    name = 'testSpider'

    def __init__(self, **kwargs):
        super(TestSpider, self).__init__(**kwargs)
        url = kwargs.get('url')
        url_list = kwargs.get('url_list')
        if url is not None:
            self.start_urls = [url]
        elif url_list is not None:
            self.ext = {}
            self.start_urls = url_list

    def parse(self, response):
        # if response.body is None:
        #     print 'body is None'
        #     return
        content = response.body
        # print content
        # remove scripts and css styles
        content = re.sub(r"<script[^>]*?>[\s\S]*?</script>", "", content)
        content = re.sub(r"<style[^>]*?>[\s\S]*?</style>", "", content)
        # remove redundant blanks
        content = re.sub(r"\s+", " ", content)
        # print response.request.url, html.fromstring(content).text_content().strip()
        loader = PageItemLoader(item=JstestItem(), response=response)
        loader.add_value('content', '%s\t%s' % (response.request.url, html.fromstring(content).text_content().strip()))
        return loader.load_item()