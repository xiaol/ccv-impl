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
    videos = tree.xpath('//ul[@class="vList"]/li')
    ret = []
    for video in videos:
        try:
            url = "http://www.zealer.com" + video.xpath('./div/a/@href')[0]
            title = video.xpath('./div/div[@class="subject"]/text()')[0]
            html = get_html(url)
            html = re.search("<embed.+</embed>", html).group()
            info = getVideoInfo(url, html)
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
    pprint.pprint(handle('http://www.zealer.com/', 100128, 1))

