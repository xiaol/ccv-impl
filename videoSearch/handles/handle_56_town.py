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


'''
    url: http://z.56.com/1331503622236203/
'''
def handle(url, channelId, tvNumber):
    html = get_html(url)
    town_id = re.search(r'tid\s*=\s*(\d+);', html).groups()[0]

    json_data = json.loads(get_html("http://z.56.com/api/getContentListByTid.php?tid=%s" %town_id))
    total = json_data["total"]
    json_data = json.loads(get_html("http://z.56.com/api/getContentListByTid.php?tid=%s&page=1&pageSize=%s"\
                                    %(town_id, total)))
    videos = json_data["data"]

    ret = []
    for video in videos:
        try:
            url = "http://z.56.com/c_%s/" %video["id"]
            title = video["dataInfo"]["Subject"]
            videoId = video["data_id"]
            ret.append(buildResource(url, title, channelId, videoId))
        except Exception, e:
            print(e, url)
            continue

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
    pprint.pprint(handle('http://z.56.com/1331503622236203/',100055,1))

