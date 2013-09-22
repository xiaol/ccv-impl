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


p_vid = re.compile(r'video/([^/]+)$')


def handle(url, channelId, tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//div[@class="wf_cell video box "]')

    ret = []
    for video in videoList:
        title = video.xpath('//span[@class="desc"]/text()')[0]
        url = "http://www.weipai.cn" + video.xpath('//a[@class="whole video_link"]/@href')[0]
        videoId = p_vid.search(url).groups()[0]
        item = buildResource(url, title, -1, channelId, videoId)
        ret.append(item)

    return ret


def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'weipai'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://www.weipai.cn/square/',100527,3))
