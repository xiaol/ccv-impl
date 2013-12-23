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

p_vid = re.compile('id_([\w=]+?).html')
p_title = re.compile(r'\stitle=["\'](.*?)["\'][\s>]')


def handle(url,channelId,tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//div[@class="v-meta-title"]/a[2]')

    ret = []
    for video in videoList:
        title = etree.tostring(video, encoding="utf-8", method="html").decode("utf-8")
        title = p_title.search(title).groups()[0]
        url = video.xpath('./@href')[0]
        videoId = p_vid.search(url).groups()[0]

        item = buildResource(url, title, channelId, videoId)
        ret.append(item)
    return ret

def buildResource(url, title, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'youku'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://www.soku.com/search_video/q_%E5%8D%B1%E6%9C%BA%E8%BE%B9%E7%BC%98',1,3))
