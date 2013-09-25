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

p_vid = re.compile('http://video.baomihua.com/[^/]+/(\d+)')


def handle(url, channelId, tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//ul[@id="J_video_list"]/li/a')

    ret = []
    for video in videoList:
        url = video.xpath('./@href')[0]
        title = video.xpath('./@title')[0]
        video_id = p_vid.search(url).groups()[0]
        item = buildResource(url, title, video_id, -1, channelId)
        ret.append(item)

    return ret


def buildResource(url, title, video_id, hot, channelId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['hot'] = hot
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['type'] = 'video'
    resource['videoType'] = 'baomihua'
    resource['videoId'] = video_id
    resource['createTime'] = getCurTime()
    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://www.baomihua.com/funny_212',100121,0))
