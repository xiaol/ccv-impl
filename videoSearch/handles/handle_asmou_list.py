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


def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url))
    last_page = tree.xpath('//div[@class="page"]/a[last()]/@href')[0]
    base_url = "http://www.asmou.cn/"
    page_num = re.search(r'-(\d+)\.html$', last_page).groups()[0]
    page_url_prefix = last_page[0:last_page.find(page_num+".html")]
    total = int(tree.xpath('//div[@class="page"]/em/text()')[0])
    page_num = int((total+12-1)/12)

    videos = tree.xpath('//div[@id="video_content"]//div[@class="subject"]/a')
    #除第一页外剩下的页面地址
    for num in range(2, int(page_num)+1):
        try:
            page_url = base_url+ page_url_prefix + str(num) + ".html"
            tree = etree.HTML(get_html(page_url))
            videos.extend(tree.xpath('//div[@id="video_content"]//div[@class="subject"]/a'))
        except Exception, e:
            print(page_url, e)
            continue

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