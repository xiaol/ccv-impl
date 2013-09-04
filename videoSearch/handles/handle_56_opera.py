# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from lxml import etree
import re, pprint, json
from common.common import getCurTime
from common.Domain import Resource, Channel
from common.HttpUtil import get_html
from setting import clct_channel


'''
    url: http://video.56.com/opera/20556.html
'''
def handle(url, channelId, tvNumber):
    mid = re.search(r'/(\d+)\.html', url).groups()[0]
    json_data = json.loads(get_html("http://video.56.com/index.php?Controller=Opera&Action=GetOpera&mid=%s" %mid))
    videos = json_data["data"]
    ret = []
    for video in videos:
        url = video["url"]
        title = video["title"]
        videoId = video["vid"]
        ret.append(buildResource(url, title, channelId, videoId))

    return ret


def buildResource(url,title,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = '56'
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://video.56.com/opera/20556.html',100055,1))
    pprint.pprint(handle('http://video.56.com/opera/6492.html',100055,1))
