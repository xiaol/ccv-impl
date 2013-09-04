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


p_vid = [re.compile('vid-([^\.]+).html'),
         re.compile('v_([^\.]+).html'),
         ]

'''
    url: http://i.56.com/hexiangufu/videos/
'''
def handle(url, channelId, tvNumber):
    ivideo_url = re.findall(r'(http://i.56.com/\w+/videos/)', url)[0]
    html = get_html(url)
    tree = etree.HTML(html)
    page_num = tree.xpath('//div[@class="mod56_page_pn"]/span[@class="afont"]/text()')[0]
    page_num = int(re.findall(u'(\d+)页', page_num)[0])

    videos = tree.xpath('//ul[@class="m_v_list "]//h6/a[@class="m_v_list_title"]')
    for page in range(2, page_num+1):
        try:
            html = get_html(ivideo_url + 'p_%d/'%page)
            tree = etree.HTML(html)
            videos.extend(tree.xpath('//ul[@class="m_v_list "]//h6/a[@class="m_v_list_title"]'))
        except Exception, e:
            print(e, ivideo_url + 'p_%d/'%page)
            continue

    ret = []
    for video in videos:
        url = video.xpath('./@href')[0]
        title = video.xpath('./@title')[0]

        videoId = None
        for p in p_vid:
            try:
                videoId = p.search(url).groups()[0]
            except:
                print url
                continue
            break
        if videoId == None:
            continue
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
    pprint.pprint(handle('http://i.56.com/xiaochoucou/videos/',100055,1))
    pprint.pprint(handle('http://i.56.com/hexiangufu/videos/o_view.html',100055,1))
