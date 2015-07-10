# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.internet.threads import deferToThread


class JstestPipeline(object):
    def __init__(self):
        self.file = open('items.txt', 'wb')

    def process_item(self, item, spider):
        deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        line = '%s\n' % dict(item)['content']
        self.file.write(line)
        return item