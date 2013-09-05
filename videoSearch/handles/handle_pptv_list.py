# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from lxml import etree
import re, pprint
from common.common import getCurTime
from common.Domain import Resource, Channel
from common.HttpUtil import get_html
from setting import clct_channel

p_vid = re.compile('"vid":(\d+)')

def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url))
    videos = tree.xpath('//ul[contains(@class, "list_140x90")]/li/p[@class="txt"]/a')

    ret = []
    for video in videos:
        try:
            title = video.xpath('./@title')[0]
            url = video.xpath('./@href')[0]
            videoId = p_vid.search(get_html(url)).groups()[0]

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
    resource['videoType'] = 'pptv'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://list.pptv.com/sort_list/75340-75348.html',100055,1))
