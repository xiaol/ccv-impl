# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re, pprint, json
from common.common import getCurTime
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel


p_vid = re.compile('sid\s*:\s*(\d+),')


def handle(url,channelId ,tvNumber):
    html = get_html(url, "gbk")
    sid = p_vid.search(html).groups()[0]
    data_url = "http://v.pps.tv/ugc/ajax/aj_newlongvideo.php?sid=%s&type=splay" % sid
    videos_data = json.loads(get_html(data_url))

    ret = []
    for video in videos_data['content'][0]:
        url = "http://v.pps.tv/play_%s.html" % video['url_key']
        title = video['d_echo']
        number = int(video['order'])
        if number <= tvNumber:
            continue
        videoId = video['url_key']

        ret.append(buildResource(url, title, number, channelId, videoId))

    '''检测完结'''
    if not re.search(u'更新至\d+', html):
        ret.append("over")

    return ret


def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['type'] = 'video'
    resource['videoType'] = 'pps'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()



if __name__ == '__main__':
    pprint.pprint(handle('http://v.pps.tv/splay_182661.html',100055,-1))

