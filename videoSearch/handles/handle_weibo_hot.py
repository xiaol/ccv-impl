# -*- coding: utf-8 -*-
__author__ = 'klb3713'

#coding=utf-8
import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from lxml import etree
import re, pprint
from common.common import getCurTime
from common.Domain import Resource,Channel
from common.HttpUtil import get_html, HttpUtil, getVideoInfoByUrl
from setting import TOKEN,APP_KEY
from setting import clct_channel

pps_vid = re.compile(r'"video_id":"(\d+)"')

def handle(url, channelId, tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    videos = tree.xpath('//li[@action-type="feed_list_media_video"]')
    ret = []
    for video in  videos:
        try:
            data = video.xpath("./@action-data")[0].split('&')
            item = {}
            for para in data:
                item[para.split('=')[0]] = para.split('=')[1]
            if item['full_url'].find("pps.tv/") != -1:
                videoid = pps_vid.search(get_html(item['full_url'], "gbk")).groups()[0]
                video_type = "pps"
                ret.append(buildResource(item['full_url'], item['title'], channelId, video_type, videoid))
            else:
                videoinfo = getVideoInfoByUrl(item['full_url'])
                video_type = videoinfo['videoType']
                videoid = videoinfo['videoId']
                ret.append(buildResource(item['full_url'], item['title'], channelId, video_type, videoid))
        except:
            print item
            continue

    return ret


def buildResource(url,title,channelId,videoType,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['type'] = 'video'
    resource['videoType'] = videoType
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    resource['modifyTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://hot.weibo.com/?v=1199', 131113, 1))
