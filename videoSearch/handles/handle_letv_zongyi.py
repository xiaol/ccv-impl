# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

import re
import json
import pprint
import datetime
from lxml import etree
from common.common import getCurTime
from common.Domain import Resource
from common.HttpUtil import get_html


p_pid = re.compile(r'/zongyi/(\d+)\.html')

''' 默认只获取最新一年的视频 '''
def handle(url, channelId, tvNumber):
    if url.startswith("http://so.letv.com/variety/"):
        url = url.replace("so.letv.com/variety", "www.letv.com/zongyi")

    ret = []
    videos = []
    if p_pid.search(url):
        pid = p_pid.search(url).groups()[0]
        year = datetime.datetime.now().year
        info = json.loads(get_html("http://hot.vrs.letv.com/vlist?y=%d&f=1&p=1&pid=%s&b=1&s=50&o=2"\
                                   % (year, pid)))
        video_num = int(info["count"])
        if video_num > 50:
            info = json.loads(get_html("http://hot.vrs.letv.com/vlist?y=2013&f=1&p=1&pid=%s&b=1&s=%d&o=2"\
                                       % (pid, video_num)))
        videos = info["videoObject"]["videoInfo"]
    else:
        return ret

    for video in videos:
        url = video["url"]
        title = video["name"]
        videoId = video["vid"]
        number = video["releasedate"]
        ret.append(buildResource(url, title, number, channelId, videoId))

    return ret


def buildResource(url, title, number, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'letv'
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()



if __name__ == '__main__':
    # pprint.pprint(handle('http://www.letv.com/zongyi/52231.html',100055,-1))
    pprint.pprint(handle('http://so.letv.com/variety/95040.html',100055,-1))

