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
    videos = tree.xpath('//div[contains(@class, "relevance_video")]//p[@class="mt5"]/a[@class="result_link"]')

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
    resource['videoType'] = 'wasu'
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://www.wasu.cn/Search/show/k/%E6%88%91%E6%98%AF%E7%89%B9%E7%A7%8D%E5%85%B5%E4%B9%8B%E7%81%AB%E5%87%A4%E5%87%B0/type/0', 100649, 3))
