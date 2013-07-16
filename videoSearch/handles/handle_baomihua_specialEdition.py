#coding=utf-8
import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re,pprint
from common.common import getCurTime
from pymongo import Connection
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel

p_vid = re.compile('http://video.baomihua.com/[^/]+/(\d+)_p=\d+')


def handle(url,channelId,tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//div[@class="bd"]//li/div[@class="info"]//a')
    ret = []
    for video in videoList:
        url = video.xpath('./@href')[0]
        title = video.xpath('./text()')[0]
        print url
        print title
        item = buildResource(url,title,-1,channelId)
        ret.append(item)
    #pprint.pprint(videoList2) 
    return ret
    

def buildResource(url,title,hot,channelId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['hot'] = hot
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['type'] = 'video'
    resource['videoType'] = 'baomihua'
    resource['videoId'] =  p_vid.search(url).groups()[0]
    resource['createTime'] = getCurTime()
    return resource.getInsertDict()
    

if __name__ == '__main__':
    pprint.pprint(handle('http://app.baomihua.com/u/1772',100121,0))
