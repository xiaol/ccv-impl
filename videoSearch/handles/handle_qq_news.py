# -*- coding: utf-8 -*-
__author__ = 'klb3713'


import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re, pprint, json
from common.common import getCurTime
from common.Domain import Resource
from common.HttpUtil import get_html


def handle(url, channelId, tvNumber):
    today_news = get_html('http://v.qq.com/c/todayHot.js')
    left = today_news.find('{')
    right = today_news.rfind('}')
    videos = json.loads(today_news[left:right+1])["data"]

    ret = []
    for video in videos:
        title = video["title"]
        url = video["url"]
        videoId = video["vid"]

        ret.append(buildResource(url, title, channelId, videoId))

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
    pprint.pprint(handle('http://v.qq.com/news/', 100055, 1))