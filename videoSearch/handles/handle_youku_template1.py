#coding=utf-8
from lxml import etree
import re,pprint
from common.common import getCurTime
from pymongo import Connection
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel


p_vid = re.compile('id_([\w=]+?).html')
p_reload = re.compile("y\.episode\.show\('(\w+?)'\)")


def handle(url,channelId,tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//div[@class="collgrid6t"]//li[@class="v_title"]/a')
    ret = []
    
    for video in videoList:
        title = video.xpath('./@title')[0]
        url = video.xpath('./@href')[0]
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
    resource['videoType'] = 'youku'
    resource['videoId'] =  p_vid.search(url).groups()[0]
    resource['createTime'] = getCurTime()
    return resource.getInsertDict()
    

if __name__ == '__main__':
    pprint.pprint(handle('http://www.youku.com/show_page/id_z1e2a5fe0b6b511e1b16f.html',1))

