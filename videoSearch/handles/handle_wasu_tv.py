# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import os
import sys
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re, pprint
from common.common import getCurTime
from common.Domain import Resource
from common.HttpUtil import get_html


p_number = re.compile('\d+')


def handle(url, channelId, tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)

    links = tree.xpath('//ul[@class="gather"]/li/a')

    ret = []
    for link in links:
        url = link.xpath('./@href')[0]
        title = link.xpath('./text()')[0]
        number = int(p_number.search(title).group())
        if number <= tvNumber:
            continue

        ret.append(buildResource(url, title, number, channelId, url))

    # 检测完结
    if re.search(u'(\d+)集全', html):
        ret.append("over")

    return ret



def buildResource(url, title, number, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'wasu'
    resource['videoId'] = url
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://www.wasu.cn/Tele/index/id/1818652',100055,-1))
    pprint.pprint(handle('http://www.wasu.cn/Tele/index/id/1723861',100055,-1))

