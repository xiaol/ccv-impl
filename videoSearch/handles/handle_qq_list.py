# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re, pprint, json
from common.common import getCurTime
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel

p_vid_1 = re.compile('/([^/]+)\.html')
p_vid_2 = re.compile('vid=(\w+)')


def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url))
    videos = tree.xpath('//div[@class="mod_cont"]/ul/li/h6/a')

    ret = []
    for video in videos:
        try:
            title = video.xpath('./text()')[0]
            url = video.xpath('./@href')[0]

            videoId = ""
            if p_vid_1.search(url):
                videoId = p_vid_1.search(url).groups()[0]
            elif p_vid_2.search(url):
                videoId = p_vid_2.search(url).groups()[0]
            else:
                pass
            if videoId:
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
    resource['videoType'] = 'qq'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://v.qq.com/games/list/501_50101/0/1_0.html',100055,1))