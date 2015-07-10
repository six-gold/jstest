# coding=utf-8
import logging
import logging.config
from scrapy import Item

RESPONSE_ERROR_FORMAT = u"\t%(status)s\t%(url)s"
log4 = logging.getLogger('response')


class Logger(object):

    @staticmethod
    def log(item, name):
        if name == 'response':
            msg = {
                'status': item.get('response_status'),
                'url': item.get('url')
            }
            if msg:
                log4.info(RESPONSE_ERROR_FORMAT % msg)

def build_crawl_msg(item):
    """
    build structed crawler message with scrapy items
    """
    if not isinstance(item, Item):
        return None
    else:
        return {
            'url': item.get('url') or '',
            'crawled': item.get('crawl_stat'),
            'written': item.get('es_stat'),
            'origin_content_len': len(item.get('origin_content') or ''),
            'extracted_content_len': len(item.get('content') or ''),
            'claimed_lang': item.get('origin_lang') or '',
            'detected_lang': item.get('lang') or '',
        }

def build_page_msg(item):
    """
    build structed crawler message with scrapy items
    """
    if not isinstance(item, Item):
        return None
    else:
        return {
            'url': item.get('url') or '',
            'content': item.get('origin_content') or '',
        }