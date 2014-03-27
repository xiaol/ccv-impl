#coding=utf-8
import os, sys

sys.path += [os.path.dirname(os.path.dirname(__file__))]

import urllib
import time
import re, pprint, json
from lxml import etree
from common.common import getCurTime
from common.Domain import Resource
from common.HttpUtil import get_html


p_vid = re.compile('videoid="([^"]+)"')


def handle(url, channelId, tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    album_name = tree.xpath('//meta[@name="irAlbumName"]/@content')
    if album_name:
        album_name = album_name[0].encode('utf-8')
        album_name = urllib.quote(album_name).replace('%', '_')
        year = time.ctime().split()[-1] + '_20'
        url = 'http://search.video.iqiyi.com/searchDateAlbum/?source=%s&date=%s&sortKey=6&cur=1&limit=300&cb=newtopic' \
              % (album_name, year)
        data_str = get_html(url)
        left = data_str.find('{')
        data = json.loads(data_str[left:])['data']['list']
        ret = []
        for video in data:
            url = video['TvApplication.purl']
            title = video['VrsVideoTv.tvName']
            number = video['VrsVideotv.tvYear']
            videoId = video['vid']
            if number <= tvNumber:
                continue
            item = buildResource(url, title, number, channelId, videoId)
            ret.append(item)
        return ret

    else:
        data = getAlbumInfo(url)
        ret = []
        for video in data:
            print video
            url = video['vUrl']
            title = video['aName']
            number = video['tvYear']
            videoId = video['vid']
            print('number:', number, 'tvNumber:', tvNumber)
            if number <= tvNumber:
                continue
            item = buildResource(url, title, number, channelId, videoId)
            ret.append(item)
        return ret


def getAlbumInfo(url):
    html = get_html(url)
    p_albumId = re.compile('"id":(\d+)[,}]')

    albumId = p_albumId.search(html)
    if not albumId:
        p_albumId = re.compile('data-player-albumid="(\d+)"')
        albumId = p_albumId.search(html)

    if not albumId:
        return []
    else:
        albumId = albumId.groups()[0]

    print 'albumId', albumId
    #获取最新一年
    url_yearMonthList = 'http://cache.video.qiyi.com/sdlst/6/%s/?cb=scDtListC' % albumId
    print url_yearMonthList
    data = json.loads(get_html(url_yearMonthList)[14:])
    year = sorted(data['data'].keys(), reverse=True)[0]
    print year
    url_videoList = 'http://cache.video.qiyi.com/sdvlst/6/%s/%s/' % (albumId, year)
    data = get_html(url_videoList)
    return json.loads(data[16:])['data']


def buildResource(url, title, number, channelId, videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['number'] = number
    resource['type'] = 'video'
    resource['videoType'] = 'iqiyi'
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    # pprint.pprint(handle('http://www.iqiyi.com/zongyi/fcwr.html',100649,3))
    # pprint.pprint(handle('http://www.iqiyi.com/zongyi/kldby.html', 100649, 3))
    # pprint.pprint(handle('http://www.iqiyi.com/zongyi/bbdkx.html', 100649, 3))
    # pprint.pprint(handle('http://www.iqiyi.com/zongyi/zydzb.html', 100649, 3))
    pprint.pprint(handle('http://www.iqiyi.com/v_19rrh46nb4.html', 100649, 3))
