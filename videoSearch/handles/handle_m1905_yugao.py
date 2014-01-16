# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re, pprint
from common.common import getCurTime
from common.Domain import Resource
from common.HttpUtil import get_html

p_vid = re.compile('http://www.m1905.com/video/play/(\d+)\.shtml')


def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url))
    videos = tree.xpath('//a')

    ret = []
    urls = {}
    for video in videos:
        try:
            url = video.xpath('./@href')[0]
            if not p_vid.search(url) or url in urls:
                continue
            urls[url] = True
            title = video.xpath('./text()')[0]
            videoId = p_vid.search(url).groups()[0]

            ret.append(buildResource(url, title, channelId, videoId))
        except Exception, e:
            print(e, url)
            continue

    return ret


def buildResource(url, title, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'm1905'
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://www.m1905.com/video/prevues/',100055,1))
