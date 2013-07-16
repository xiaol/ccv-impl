# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from lxml import etree
import re,pprint, json
from common.common import getCurTime
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel

p_aid = re.compile(r'aid-(\d+).html')
p_vid = re.compile('vid-([^\.]+).html')

def getAlbumData(url):
    #从js代码里里查到的
    aid = int(p_aid.search(url).groups()[0])
    cid = aid%89+11
    data_url = "http://www.56.com/w%d/album_v3/album_videolist_2012.phtml?page=0&row=20&aid=%d" %(cid, aid)
    result  = json.loads(get_html(data_url))
    total = result["total"]

    if total>20:
        data_url = "http://www.56.com/w%d/album_v3/album_videolist_2012.phtml?page=0&row=%d&aid=%d"\
                   %(cid, total, aid)
        result = json.loads(get_html(data_url))

    data = []
    for item in result["data"]:
        url = "http://www.56.com/w%d/play_album-aid-%d_vid-%s.html" %(cid, aid, item["video_id"])
        data.append({"url":url, "title":item["video_title"], "vid":item["video_id"]})

    return data

def handle(url,channelId,tvNumber):
    #html = get_html(url)
    #tree = etree.HTML(html)
    ret = []
    data = getAlbumData(url)
    for item in data:
        url = item["url"]
        title = item["title"]
        videoId = item["vid"]
        ret.append(buildResource(url,title,channelId,videoId))

    return ret


def buildResource(url,title,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['type'] = 'video'
    resource['videoType'] = '56'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://www.56.com/w75/album-aid-11150251.html',100055,1))
    pprint.pprint(handle('http://www.56.com/w79/album-aid-9875241.html',100055,1))
