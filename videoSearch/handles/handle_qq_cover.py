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


def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url))
    videos = tree.xpath('//div[@id="period_content"]//li[@class="item"]/a')

    ret = []
    p_vid = re.compile('vid:\s*["\'](\w+)["\']')
    for video in videos:
        try:
            title = video.xpath('./text()')[0]
            url = "http://v.qq.com" + video.xpath('./@href')[0]
            videoId = p_vid.search(get_html(url)).groups()[0]
            ret.append(buildResource(url, title, channelId, videoId))
        except Exception, e:
            print(e, url)

    return ret


def buildResource(url, title, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'qq'
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://v.qq.com/cover/9/9s03hqx0qorycem.html',100055,1))