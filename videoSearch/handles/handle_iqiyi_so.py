# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re,pprint
from common.common import getCurTime
from pymongo import Connection
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel

p_vid = re.compile('data-player-videoid="(\w+?)"')
pps_vid = re.compile(r'"video_id":"(\d+)"')

'''
    只抽取第一页
'''
def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url))
    videos = tree.xpath('//div[@class="mod_sideright clearfix"]/ul/li/p/a')
    ret = []
    for video in videos:
        try:
            url = video.xpath('./@href')[0]
            title = video.xpath('./@title')[0]
            #搜索结果里会有pps网站上的视频
            if url.find("pps.tv/") != -1:
                videoId = pps_vid.search(get_html(url, "gbk")).groups()[0]
                video_type = "pps"
                ret.append(buildResource(url, title, channelId, videoId, video_type))
            else:
                videoId = p_vid.search(get_html(url)).groups()[0]
                ret.append(buildResource(url, title, channelId, videoId))
        except Exception, e:
            print e
            continue

    return ret


def buildResource(url, title, channelId, videoId, videoType='iqiyi'):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['type'] = 'video'
    resource['videoType'] = videoType
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://so.iqiyi.com/so/q_%E9%82%93%E5%B0%8F%E5%B9%B3',100095, 0))
    pprint.pprint(handle('http://so.iqiyi.com/so/q_%E5%B9%BF%E6%92%AD%E4%BD%93%E6%93%8D',100128, 0))

