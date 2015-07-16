# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.internet.threads import deferToThread


class JstestPipeline(object):
    def __init__(self):
        # pass
        self.file = open('items.txt', 'wb')

    def process_item(self, item, spider):
        deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        # line = '%s\n' % dict(item)['content']
        # url = dict(item)['url']
        content = dict(item)['content']
        # print url
        # with open(url.replace(':', '').replace('/', '').replace('?', '')) as writer:
        #     writer.write(dict(item)['content'])
        # self.file.write(url)
        self.file.write(content)
        return item