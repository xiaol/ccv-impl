# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re,pprint
from common.common import getCurTime
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel


'''只获取第一页的视频'''
def handle(url, channelId, tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//*[@id="mvlist"]/ul/li/div/h3/a')

    ret = []
    p_vid = re.compile('(\d+)$')
    for video in videoList:
        title = video.xpath('./@title')[0]
        url = video.xpath('./@href')[0]
        videoId = p_vid.search(url).groups()[0]

        item = buildResource(url, title, channelId, videoId)
        ret.append(item)

    return ret

def buildResource(url, title, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'yinyuetai'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://mv.yinyuetai.com/all',1,3))
