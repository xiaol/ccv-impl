# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from lxml import etree
import re, pprint, json
from common.common import getCurTime
from common.Domain import Resource,Channel
from common.HttpUtil import get_html, get_gzip_html
from setting import clct_channel

p_vid = re.compile('(\d+)\.html')
p_gameid = re.compile(r"gameid\s*=\s*'(\d+)';")

def handle(url, channelId, tvNumber):
    html = get_gzip_html(url)
    #tree = etree.HTML(html)
    #page_number = int(tree.xpath('//*[@id="game_page"]/ul/li[@class="spe"]/span/text()')[0])
    game_id = p_gameid.search(html).groups()[0]

    #默认获取前50个视频
    page_size = 50
    info_url = "http://www.aipai.com/app/www/apps/gameAreaInfo.php?" + \
                'data={"gameid":%s,"page":1,"pageSize":%d}' %(game_id, page_size)
    json_data = get_html(info_url)
    begin = json_data.find('(')+1
    end = json_data.rfind(')')
    data_list = json.loads(json_data[begin:end])['data']
    videos = []
    for data in data_list:
        for item in data:
            videos.append(item['work'])
    ret = []
    for video in videos:
        try:
            title = video['title']
            url = video['url']
            videoId = url
            ret.append(buildResource(url, title, channelId, videoId))
        except Exception, e:
            print e
            continue

    return ret


def buildResource(url,title,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'aipai_url'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    # pprint.pprint(handle('http://vsa.aipai.com/',100055,1))
    pprint.pprint(handle('http://www.aipai.com/game_gameid-16391.html',100055,1))
