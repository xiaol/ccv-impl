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

p_vid = re.compile('vid:"([\w=]+?)",')

def handle(url,channelId,tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    month_urls = tree.xpath('//ul[@class="mod_tab_sub clearfix"]/li/a/@href')

    page_urls = []
    base_url = "http://v.qq.com"
    for url in month_urls:
        url = base_url+url
        page_urls.append(url)
        tree = etree.HTML(get_html(url))
        urls = [base_url+url for url in tree.xpath('//*[@id="pager"]/p/span[2]/a/@href')]
        page_urls.extend(urls)

    videoList = []
    for url in page_urls:
        tree = etree.HTML(get_html(url))
        videoList.extend(tree.xpath('//div[@class="mod_item_tit"]/h6/a'))

    ret = []
    for video in videoList:
        title = video.xpath('./@title')[0]
        url = video.xpath('./@href')[0]
        videoId = p_vid.search(get_html(url)).groups()[0]

        item = buildResource(url, title, channelId, videoId)
        ret.append(item)

    return ret

def buildResource(url, title, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'qq'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://v.qq.com/variety/column/column_1496.html',1,3))
