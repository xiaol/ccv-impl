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


p_video = [
    re.compile('http://my.tv.sohu.com/[a-z]{2}/\d+/\d+\.shtml'),
    re.compile('http://tv.sohu.com/\d+/\w+\.shtml')
]


def handle(url, channelId, tvNumber):
    html = get_html(url, 'gbk')
    tree = etree.HTML(html)
    videos = tree.xpath('//a')

    ret = []
    exist = {}
    for video in videos:
        url = video.xpath('./@href')[0]
        is_video = False
        for p_vid in p_video:
            if p_vid.search(url):
                is_video = True
                break
        if not is_video or exist.get(url, False):
            continue
        exist[url] = True
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
    pprint.pprint(handle('http://tv.sohu.com/tech/',100649,3))

