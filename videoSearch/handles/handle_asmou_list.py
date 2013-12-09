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

p_vid = re.compile(r'vid=([^&]+)&source=([^&]+)')

# 只爬取第一页的视频
def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url))
    base_url = "http://www.asmou.cn/"
    videos = tree.xpath('//div[@id="video_content"]//div[@class="subject"]/a')

    ret = []
    for video in videos:
        try:
            title = video.xpath('./span/text()')[0]
            url = base_url + video.xpath('./@href')[0]
            html = get_html(url)
            videoId, video_type= p_vid.search(html).groups()
            ret.append(buildResource(url, title, channelId, videoId, video_type))
        except Exception, e:
            print e
            continue

    return ret


def buildResource(url,title,channelId,videoId, video_type):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = video_type
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://www.asmou.cn/videolist-do-tag-id-277.html',100055,1))
    pprint.pprint(handle('http://www.asmou.cn/videolist-do-tag-id-90.html',100055,1))