#coding=utf-8
import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from lxml import etree
import re,pprint
from common.common import getCurTime
from common.Domain import Resource
from common.HttpUtil import get_html

p_vid = re.compile('video[Ii]d["]{0,1}[:=]"([^"]+)"')
p_tvId = re.compile(r'tvId:(\d+)')
p_number = re.compile(u'第(\d+)集')
p_totalNumber = re.compile(u'共(\d+)集')


def handle(url,channelId,tvNumber):
    pageUrl = url
    tree = etree.HTML(getAllEpisode(url))
    videos = tree.xpath('//li')
    ret = []
    for video in videos:
        url = video.xpath('./a/@href')[0]
        title = video.xpath('./a/img/@title')[0]
        number = int(p_number.search(title).groups()[0])
        if number <= tvNumber:
            continue

        html = get_html(url)
        videoId = p_vid.search(html).groups()[0]
        tvid = p_tvId.search(html).groups()[0]
        videoId = tvid + '__' + videoId
        ret.append(buildResource(url,title,number,channelId,videoId))
    '''检测完结'''
    try:
        tree = etree.HTML(get_html(pageUrl))
        totalNumber = int(p_totalNumber.search(tree.xpath('//span[@class="upALL"]/text()')[0]).groups()[0])
        if len(videos) == totalNumber:
            ret.append('over')
    except:
        pass
    
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
    resource['type'] = 'video'
    resource['videoType'] = 'iqiyi'
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()
    
if __name__ == '__main__':
    pprint.pprint(handle('http://www.iqiyi.com/dongman/jjdjr.html',100252 ,1))
    #pprint.pprint(handle('http://www.iqiyi.com/dongman/mztkngyb.html',100252 ,1))

