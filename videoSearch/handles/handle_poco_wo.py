# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import os
import sys
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from lxml import etree
import re,pprint
from common.common import getCurTime
from common.Domain import Resource
from common.HttpUtil import get_html


def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url, "gbk"))
    links = tree.xpath('//div[@class="video-box"]/p/a')

    ret = []
    p_url = re.compile(r'http://v.youku.com/v_show/id_\w+\.html')
    p_vid = re.compile('id_([\w=]+?).html')

    for link in links:
        try:
            url = link.xpath('./@href')[0]
            html = get_html(url, "gbk")
            video_url = p_url.search(html).group()
            video_id = p_vid.search(video_url).groups()[0]
            title = link.xpath('./strong/text()')[0]

            ret.append(buildResource(video_url, title, channelId, video_id))
        except:
            print(url)

    return ret


def buildResource(url, title, channelId, video_id):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'youku'
    resource['videoId'] = video_id
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://wo.poco.cn/alluregirls', 100055, 1))
