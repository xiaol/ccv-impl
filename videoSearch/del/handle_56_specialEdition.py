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


p_vid = [re.compile('vid-([^\.]+).html'),
         re.compile('v_([^\.]+).html'),
         ]

'''
    url: http://ent.56.com/gossip/
'''
def handle(url,channelId,tvNumber):
    tree = etree.HTML(get_html(url))
    videos = tree.xpath('//div[@class="video_list"]//dt/a')
    ret = []
    for video in videos:
        url = video.xpath('./@href')[0]
        title = video.xpath('./text()')[0]
        print url
        print title
        videoId = None
        for p in p_vid:
            try:
                videoId = p.search(url).groups()[0]
                print 1
            except:
                print url
                continue
            break
        if videoId == None:
            continue
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
	pprint.pprint(handle('http://www.56.com/w17/album-aid-11549180.html',100122,1))
