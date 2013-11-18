# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

import re
import pprint
from lxml import etree
from common.common import getCurTime
from common.Domain import Resource
from common.HttpUtil import get_html

p_vid = re.compile('/([^/]+)\.html')


def handle(url,channelId,tvNumber):
    tree = etree.HTML(get_html(url, 'gbk'))
    videos = []
    if url.startswith('http://www.ku6.com'):
        videos = tree.xpath('//div[@class="slide_tab2"]//div[@class="r_infor"]/h3/a')[:10]
    elif url.startswith('http://fashion.ku6.com'):
        videos = tree.xpath('//ul[@class="listTop"]/li//a')

    ret = []
    for video in videos:
        url = video.xpath('./@href')[0]
        title = video.xpath('./text()')
        if not title:
            continue
        else:
            title = title[0]
        videoId = p_vid.search(url).groups()[0]
        ret.append(buildResource(url, title, channelId, videoId))

    return ret


def buildResource(url, title, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'ku6'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    # pprint.pprint(handle('http://www.ku6.com/',1,1))
    pprint.pprint(handle('http://fashion.ku6.com/?hpsrc=1_29_6_0_0',1,1))