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


p_content_vid = re.compile('vid\s*:\s*(\d+),')
p_number = re.compile('(\d+)')



def handle(url,channelId ,tvNumber):
    tree = etree.HTML(get_html(url))
    
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
        
        content = get_html(url)
        videoId = p_content_vid.search(content).groups()[0]
        
        ret.append(buildResource(url,title,number,channelId,videoId))
    return ret
    

def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['type'] = 'video'
    resource['videoType'] = 'letv'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()



if __name__ == '__main__':
    #pprint.pprint(handle('http://so.letv.com/tv/89951.html',100055,-1))
    #pprint.pprint(handle('http://tv.letv.com/zt/xlasd/index.shtml',100055,-1))
    #pprint.pprint(handle('http://tv.letv.com/zt/hxsxd/index.shtml',100055,-1))
    pprint.pprint(handle('http://tv.letv.com/zt/hxsxd/index.shtml',100055,-1))

