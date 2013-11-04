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
from setting import clct_channel


p_number = re.compile(u'/subject/play/\d+/(\d+)')
p_vid = re.compile("['\"]*mp4['\"]*\s*?:\s*['\"](\w+)['\"]")
p_file = re.compile("['\"]*filename['\"]*\s*?:\s*['\"]([\w\.]+)['\"]")


def handle(url, channelId, tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    videos = tree.xpath('//a[@class="rankname"]')

    ret = []
    for video in videos:
        try:
            title = video.xpath('./@title')[0]
            url = 'http://www.funshion.com' + video.xpath('./@href')[0]
            html = get_html(url)
            videoId = p_vid.search(html).groups()[0]
            file_name = p_file.search(html)
            if file_name:
                videoId = videoId + '/' + file_name.groups()[0]
            item = buildResource(url, title, videoId, channelId)
            ret.append(item)
        except Exception, e:
            print(url, e)

    return ret


def buildResource(url, title, videoId, channelId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'funshion'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://www.funshion.com/list/video/o-z1',100550,3))
    # pprint.pprint(handle('http://www.funshion.com/list/sports/',100550,30))

