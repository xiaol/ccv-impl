# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re, pprint
from common.common import getCurTime
from common.Domain import Resource,Channel
from common.HttpUtil import get_html, get_gzip_html
from setting import clct_channel


def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url, "gbk"))
    last_page_url = tree.xpath('//div[@class="page-nav"]/a[last()]/@href')[0]
    page_num = int(last_page_url.split('=')[-1])

    videos = tree.xpath('//div[@class="product-show"]/ul/li/div/a')
    for page in range(2, page_num+1):
        try:
            page_url = url + "?page=%d" %page
            tree = etree.HTML(get_html(url, "gbk"))
            videos.extend(tree.xpath('//div[@class="product-show"]/ul/li/div/a'))
        except Exception, e:
            print(page_url, e)
            continue

    ret = []
    for video in videos:
        url = video.xpath('./@href')[0]
        title = video.xpath('./@title')[0]
        vid = re.search(r'play_(\w+)\.html', url).groups()[0]

        ret.append(buildResource(url, title,  channelId, vid))

    return ret


# def handle(url, channelId, tvNumber):
#     html = get_gzip_html(url, "gbk")
#     tree = etree.HTML(html)
#     channels = tree.xpath('//div[@class="slide-list"]//div[@class="t"]/a')
#
#     ret = []
#     for channel in channels:
#         channel_url = "http://ipd.pps.tv/" + channel.xpath('./@href')[0]
#         for video in get_channel_video(channel_url):
#             ret.append(buildResource(video["url"], video["title"],  channelId, video["videoId"]))
#
#     return ret


def buildResource(url, title, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'pps'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://ipd.pps.tv/11381758', 100055, -1))

