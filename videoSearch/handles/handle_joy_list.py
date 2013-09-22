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

# p_vid = re.compile('/([^/]+)\.htm')

def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url))
    videos = tree.xpath('//div[@class="msglist3"]/dl/dd/h3/a')

    ret = []
    for video in videos:
        url = video.xpath('./@href')[0]
        title = video.xpath('./@title')[0]
        # videoId = p_vid.search(url).groups()[0]
        number = -1
        ret.append(buildResource(url, title, number, channelId, url))

    return ret


def buildResource(url, title, number, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'joy_url'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://fashion.joy.cn/videolist/2_0_2/1.htm',1,1))
