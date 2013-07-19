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
    url: http://fun.56.com
'''
def handle(url,channelId,tvNumber):
    tree = etree.HTML(get_html(url))
    videos = tree.xpath('//div[@class="bd mod56_video_list_H ent_list_H"]//div[@class="m_v_list_txt"]/h6/a')
        
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
    resource['type'] = 'video'
    resource['videoType'] = '56'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()
    

if __name__ == '__main__':
    pprint.pprint(handle('http://fun.56.com/znznv2/',100055,1))
    #pprint.pprint(handle('http://video.56.com/opera/6918.html',100055,1))
