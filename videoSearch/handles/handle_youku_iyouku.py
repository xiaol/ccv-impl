# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re, pprint
from common.common import getCurTime
from common.Domain import Resource
from common.HttpUtil import get_html


p_vid = re.compile('id_([^\._]+)')
p_title = re.compile(r'\stitle=["\'](.*?)["\'][\s>]')

'''
    根据用户的个人主页url 抽取该用户的收藏视频（只抽取第一页）
'''
def handle(url, channelId, tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//div[@class="v-meta-title"]/a')
    
    ret = []
    for video in videoList:
        title = etree.tostring(video, encoding="utf-8", method="html").decode("utf-8")
        title = p_title.search(title).groups()[0]
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
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()
    

if __name__ == '__main__':
    pprint.pprint(handle('http://i.youku.com/u/UMjIxMTYyOTI0/videos',100527,3))
