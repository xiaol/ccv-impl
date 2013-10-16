# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re
import json
import pprint
from common.common import getCurTime
from common.Domain import Resource,Channel
from common.HttpUtil import get_html


def handle(url, channelId, tvNumber):
    html = get_html(url, 'gbk')

    album_id = re.search(r'/(\w+)\.html', url).groups()[0]
    album_data = json.loads(get_html("http://www.tudou.com/albumcover/albumdata/getAlbumItems.html?acode=%s&charset=utf-8"\
                        % album_id))
    item_num = album_data['itemNum']
    if item_num < tvNumber:
        return []

    p_vid = re.compile('/([^/]+)\.html')
    videos = album_data["items"]
    ret = []
    for video in videos:
        try:
            url = video["itemPlayUrl"]
            title = video["title"]
            number = video["episode"]
            if number <= tvNumber:
                continue
            videoId = p_vid.search(url).groups()[0]
            ret.append(buildResource(url, title, number, channelId, videoId))
        except Exception, e:
            print(video, e)

    '''检测完结'''
    total_num = re.search(u"update:\s*['\"]全(\d+)", html)
    if total_num:
        ret.append('over')

    return ret


def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'tudou'
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    # pprint.pprint(handle('http://www.tudou.com/albumcover/_nJJMEa6O6I.html',1,1))
    pprint.pprint(handle('http://www.tudou.com/albumcover/92J2xqpSxWY.html',1,1))
