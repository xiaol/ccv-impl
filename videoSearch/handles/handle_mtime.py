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

p_vid = re.compile('http://movie.mtime.com/\d+/trailer/(\d+).html')

def handle(url,channelId,tvNumber):
    tree = etree.HTML(get_html(url))
    links = tree.xpath('//a')
    ret = []
    for link in links:
        if not link.text:
            continue
        url = link.xpath('./@href')[0]
        if p_vid.search(url) != None:
            videoId = p_vid.search(url).groups()[0]
        else:
            continue
        title = link.xpath('./text()')[0]
        ret.append(buildResource(url,title,-1,channelId,videoId))
    return ret
    

def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['type'] = 'video'
    resource['videoType'] = 'mtime'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()
    
if __name__ == '__main__':
    pprint.pprint(handle('http://www.mtime.com/trailer/',100055))

