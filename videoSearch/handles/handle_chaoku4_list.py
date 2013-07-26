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

p_vid = re.compile('html\?(\d+)-')

def handle(url,channelId,tvNumber):
    tree = etree.HTML(get_html(url, "gbk"))
    videos_div = tree.xpath('//div[@class="twC2"]')

    ret = []
    base_url = "http://www.chaoku4.com"
    for video in videos_div:
        try:
            title = video.xpath('./p[2]/text()')[0]
            url = base_url + video.xpath('./p[3]/a[1]/@href')[0]
            videoId = p_vid.search(url).groups()[0]
            ret.append(buildResource(url, title, channelId, videoId))
        except Exception, e:
            print e
            continue

    return ret


def buildResource(url,title,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'chaoku4'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://www.chaoku4.com/list/index2.html',100055,1))
    pprint.pprint(handle('http://www.chaoku4.com/list/index8.html',100055,1))
