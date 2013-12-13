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
    html = get_html(url)
    tree = etree.HTML(html)
    videos = tree.xpath('//a')

    ret = []
    p_link = re.compile(r'http://www.v1.cn/\d{4}-\d{2}-\d{2}/\d+\.shtml')
    links = {}
    for video in videos:
        url = video.xpath('./@href')[0]
        if not p_link.search(url) or links.get(url, False):
            continue
        links[url] = True
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
    resource['videoType'] = 'v1'
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://www.v1.cn/roll/1001/1.shtml', 100649, 3))

