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


p_vid = re.compile('/(\d+)\.html')


def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url))
    links = tree.xpath('//div[@class="list_seo"]/div/dl/dt/a')

    ret = []
    urls = {}
    for link in links:
        url = link.xpath('./@href')[0]
        if urls.get(url, None):
            continue
        else:
            urls[url] = 1
        title = link.xpath('./@title')[0]
        videoId = p_vid.search(url).groups()[0]
        ret.append(buildResource(url, title, channelId, videoId))

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
    pprint.pprint(handle('http://list.letv.com/list/c4_t230_vt-1_md_o1_d2_p.html',100055,-1))

