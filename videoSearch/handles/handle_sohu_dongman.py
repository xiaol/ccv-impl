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

p_vid = re.compile('/([^/]+)\.shtml')
p_number = re.compile('(\d+)')
p_totalNumber = re.compile(u'共(\d+)集')


def handle(url,channelId,tvNumber):
    tree = etree.HTML(get_html(url,'gbk'))
    videos = tree.xpath('//div[@id="list_desc"]//li//strong/a')
    print tvNumber
    if not len(videos) > tvNumber:
        return []
    ret = []
    for video in videos:
        url = video.xpath('./@href')[0]
        title = video.xpath('./text()')[0]
        try:
            number = int(p_number.search(title).groups()[0])
            if number <= tvNumber:
                continue
        except:
            pass
        

        videoId = p_vid.search(url).groups()[0]
        ret.append(buildResource(url,title,number,channelId,videoId))

    '''检测完结'''
    try:
        totalNumber = int(p_totalNumber.search(tree.xpath('//div[@class="d1 clear"]/div[1]/text()')[0]).groups()[0])
        if len(videos) == totalNumber:
            ret.append('over')
    except:
        pass

    return ret

def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'sohu_url'
    resource['videoId'] =  url
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()
    


if __name__ == '__main__':
    #pprint.pprint(handle('http://so.letv.com/tv/89951.html',100055,-1))
    #pprint.pprint(handle('http://tv.sohu.com/s2013/sdsxsomg/',100055,-1))
    pprint.pprint(handle('http://tv.sohu.com/s2011/6358/s329815619/',100055,-1))