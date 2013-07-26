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

p_vid = re.compile('data-player-videoid="(\w+?)"')


'''
    只抽取第一页
'''
def handle(url,channelId,tvNumber):
    tree = etree.HTML(get_html(url))
    videos = tree.xpath('//div[@class="list0"]//li//a[2]')
    ret = []
    for video in videos:
        try:
            url = video.xpath('./@href')[0]
            title = video.xpath('./text()')[0]
            videoId = p_vid.search(get_html(url)).groups()[0]
            print videoId
            ret.append(buildResource(url,title,channelId,videoId))
        except:
            print url
            continue

    return ret
    


def buildResource(url,title,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['type'] = 'video'
    resource['videoType'] = 'iqiyi'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()
    

if __name__ == '__main__':
    #pprint.pprint(handle('http://list.iqiyi.com/www/17/1688-1690-----------2-1-1-1---.html',100125))
    #pprint.pprint(handle('http://list.iqiyi.com/www/17/1673-1915-----------2-1-1-1---.html',100129))
    #pprint.pprint(handle('http://list.iqiyi.com/www/17/1673-1677-----------2-1-1-1---.html',100130))
    #pprint.pprint(handle('http://list.iqiyi.com/www/17/1673-1674-----------2-1-1-1---.html',100095))
    pprint.pprint(handle('http://list.iqiyi.com/www/17/1688-1690-----------2-1-1-1---.html', 100128, 1))

