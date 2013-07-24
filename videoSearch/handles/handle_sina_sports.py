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


def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url, "gbk"))
    ret = []

    #右侧导航栏视频
    videos = tree.xpath('//h3/a[@class="btn_video"]')
    for video in videos:
        try:
            url = video.xpath('./@data-url')[0]
            title = video.xpath('./@data-tit')[0]
            videoId = video.xpath('./@data-vid')[0].split('-')[0]
            ret.append(buildResource(url, title, channelId, videoId))
        except:
            print url
            continue

    #下方导航栏视频
    videos = tree.xpath('//div[@class="scroll_box"]/a[@class="fgrey02"]')
    for video in videos:
        try:
            url = video.xpath('./@href')[0]
            title = video.xpath('./text()')[0]
            p_vid = re.compile(r"vid:'(\d+)',")
            videoId = p_vid.search(get_html(url)).groups()[0]
            ret.append(buildResource(url, title, channelId, videoId))
        except:
            print url
            continue

    return ret


def buildResource(url,title,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'sina'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://sports.sina.com.cn/video/g/pl/#104750832',100055,1))
