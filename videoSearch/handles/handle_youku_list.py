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


# 形如 http://sports.youku.com/toutiao 这样的页面里的所有视频 只获取第一页的视频
def handle_window_page(url, channelId):
    html = get_html(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//div[@class="yk-row"]//div[@class="v-meta-title"]/a')

    ret = []
    for video in videoList:
        try:
            title = video.xpath('./text()')[0]
            url = video.xpath('./@href')[0]
            videoId = p_vid.search(url).groups()[0]

            item = buildResource(url, title, channelId, videoId)
            ret.append(item)
        except:
            pass

    return ret


''' handle_youku_playlist 获取小合集的所有视频， handle_youku_list 只获取第一页的视频'''
def handle(url, channelId, tvNumber):
    if url.startswith('http://sports.youku.com'):
        return handle_window_page(url, channelId)
    elif url.startswith("http://auto.youku.com"):
        return handle_window_page(url, channelId)
    elif url.startswith("http://fun.youku.com"):
        return handle_window_page(url, channelId)

    html = get_html(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//div[@class="items"]/ul/li[@class="v_title"]/a')

    ret = []
    for video in videoList:
        title = video.xpath('./@title')[0]
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
    # pprint.pprint(handle('http://ent.youku.com/mingxing/mingxing',1,3))
    # pprint.pprint(handle('http://sports.youku.com/niuren',1,3))
    # pprint.pprint(handle('http://auto.youku.com/newcar',1,3))
    pprint.pprint(handle('http://auto.youku.com/',1,3))