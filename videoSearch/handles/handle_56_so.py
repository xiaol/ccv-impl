# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from lxml import etree
import re,pprint
from common.common import getCurTime
from pymongo import Connection
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel

p_vid = [re.compile('v_([^\.]+).html'), re.compile('vid-([^\.]+).html')]


def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url))
    videos = tree.xpath('//*[@id="soSwitch"]/ul/li/div/h6/a')

    ret = []
    for video in videos:
        url = video.xpath('./@href')[0]
        title = video.xpath('./text()')[0]

        videoId = None
        for p in p_vid:
            try:
                videoId = p.search(url).groups()[0]
            except:
                print url
                continue
            break
        if videoId == None:
            continue
        ret.append(buildResource(url,title,channelId,videoId))
    return ret


def buildResource(url,title,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = '56'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://so.56.com/video/%E5%A5%A5%E5%B7%B4%E9%A9%AC/',100055,1))
