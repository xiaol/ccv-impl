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

p_vid = re.compile('id_([\w=]+?).html')
p_page_num = re.compile(r'(\d+).html')
p_title = re.compile(r'\stitle=["\'](.*?)["\'][\s>]')

def handle(url,channelId,tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    last_page_url = tree.xpath(u'//div[@class="page f_r"]/a[@title="末页"]/@href')
    videoList = tree.xpath('//div[@class="items"]/ul/li[@class="v_title"]/a')
    if last_page_url:
        last_page_url = last_page_url[0]
        last_page_num = int(p_page_num.search(last_page_url).groups()[0])
        for page_num in range(2, last_page_num+1):
            page_url = p_page_num.sub(str(page_num)+".html", last_page_url)
            tree = etree.HTML(get_html(page_url))
            videoList.extend(tree.xpath('//div[@class="items"]/ul/li[@class="v_title"]/a'))

    ret = []
    for video in videoList:
        title = etree.tostring(video,encoding="utf-8",method="html").decode("utf-8")
        title = p_title.search(title)
        if title:
            title = title.groups()[0]
        else:
            title = video.xpath('./@title')[0]
        url = video.xpath('./@href')[0]
        videoId = p_vid.search(url).groups()[0]

        item = buildResource(url, title, channelId, videoId)
        ret.append(item)

    return ret

def buildResource(url, title, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'youku'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    #pprint.pprint(handle('http://www.youku.com/playlist_show/id_19416824.html',1,3))
    pprint.pprint(handle('http://www.youku.com/playlist_show/id_18600811.html',1,3))
