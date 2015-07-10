#!/bin/env python
# -*- coding: utf-8 -*-
from urlparse import urlparse

domain_list = [
    'bestbuy.com',
    'download.cnet.com',
    'forum.xda-developers.com',
    'taringa.net',
    'smashboards.com',
    'mp3fiber.com',
    'classmates.com',
    'fichas.findthecompany.com.mx',
    'mediafire.com',
    'forums.anandtech.com'
]


def original_url_count(file_name):
    with open(file_name, 'r') as reader:
        for line in reader.readlines():
            domain = '{uri.netloc}'.format(uri=urlparse(line.split('\t')[0]))
            for d in domain_list:
                result[d] = d in domain and result[d] + 1 or 1


def test(file_name, error_log_result):
    with open(file_name, 'r') as reader:
        for line in reader.readlines():
            domain = '{uri.netloc}'.format(uri=urlparse(line.split('\t')[2]))
            for d in domain_list:
                if d in domain:
                    if d in error_log_result:
                        error_log_result[d] += 1
                    else:
                        error_log_result[d] = 1


if __name__ == '__main__':
    result = {}
    # test('a', result)
    for i in range(10):
        try:
            if int('301') < 400:
                continue
        except Exception:
            pass
        print i