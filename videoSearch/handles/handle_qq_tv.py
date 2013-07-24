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

p_vid = re.compile('/([^/]+)\.html')
p_number = re.compile(u'第(\d+)集')
p_isover = re.compile(u'剧集：全(\d+)集')
xpaths = ['//*[@id="mod_video_content"]/div/ul/li/p']

def handle(url,channelId,tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    videos = []
    for xpath_str in xpaths:
        videos = tree.xpath(xpath_str)
        if len(videos) > 0:
            break

    ret = []
    base_url = "http://v.qq.com"
    for video in videos:
        title = video.xpath('./a/@title')[0]
        number = int(p_number.search(title).groups()[0])
        if number <= tvNumber:
            continue
        url = base_url + video.xpath('./a/@href')[0]
        subtitle = video.xpath('./span/text()')
        if subtitle:
            title += " " + subtitle[0]
        videoId = p_vid.search(url).groups()[0]

        item = buildResource(url, title, number, channelId, videoId)
        ret.append(item)

    '''检测完结'''
    if p_isover.search(html):
        ret.append("over")

    return ret

def buildResource(url, title, number, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'qq'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://v.qq.com/detail/x/xgnnne5is86cqh2.html',1,0))
    pprint.pprint(handle('http://v.qq.com/detail/t/t7748cv5nzh74l6.html',1,0))

