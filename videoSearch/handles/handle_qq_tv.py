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

p_vid = re.compile('/([^/]+)\.html')
p_number = re.compile(u'(\d+)集')
p_isover = re.compile(u'剧集：全\d+集')
p_update = re.compile(u'更新至\d+集')
p_data_url = re.compile('src=[\'"](http://v.qq.com/c/[^/]+\.js).+Math.random()')


'''
    qq tv有两种页面，格式、编码都不一样，这里分开处理
'''
def handle(url, channelId, tvNumber):
    ret = []
    base_url = "http://v.qq.com"

    if url.find("/zt/detail/") != -1:
        html = get_html(url, "gbk")
        try:
            data_url = p_data_url.search(html).groups()[0]
            data = get_html(data_url)
            begin = data.find('{')
            end = data.rfind('}')
            json_str = data[begin:end+1]
            data = json.loads(json_str)
            video_list = data['vidlist']
        except:
            return []

        for index, video in enumerate(video_list):
            url = base_url+ video["playUrl"]
            title = video["title"]
            videoId = video["vid"]
            number = index+1
            if title.find(u"预告") != -1:
                continue

            item = buildResource(url, title, number, channelId, videoId)
            ret.append(item)

        '''检测完结'''
        if not p_update.search(html):
            ret.append("over")
    elif url.find("/p/tv/") != -1:
        html = get_html(url)
        tree = etree.HTML(html)
        videos = tree.xpath('//div[@class="mod_video_fragments"]//ul/li/strong/a')

        for video in videos:
            title = video.xpath('./@title')[0]
            if title.find(u"预告") != -1:
                continue
            number = int(p_number.search(title).groups()[0])
            if number <= tvNumber:
                continue
            url = base_url + video.xpath('./@href')[0]
            videoId = p_vid.search(url).groups()[0]

            item = buildResource(url, title, number, channelId, videoId)
            ret.append(item)

        '''检测完结'''
        total = int(tree.xpath('//span[@class="episodes_sum"]/em/text()')[0])
        current = int(tree.xpath('//span[@class="episodes_current"]/em/a/text()')[0])
        if not current < total:
            ret.append("over")
    else:
        html = get_html(url)
        tree = etree.HTML(html)
        sourceId = tree.xpath('//div[@sourceid]/@sourceid')[0]
        loadplaylistUrl = 'http://s.video.qq.com/loadplaylist?vkey=%s&vtype=2&otype=json&callback=1'%sourceId
        print loadplaylistUrl
        videos = json.loads(get_html(loadplaylistUrl)[2:-1])
        print videos
        videos = videos['video_play_list']['playlist']

        for video in videos:
            title = video['title']
            if title.find(u"预告") != -1:
                continue
            number = int(video['episode_number'])
            if number <= tvNumber:
                continue
            url = video['url']
            videoId = p_vid.search(url).groups()[0]
            item = buildResource(url, title, number, channelId, videoId)
            ret.append(item)

        '''检测完结'''
        if p_isover.search(html):
            ret.append("over")

    return ret

def buildResource(url, title, number, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'qq'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    # pprint.pprint(handle('http://v.qq.com/detail/x/xgnnne5is86cqh2.html',1,0))
    # pprint.pprint(handle('http://v.qq.com/detail/t/t7748cv5nzh74l6.html',1,0))
    # pprint.pprint(handle('http://v.qq.com/detail/n/nndopnljjrwnwck.html',1,0))
    # pprint.pprint(handle('http://v.qq.com/zt/detail/hml/index.html',1,0))
    # pprint.pprint(handle('http://v.qq.com/zt/detail/index.html',1,0))
    #pprint.pprint(handle('http://v.qq.com/p/tv/zt/lama/index.html',1,0))
    #pprint.pprint(handle('http://v.qq.com/detail/f/fgcbe05ey1wfc7k.html',1,0))
    pprint.pprint(handle('http://v.qq.com/p/tv/detail/zonglihewo/index.html',1,0))