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

p_vid = re.compile('v_([^\.]+).html')


def handle(url,channelId,tvNumber):
    tree = etree.HTML(get_html(url))
    videos = tree.xpath('//a[@class="p_link"]')
        
    ret = []
    for video in videos:
        try:
            url = video.xpath('./@href')[0]
            title = video.xpath('./span[@class="m_txt"]/text()')[0]
            videoId = p_vid.search(url).groups()[0]
            ret.append(buildResource(url,title,channelId,videoId))
        except:
            pass

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
    pprint.pprint(handle('http://mm.56.com/',100055,1))