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


def handle(url, channelId, tvNumber):
    html = get_html(url, 'gbk')
    tree = etree.HTML(html)
    videos = tree.xpath('//*[@id="list1"]//td[@class="u-ctitle"]')

    ret = []
    max_number = 0
    for video in videos:
        try:
            number = int(re.search(r'\d+', video.xpath('./text()')[0]).group())
            if number <= tvNumber:
                continue
            if number > max_number: max_number = number
            url = video.xpath('./a/@href')[0]
            title = video.xpath('./a/text()')[0]

            # ids = re.search(r'/([^/]+)/([^/]+)/([^/]+)\.html', url).groups()
            # videoId = 'movie/' + ids[0] + '/' + ids[1] + '/2_' + ids[2]
            ret.append(buildResource(url, title, number, channelId))
        except Exception, e:
            print(e)

    '''检测完结'''
    try:
        total_num = int(re.search(u"本课程共(\d+)集", html).groups()[0])
        if max_number >= total_num:
            ret.append('over')
    except:
        pass

    return ret


def buildResource(url,title, number, channelId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'netease'
    resource['videoId'] = url
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://v.163.com/special/opencourse/form.html',100055,1))
    pprint.pprint(handle('http://v.163.com/special/cuvocw/xifangjingdianjuzuo.html',100055,1))