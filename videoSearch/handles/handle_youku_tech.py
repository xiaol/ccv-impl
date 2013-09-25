# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re, pprint
from common.common import getCurTime
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel

p_vid = re.compile('id_([^\._]+)')


def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url))
    videos = tree.xpath('//div[@class="yk-body"]//div[@class="v-meta-title"]/a')

    ret = []
    for video in videos:
        url = video.xpath('./@href')[0]
        title = video.xpath('./text()')[0]
        videoId = p_vid.search(url).groups()[0]
        number = -1
        ret.append(buildResource(url, title, number, channelId, videoId))

    return ret

def buildResource(url, title, number, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'youku'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://tech.youku.com/tansuo',1,1))

