# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import os,sys
sys.path += [os.path.dirname(os.path.dirname(__file__))]
import pprint
from lxml import etree
from common.common import getCurTime
from common.Domain import Resource
from common.HttpUtil import get_html


def handle(url, channelId, tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    videos = tree.xpath('//div[@class="charts_tab"]//div[contains(@class, "top_itemname")]/a')

    ret = []
    for video in videos:
        url = video.xpath('./@href')[0]
        title = video.xpath('./text()')[0]
        item = buildResource(url, title, channelId, url)
        ret.append(item)

    return ret


def buildResource(url, title, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'wasu'
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://tops.wasu.cn/show/cid/37', 100649, 3))

