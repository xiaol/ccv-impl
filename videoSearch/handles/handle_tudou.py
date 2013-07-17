#coding=utf-8
from lxml import etree
import re,pprint
from common.common import getCurTime
from pymongo import Connection
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel

p_vid = re.compile('/([^/]+)\.html')
p_number = re.compile('(\d+)')
p_not_over = re.compile(u'更新至')

def handle(url,channelId,tvNumber, needNumber = True):
    tree = etree.HTML(get_html(url,'gbk'))
    videos = tree.xpath('//div[contains(@class,"playitems")]//h6[@class="caption"]/a')
    print tvNumber
    if not len(videos) > tvNumber:
        return []
    ret = []
    for video in videos:
        url = video.xpath('./@href')[0]
        title = video.xpath('./@title')[0]
        if needNumber:
            number = int(p_number.search(title).groups()[0])
            if number <= tvNumber:
                continue
        else:
            number = 0
        videoId = p_vid.search(url).groups()[0]
        ret.append(buildResource(url,title,number,channelId,videoId))

    '''检测完结'''
    try:
        if p_not_over.search(tree.xpath('//*[@id="title"]/span/text()')[0]):
            pass
        else:
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
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['type'] = 'video'
    resource['videoType'] = 'tudou'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()
    

if __name__ == '__main__':
    pprint.pprint(handle('http://www.tudou.com/albumplay/Lqfme5hSolM.html',1,1))

