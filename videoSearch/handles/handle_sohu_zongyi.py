# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import os,sys
sys.path += [os.path.dirname(os.path.dirname(__file__))]
from lxml import etree
import re,pprint,json
from common.common import getCurTime
from pymongo import Connection
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel

p_playlistid = re.compile(r'PLAYLIST_ID="(\d+)"')


def handle(url,channelId,tvNumber):
    data = getAlbumInfo(url)
    ret = []
    for video in data:
        print video
        url =video['pageUrl']
        title = video['name']
        number = video['order']
        videoId = video['vid']
        print('number:',number,'tvNumber:',tvNumber)
        if number <= tvNumber:
            continue
        item = buildResource(url,title,number,channelId,videoId)
        ret.append(item)

    return ret

def getAlbumInfo(url):
    html = get_html(url,'gbk')
    tree = etree.HTML(html)
    year = tree.xpath('//*[@id="zy_y"]/li/a[@class="current"]/text()')[0]
    print year
    playlistid = p_playlistid.search(html).groups()[0]
    #获取最新一年
    url_yearList = 'http://hot.vrs.sohu.com/pl/videolist?playlistid=%s&year=%s' %(playlistid, year)
    print url_yearList
    data  = json.loads(get_html(url_yearList,'gbk'))
    url_videoList = data["videos"]
    return url_videoList

def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['number'] = number
    resource['type'] = 'video'
    resource['videoType'] = 'sohu_url'
    resource['videoId'] =  url
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    #pprint.pprint(handle('http://tv.sohu.com/jsfcwr/',100649,3))
    #pprint.pprint(handle('http://tv.sohu.com/wmyhbj/',100649,3))
    pprint.pprint(handle('http://tv.sohu.com/s2014/ellen/',100649,0))

