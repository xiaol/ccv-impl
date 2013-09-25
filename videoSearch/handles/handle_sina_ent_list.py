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

p_vid = re.compile(r"vid:'(\d+)',")

def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url, 'gbk'))
    videos = tree.xpath('//div[@id="Page_1"]/div/h2/a')
    if not videos:
        videos = tree.xpath('//div[@id="Page_1"]//div/h4/a')

    ret = []
    for video in videos:
        try:
            url = video.xpath('./@href')[0]
            title = video.xpath('./text()')[0]
            videoId = p_vid.search(get_html(url)).groups()[0]
            ret.append(buildResource(url, title, channelId, videoId))
        except Exception, e:
            print(url, e)
            continue

    return ret


def buildResource(url,title,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'sina'
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://ent.sina.com.cn/bn/bgml/',100055,1))
    pprint.pprint(handle('http://ent.sina.com.cn/bn/korea/more.html',100055,1))