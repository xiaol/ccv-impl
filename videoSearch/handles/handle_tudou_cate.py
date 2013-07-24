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

p_vid = [re.compile('/([^/]+)/$'), re.compile('/([^/]+)\.html')]


def handle(url,channelId,tvNumber):
    tree = etree.HTML(get_html(url,'gbk'))
    videos = tree.xpath('//div[@class="showcase"]//h6[@class="caption"]/a')

    ret = []
    for video in videos:
        url = video.xpath('./@href')[0]
        title = video.xpath('./@title')[0]
        if len(title) == 0:
            title = video.xpath('./text()')[0]
        number = 0
        videoId = ""
        for vid in p_vid:
            try:
                videoId = vid.search(url).groups()[0]
                break
            except:
                continue
        ret.append(buildResource(url,title,number,channelId,videoId))

    return ret


def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'tudou'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://www.tudou.com/cate/ich15a409b429c-2d-2e-2f-2g-2h-2i-2j-2k-2l-2m-2n-2o-2so2pe-2pa1.html',1,1))

