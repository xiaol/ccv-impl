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
    if url.startswith('http://cctv.cntv.cn/lm/tianxiazuqiu'):
        return handle_tianxiazuqiu(url, channelId)   # 处理《天下足球》
    else:
        return handle_normal(url, channelId)    # 处理其他栏目视频


# 处理《天下足球》栏目页面
def handle_tianxiazuqiu(url, channelId):
    tree = etree.HTML(get_html(url, "gbk"))
    links = tree.xpath('//a')

    ret = []
    exist = {}
    p_url = re.compile(r'http://sports.cntv.cn/\d{4}/\d{2}/\d{2}/\w+\.shtml')
    p_vid = re.compile(r'"videoCenterId"\s*,\s*"(\w+)"')
    for link in links:
        try:
            if not link.xpath('./@href') or not link.xpath('./text()'):
                continue
            url = link.xpath('./@href')[0]
            title = link.xpath('./text()')[0]
            if not p_url.search(url) or exist.get(url, False):
                continue
            exist[url] = True
            video_id = p_vid.search(get_html(url)).groups()[0]
            ret.append(buildResource(url, title, channelId, video_id))
        except:
            print(url)

    return ret


def handle_normal(url, channelId):
    return []


def buildResource(url, title, channelId, video_id):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'cntv'
    resource['videoId'] = video_id
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://cctv.cntv.cn/lm/tianxiazuqiu/', 100055, 1))
