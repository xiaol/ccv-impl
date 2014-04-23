# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import os,sys
sys.path += [os.path.dirname(os.path.dirname(__file__))]
import re
import pprint
from lxml import etree
from common.common import getCurTime
from common.Domain import Resource
from common.HttpUtil import get_html


def handle(url, channelId, tvNumber):
    p_prefix = re.compile(r'http://my.tv.sohu.com/pl/\d+/')
    videos = []
    if p_prefix.search(url):
        list_url = p_prefix.search(url).group() + 'index.shtml'
        html = get_html(url)
        tree = etree.HTML(html)
        videos = tree.xpath('//ul[@class="uList cfix"]/li/strong/a')

    ret = []
    for video in videos:
        url = video.xpath('./@href')[0]
        title = video.xpath('./@title')[0]
        item = buildResource(url, title, channelId, url)
        ret.append(item)

    return ret


def buildResource(url, title, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'sohu_url'
    resource['videoId'] = url
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://my.tv.sohu.com/pl/5083492/index.shtml',100649,3))

