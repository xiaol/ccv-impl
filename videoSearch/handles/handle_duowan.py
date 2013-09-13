# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys, os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re, pprint
from common.common import getCurTime
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel
from handle_embed import getVideoInfo


'''
    只抽取第一页
'''
def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url))
    videos = tree.xpath('//div[@id="main"]/ul/li/a')
    ret = []
    for video in videos:
        try:
            url = "http://kan.duowan.com" + video.xpath('./@href')[0]
            title = video.xpath('./@title')[0]
            info = getVideoInfo(url)
            if info:
                ret.append(buildResource(info[0]["url"], title, channelId, info[0]["videoId"], info[0]["video_type"]))
        except:
            print url
            continue

    return ret


def buildResource(url, title, channelId, videoId, video_type):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = video_type
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://kan.duowan.com/1212/m_220294823394.html', 100128, 1))

