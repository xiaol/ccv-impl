# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import os
import sys
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

import re
import pprint
from lxml import etree
from common.common import getCurTime
from common.Domain import Resource, Channel
from common.HttpUtil import get_html, downloadGif
from setting import clct_channel


def handle(url, channelId):
    tree = etree.HTML(get_html(url))
    images = tree.xpath('//img')

    ret = []
    p_image_id = re.compile(r'/d/([\d-]+)/')
    for image in images:
        try:
            gif_url = "http://forgifs.com/gallery/" + image.xpath('./@src')[0]
            if not gif_url.endswith('.gif'):
                continue
            image_id = p_image_id.search(gif_url).groups()[0]
            real_image_id = str(int(image_id.split('-')[0]) - 1)
            gif_url = gif_url.replace(image_id.split('-')[0], real_image_id)
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
    pprint.pprint(handle('http://forgifs.com/gallery/main.php', 100056))