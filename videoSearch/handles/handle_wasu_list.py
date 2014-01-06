# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import os,sys,re
sys.path += [os.path.dirname(os.path.dirname(__file__))]
import pprint
from lxml import etree
from common.common import getCurTime
from common.Domain import Resource
from common.HttpUtil import get_html


p_number = re.compile('_(\d+)_')

def handle(url, channelId, tvNumber):
    videos = []
    if url.startswith('http://www.wasu.cn/Column/show'):
        videos = getZongYi(url)
    else:
        html = get_html(url)
        tree = etree.HTML(html)
        videos = tree.xpath('//div[@id="publish"]/dl/dd/p[1]/a[1]')

    ret = []
    for video in videos:
        url = video.xpath('./@href')[0]
        title = video.xpath('./@title')[0]
        try:
            number = p_number.search(title).groups()[0]
        except:
            number = None

        item = buildResource(url, title, channelId, url,number)
        ret.append(item)

    return ret


def getZongYi(url):
    html = get_html(url)
    tree = etree.HTML(html)
    page_num = tree.xpath('//div[@class="item_page right"]/a[not(@class)]')
    videos = tree.xpath('//div[contains(@class, "relevance_video")]//p[@class="pt13 lvjz"]/a')
    if page_num:
        page_num = int(page_num[-1].xpath('./text()')[0])
        for page in range(2, page_num+1):
            try:
                html = get_html(url + '?&p=%d' % page)
                tree = etree.HTML(html)
                videos.extend(tree.xpath('//div[contains(@class, "relevance_video")]//p[@class="pt13 lvjz"]/a'))
            except:
                pass

    return videos


def buildResource(url, title, channelId, videoId, number = None):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'wasu'
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()
    if number!= None:resource['number'] = number

    return resource.getInsertDict()


if __name__ == '__main__':
    # pprint.pprint(handle('http://www.wasu.cn/list/index/cid/6', 100649, 3))
    # pprint.pprint(handle('http://all.wasu.cn/index/cid/91', 100649, 3))
    pprint.pprint(handle('http://www.wasu.cn/Column/show/column/1788388', 100649, 3))

