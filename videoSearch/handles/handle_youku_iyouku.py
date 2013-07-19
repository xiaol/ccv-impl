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


p_vid = re.compile('id_([^\._]+)')

#=========================================================



def handle(url,channelId,tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//div[@class="YK_view"]//ul[@class="v"]/li[@class="v_link"]/a')
    
    ret = []
    for video in videoList:
        title = video.xpath('./@title')[0]
        url = video.xpath('./@href')[0]
        print title
        print url
        videoId = p_vid.search(url).groups()[0]
        item = buildResource(url,title,0,channelId,videoId)
        ret.append(item)
    return ret
    



def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'youku'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()
    

if __name__ == '__main__':
    #pprint.pprint(handle('http://www.youku.com/show_page/id_z3f6eb098940f11e196ac.html',1,3))
    pprint.pprint(handle('http://i.youku.com/u/UNTMxOTkwNjA0',100527,3))

