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

    DateMonths = []
    date = json_data["date"]
    for year in date:
        if year.startswith('y'):
            year_num = year.lstrip('y')
            for month in date[year]:
                DateMonths.append(year_num + '-' + month)

    DateMonths.sort(key=lambda x: x.split('-'))


    videos = []
    for sortDateM in DateMonths:
        try:
            json_data = json.loads(get_html("http://z.56.com/api/getContentListByTid.php?tid=%s&sortDateM=%s" \
                                            %(town_id, sortDateM)))
            total = json_data["total"]
            json_data = json.loads(get_html("http://z.56.com/api/getContentListByTid.php?tid=%s&sortDateM=%s&page=1&pageSize=%s" \
                                        %(town_id, sortDateM, total)))
            videos.extend(json_data["data"])
        except Exception, e:
            print(e, sortDateM)

    ret = []
    for video in videos:
        try:
            url = "http://z.56.com/c_%s/" %video["id"]
            title = video["dataInfo"]["Subject"]
            videoId = video["data_id"]
            ret.append(buildResource(url, title, channelId, videoId))
        except Exception, e:
            print(e, url)

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

