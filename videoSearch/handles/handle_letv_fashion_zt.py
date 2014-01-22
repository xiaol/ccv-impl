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


p_vid = re.compile('http://www.letv.com/ptv/vplay/(\d+)\.html')


def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url))
    links = tree.xpath('//dd/a')

    exist = {}
    ret = []
    for link in links:
        try:
            url = link.xpath('./@href')[0]
            videoId = p_vid.search(url).groups()[0]
            if exist.get(url, False):
                continue
            else:
                exist[url] = True
            title = link.xpath('./text()')[0]
            ret.append(buildResource(url, title, channelId, videoId))
        except:
            pass

    return ret


def buildResource(url, title, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'letv'
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://fashion.letv.com/zt/mfkt/index.shtml',100055,-1))

