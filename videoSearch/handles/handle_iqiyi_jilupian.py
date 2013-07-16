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

p_vids = [re.compile('"videoId":"([^"]+)"'),
         re.compile('videoid="([^"]+)"')]

p_number = re.compile('\[(\d+)\]')



def handle(url,channelId,tvNumber):
    tree = etree.HTML(getAllEpisode(url))
    videos = tree.xpath('//ul//li')
    print tvNumber
    if len(videos) == 0:
        return []
    
    ret = []
    for video in videos:
        url = video.xpath('./a/@href')[0]
        title = video.xpath('./a/img/@title')[0]
        number = int(p_number.search(video.xpath('./p/a/@title')[0]).groups()[0])
        
        if not number > tvNumber:
            return []
        print url
        videoId = None
        for p_vid in p_vids:
            try:
                videoId = p_vid.search(get_html(url)).groups()[0]
                break
            except:
                pass
        if videoId == None:
            continue
        ret.append(buildResource(url,title,number,channelId,videoId))
    return ret
    
def getAllEpisode(url):
    tree = etree.HTML(get_html(url))
    urls = tree.xpath('//div[@j-tab-cnt="pagelist"]//div[contains(@id,"j-album")]/text()')
    print urls
    ret = '<html>'
    for url in urls:
        url = 'http://www.iqiyi.com' + url
        ret += get_html(url)
    ret += '</html>'
    return ret


def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['type'] = 'video'
    resource['videoType'] = 'iqiyi'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()
    
if __name__ == '__main__':
    #pprint.pprint(handle('http://www.iqiyi.com/jilupian/jqgc.html',1,1))
    pprint.pprint(handle('http://www.iqiyi.com/dongman/mztkngyb.html',100249 ,1))

