#coding=utf-8
import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from lxml import etree
import re,pprint,json
from common.common import getCurTime
from pymongo import Connection
from common.Domain import Resource,Channel
from common.HttpUtil import get_html,HttpUtil
from setting import TOKEN,APP_KEY
from setting import clct_channel


p_1 = re.compile('http://(.*?)/')
#p_iqiyi = re.compile('vid=(.*?)&')
p_youku = re.compile('/id_(.*?)\.html')
#p_tudou = re.compile('v/(.*?)/')
#p_sina = re.compile('vid=(.*?)/s\.swf')
p_56 = re.compile('/v_(.*?)\.html')
p_ku6 = re.compile('show/(.*?)\.')



def analysiseVideoTypeId(url):
    print url
    domain = p_1.search(url).groups()[0]
    if domain.find('youku') != -1:
        task = {'type':'youku'}
        task['videoId'] = p_youku.search(url).groups()[0]
    elif domain.find('ku6') != -1:
        task = {'type':'ku6'}
        task['videoId'] = p_ku6.search(url).groups()[0]
    elif domain.find('56') != -1:
        task = {'type':'56'}
        task['videoId'] = p_56.search(url).groups()[0]

    else:
        raise Exception('unsupport domain:' + domain)
    
    return task['type'],task['videoId']

def handle(url,channelId,tvNumber,page=1,count=20):
    html = get_html(url)
    html = "<html>" + json.loads(html)['data'] + "</html>"
    tree = etree.HTML(html)
    videos = tree.xpath('//div[@class="videoone clearfix"]')
    videoList  = []
    for video in  videos:
        try:
            url= 'http://www.jimu.tv' +video.xpath('.//a/@href')[0]
            tree = etree.HTML(get_html(url))
            videoUrl = tree.xpath('//div[@class="link"]/a/@href')[0]
            title = video.xpath('.//p[@class="title"]//a/text()')[0].strip()
            videoType, videoId = analysiseVideoTypeId(videoUrl)
            
            videoList.append(buildResource(videoUrl, title, channelId, videoType, videoId))
        except:
            continue
        

    return videoList




def buildResource(url,title,channelId,videoType,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['type'] = 'video'
    resource['videoType'] = videoType
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    resource['modifyTime'] = getCurTime()
    
    return resource.getInsertDict()
    

if __name__ == '__main__':
    pprint.pprint(handle('2214257545',int(13),1,100))

