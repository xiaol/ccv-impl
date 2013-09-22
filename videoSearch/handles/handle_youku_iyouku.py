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


p_vid = re.compile('id_([^\._]+)')

'''
    根据用户的个人主页url 抽取该用户的共享视频和收藏视频（只抽取第一页）
'''
def handle(url, channelId, tvNumber):
    url = url.rstrip('/')

    #抽取该用户的共享视频
    html = get_html(url+'/videos')
    tree = etree.HTML(html)
    videoList = tree.xpath('//div[@class="items"]/ul[@class="v"]/li[@class="v_title"]/a')

    #抽取该用户的收藏视频
    html = get_html(url+'/videos')
    tree = etree.HTML(html)
    videoList.extend(tree.xpath('//div[@class="items"]/ul[@class="v"]/li[@class="v_title"]/a'))
    
    ret = []
    for video in videoList:
        title = video.xpath('./@title')[0]
        url = video.xpath('./@href')[0]
        videoId = p_vid.search(url).groups()[0]
        item = buildResource(url, title, -1, channelId, videoId)
        ret.append(item)

    return ret
    

def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'youku'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()
    

if __name__ == '__main__':
    #pprint.pprint(handle('http://i.youku.com/u/UNTMxOTkwNjA0',100527,3))
    pprint.pprint(handle('http://i.youku.com/u/UOTY0MzY0NjQ=/videos',100527,3))
