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

p_vid = re.compile('/([^/]+)\.html')
p_page_number = re.compile(r'/index_\d+_(\d+)\.html')

def handle(url,channelId,tvNumber):
    tree = etree.HTML(get_html(url, 'gbk'))
    first_page_url = tree.xpath('//div[@class="pages"]/a[1]/@href')[0]
    last_page_url = tree.xpath('//div[@class="pages"]/a[last()]/@href')[0]
    page_number = 1
    if p_page_number.search(last_page_url):
        page_number = int(p_page_number.search(last_page_url).groups()[0])

    videos = tree.xpath('//div[@class="innerViewLeft"]/dl/dt/a')
    if page_number > 1:
        for page_i in range(2, page_number+1):
            page_url = first_page_url.rstrip(".html") + '_' + str(page_i) + '.html'
            tree = etree.HTML(get_html(page_url, 'gbk'))
            videos.extend(tree.xpath('//div[@class="innerViewLeft"]/dl/dt/a'))

    ret = []
    for video in videos:
        url = video.xpath('./@href')[0]
        title = video.xpath('./@title')[0]
        videoId = p_vid.search(url).groups()[0]
        number = -1
        ret.append(buildResource(url,title,number,channelId,videoId))

    return ret


def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'ku6'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://v.ku6.com/playlist/index_6568865.html',1,1))
    pprint.pprint(handle('http://v.ku6.com/playlist/index_6564263.html',1,1))
