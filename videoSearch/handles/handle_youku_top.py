# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import os
import sys
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

import re
import pprint
import json
from lxml import etree
from common.common import getCurTime
from common.Domain import Resource
from common.HttpUtil import get_html


p_vid = re.compile('id_(\w+).html')
p_title = re.compile(r'title="(.*?)" href=')

def handle(url, channelId, tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    videos = []
    url_type = 'link'
    if url.startswith('http://news.youku.com'):
        videos = tree.xpath('//div[@id="top10"]//div[@class="item"]/a')
    elif url.startswith('http://paike.youku.com'):
        videos = tree.xpath('//div[@id="m_90427"]//div[@class="item"]/a')
    elif url.startswith('http://sports.youku.com'):
        videos = tree.xpath('//div[@id="m_91301"]//div[@class="v-meta-title"]/a')
    elif url.startswith('http://ent.youku.com'):
        videos = tree.xpath('//div[@id="m_88719"]//div[@class="v-meta-title"]/a')
    elif url.startswith('http://game.youku.com'):
        videos = tree.xpath('//div[@id="m_93403"]//div[@class="v-meta-title"]/a')
    elif url.startswith('http://fun.youku.com'):
        videos.extend(json.loads(get_html('http://vq.youku.com/video/AppTop.json?cate=94&listtype=1&pl=6&period=day'))['data'])
        videos.extend(json.loads(get_html('http://vq.youku.com/video/AppTop.json?cate=94&listtype=1&pl=6&period=week'))['data'])
        videos.extend(json.loads(get_html('http://vq.youku.com/video/AppTop.json?cate=94&listtype=1&pl=6&period=month'))['data'])
        url_type = 'json'
    elif url.startswith('http://travel.youku.com/food'):
        videos = tree.xpath('//div[@id="m_90985"]//div[@class="v-meta-title"]/a')
    elif url.startswith('http://travel.youku.com/gossip'):
        videos = tree.xpath('//div[@id="m_90994"]//div[@class="v-meta-title"]/a')
    elif url.startswith('http://fashion.youku.com'):
        videos = tree.xpath('//div[@id="m_88840"]//div[@class="v-meta-title"]/a')
    elif url.startswith('http://index.youku.com/protop'):
        videos = tree.xpath('//div[@class="rankall"]//tr/td/a')
        url_type = 'js'

    ret = []
    if url_type == 'link':
        urls = {}
        for video in videos:
            title = video.xpath('./text()')[0]
            url = video.xpath('./@href')[0]
            if urls.get(url, None) or not url.startswith("http://v.youku.com/v_show/id_"):
                continue
            urls[url] = 1
            video_id = p_vid.search(url).groups()[0]
            item = buildResource(url, title, video_id, channelId)
            ret.append(item)
    elif url_type == 'json':
        for video in videos:
            title = video['title']
            url = video['playUrl']
            video_id = p_vid.search(url).groups()[0]
            item = buildResource(url, title, video_id, channelId)
            ret.append(item)
    elif url_type == 'js':
        p_url = re.compile(r'http://v.youku.com/v_show/id_[\w=]+')
        for video in videos:
            title = video.xpath('./text()')[0]
            url = p_url.search(video.xpath('./@onclick')[0]).group() + '.html'
            video_id = p_vid.search(url).groups()[0]
            item = buildResource(url, title, video_id, channelId)
            ret.append(item)

    return ret


def buildResource(url, title, videoId, channelId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'youku'
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    # pprint.pprint(handle('http://news.youku.com/', 10000, 1))
    # pprint.pprint(handle('http://paike.youku.com/',10000, 1))
    # pprint.pprint(handle('http://sports.youku.com/',10000, 1))
    # pprint.pprint(handle('http://ent.youku.com/',10000, 1))
    # pprint.pprint(handle('http://game.youku.com/index/jiaodian',10000, 1))
    # pprint.pprint(handle('http://fun.youku.com/',10000, 1))
    # pprint.pprint(handle('http://travel.youku.com/food/',10000, 1))
    # pprint.pprint(handle('http://travel.youku.com/gossip/',10000, 1))
    pprint.pprint(handle('http://fashion.youku.com/',10000, 1))
    pprint.pprint(handle('http://index.youku.com/protop/5',10000, 1))
    pprint.pprint(handle('http://index.youku.com/protop/6',10000, 1))



