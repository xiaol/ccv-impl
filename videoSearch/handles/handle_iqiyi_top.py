# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import os
import sys
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

import re
import pprint
from lxml import etree
from common.common import getCurTime
from common.Domain import Resource
from common.HttpUtil import get_html
from setting import clct_channel

p_vid = re.compile('data-player-videoid="(\w+?)"')
p_tvId = re.compile(r'tvId:(\d+)')
pps_vid = re.compile(r'"video_id":"(\d+)"')

'''
    只抽取第一页
'''
def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url))
    videos = tree.xpath('//div[@id="tab_top50"]//a[@class="toplay"]')
    titles = tree.xpath('//div[@id="tab_top50"]//a[@class="topic"]/@title')
    ret = []
    for i, video in enumerate(videos):
        try:
            url = video.xpath('./@href')[0]
            title = titles[i]
            #搜索结果里会有pps网站上的视频
            if url.find("pps.tv/") != -1:
                videoId = pps_vid.search(get_html(url, "gbk")).groups()[0]
                video_type = "pps"
                ret.append(buildResource(url, title, channelId, videoId, video_type))
            else:
                html = get_html(url)
                videoId = p_vid.search(html).groups()[0]
                tvid = p_tvId.search(html).groups()[0]
                videoId = tvid + '__' + videoId
                ret.append(buildResource(url, title, channelId, videoId))
        except Exception, e:
            print e

    return ret


def buildResource(url, title, channelId, videoId, videoType='iqiyi'):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = videoType
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://top.iqiyi.com/yule.html',100095, 0))
    pprint.pprint(handle('http://top.iqiyi.com/tiyu.html',100128, 0))

