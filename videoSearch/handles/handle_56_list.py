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

p_vid = [
    re.compile('vid-([^\.]+).html'),
    re.compile('v_([^\.]+).html'),
]


def handle(url,channelId,tvNumber):
    tree = etree.HTML(get_html(url))
    videos = []
    if url.startswith("http://www.56.com/p98/list"):
        videos = tree.xpath('//h2[@class="video_title"]/a')
    if not videos:
        videos = tree.xpath('//div[@class="m_v_list_txt"]/h6/a')
    if not videos:
        videos = tree.xpath('//div[@class="txt"]/a')
        
    ret = []
    for video in videos:
        url = video.xpath('./@href')[0]
        title = video.xpath('./text()')[0]
        videoId = None
        for p in p_vid:
            try:
                videoId = p.search(url).groups()[0]
            except:
                print url
                continue
            break
        if videoId:
            ret.append(buildResource(url,title,channelId,videoId))

    return ret


def buildResource(url,title,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = '56'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()
    

if __name__ == '__main__':
    # pprint.pprint(handle('http://ent.56.com/musicInfo/',100055,1))
    # pprint.pprint(handle('http://fun.56.com/znznv2/',100055,1))
    # pprint.pprint(handle('http://www.56.com/p98/list/',100055,1))
    pprint.pprint(handle('http://games.56.com/focus/',100055,1))
    pprint.pprint(handle('http://games.56.com/',100055,1))
