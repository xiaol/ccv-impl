#coding=utf-8
import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re,pprint
from common.common import getCurTime
from pymongo import Connection
from common.Domain import Resource,Channel
from common.HttpUtil import get_html,getVideoIdByUrl
from setting import clct_channel


p_number = re.compile(u'/subject/play/\d+/(\d+)')

#=========================================================


def handle(url,channelId,tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//div[@class="p-content"]//ul/li/a')
    number = len(videoList)
    channel =  clct_channel.find_one({'channelId':channelId})
    channelType = channel['channelType']
    channelName = channel['channelName']
    
    
    ret = []
    for video in videoList:
        title =  channelName+ ' '+ video.xpath('./text()')[0]
        url = 'http://www.funshion.com' +video.xpath('./@href')[0]
        number = int(p_number.search(url).groups()[0])
        if number < tvNumber:
            continue
        videoId = getVideoIdByUrl(url)
        item = buildResource(url,title,number,channelId,videoId,channelType)
        ret.append(item)
    return ret
    



def buildResource(url,title,number,channelId,videoId,channelType):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['categoryId'] = channelType
    resource['type'] = 'video'
    resource['videoType'] = 'funshion'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()
    

if __name__ == '__main__':
    #pprint.pprint(handle('http://www.funshion.com/subject/107354',100550,3))
    #pprint.pprint(handle('http://www.funshion.com/subject/43280/',100550,700))
    pprint.pprint(handle('http://www.funshion.com/subject/107305/',100550,30))

