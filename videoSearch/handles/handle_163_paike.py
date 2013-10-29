# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from lxml import etree
import re,pprint
from common.common import getCurTime
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel


def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url, 'gbk'))
    videos = tree.xpath('//a')

    ret = []
    p_url = re.compile(r'http://v.163.com/paike/[^/]+/[^/]+\.html')
    for video in videos:
        url = video.xpath('./@href')
        if not url or not p_url.search(url[0]):
            continue
        url = url[0]
        title = video.xpath('./@title')
        if not title:
            title = video.xpath('./text()')[0]
        else:
            title = title[0]

        # ids = re.search(r"http://v.163.com/video/recommend/([^/]+)/([^/]+)/([^/]+)/([^/]+)\.xml",
        #                 get_html(url, 'gbk')).groups()
        # videoId = 'video/%s/%s/%s_%s' %(ids[1], ids[2], ids[0], ids[3])
        ret.append(buildResource(url, title, channelId))

    return ret


def buildResource(url,title,channelId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'netease'
    resource['videoId'] = url
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://v.163.com/paike/',100055,1))
