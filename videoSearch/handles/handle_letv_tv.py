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


p_vid = re.compile('/(\d+)\.html')
p_number = re.compile('(\d+)')


def handle(url, channelId, tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    
    links = tree.xpath('//div[@class="gut"]/div/div[1]/div/dl/dd/p/a')
    if len(links) == 0:
        links = tree.xpath('//div[@class="listTAB" or @class="listTab"]//dl/dd/a')
    ret = []
    
    for link in links:
        url = link.xpath('./@href')[0]
        title = link.xpath('./text()')[0]
        number = int(p_number.search(title).groups()[0])
        if number <= tvNumber:
            continue
        
        videoId = p_vid.search(url).groups()[0]
        
        ret.append(buildResource(url,title,number,channelId,videoId))

    '''检测完结'''
    current_number = re.search(u'更新至(\d+)集', html)
    if not current_number:
        ret.append("over")

    return ret
    

def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'letv'
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()



if __name__ == '__main__':
    pprint.pprint(handle('http://www.letv.com/tv/73868.html',100055,-1))
    pprint.pprint(handle('http://www.letv.com/tv/93983.html',100055,-1))