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

p_vid = re.compile('(\d+)\.html')

def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url))
    videos = tree.xpath('//div[@id="main_play"]//li/a')
    if len(videos) == 0:
        videos = tree.xpath('//div[@class="overview"]//dt/a')

    ret = []
    for video in videos:
        try:
            title = video.xpath('./@title')[0]
            videoId = None
            if len(video.xpath('./@id')) > 0:
                videoId = video.xpath('./@id')[0]
            else:
                href = video.xpath('./@href')[0]
                videoId = re.search(r"getFlash\('(\d+)'\)", href).groups()[0]
            url = "http://www.boosj.com/%s.html" %videoId

            ret.append(buildResource(url, title, channelId, videoId))
        except Exception, e:
            print e
            continue

    return ret


def buildResource(url, title, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'boosj'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://subject.boosj.com/subject_50327.html',100055,1))
    pprint.pprint(handle('http://subject.boosj.com/subject_79887.html',100055,1))
