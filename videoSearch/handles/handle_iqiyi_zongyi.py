#coding=utf-8
import os,sys
sys.path += [os.path.dirname(os.path.dirname(__file__))]
from lxml import etree
import re,pprint,json
from common.common import getCurTime
from pymongo import Connection
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel

p_vid = re.compile('"videoId":"([^"]+)"')
p_vid = re.compile('videoid="([^"]+)"')

p_albumId = re.compile('"id":(\d+)[,}]')

def get_group(p,s):
    return p.search(s).groups()[0]

def handle(url,channelId,tvNumber):
    data = getAlbumInfo(url)
    ret = []
    for video in data:
        print video
        url =video['vUrl']
        title = video['aName']
        number = video['tvYear']
        videoId = video['vid']
        print('number:',number,'tvNumber:',tvNumber)
        if number <= tvNumber:
            continue
        item = buildResource(url,title,number,channelId,videoId)
        ret.append(item)
        
    return ret
    


def getAlbumInfo(url):
    html = get_html(url)
    albumId = get_group(p_albumId,html)
    #获取最新一年
    url_yearMonthList = 'http://cache.video.qiyi.com/sdlst/6/%s/?cb=scDtListC' % albumId
    data  = json.loads(get_html(url_yearMonthList)[14:])
    year =  sorted(data['data'].keys(),reverse=True)[0]
    print year
    url_videoList = 'http://cache.video.qiyi.com/sdvlst/6/%s/%s/' % (albumId, year)
    data = get_html(url_videoList)
    return json.loads(data[16:])['data']

def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['number'] = number
    resource['type'] = 'video'
    resource['videoType'] = 'iqiyi'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()
    

if __name__ == '__main__':
    pprint.pprint(handle('http://www.iqiyi.com/zongyi/fcwr.html',100649,3))

