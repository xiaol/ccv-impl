# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import os
import sys
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from lxml import etree
import re
import pprint
from common.common import getCurTime
from common.Domain import Resource, Channel
from common.HttpUtil import get_html, downloadGif
from setting import clct_channel


def handle(url, channelId):
    tree = etree.HTML(get_html(url))
    images = tree.xpath('//img')

    ret = []
    for image in images:
        try:
            gif_url = image.xpath('./@src')[0]
            if not gif_url.endswith('.gif'):
                continue
            title = image.xpath('./@title')[0]
            if not title:
                title = image.xpath('./@alt')[0]
            videoId, resourceImageUrl = downloadGif(gif_url, channelId)
            if videoId and resourceImageUrl:
                ret.append(buildResource(gif_url, title, channelId, videoId, resourceImageUrl))
        except Exception, e:
            print(e, gif_url)
            continue

    return ret


def buildResource(url, title, channelId, videoId, resourceImageUrl):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'gif'
    resource['videoType'] = 'gif'
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()
    resource['resourceImageUrl'] = resourceImageUrl

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://onegif.com/', 100055))