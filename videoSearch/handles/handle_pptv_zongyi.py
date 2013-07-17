#coding=utf-8
import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re,pprint,json
from common.common import getCurTime
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel

p_number = re.compile('^(\d+)')
p_vid = re.compile('"vid":(\d+)')
p_channelId = re.compile('"channel_id":(\d+)')

def handle(url,channelId ,tvNumber):
    tree = etree.HTML(getAllEpisodes(url))
    
    links = tree.xpath('//ul/li/span/a')
    ret = []
    
    for link in links:
        url = link.xpath('./@href')[0]
        title = link.xpath('./text()')[0]
        number = p_number.search(title).groups()[0]
        if number <= tvNumber:
            continue
        
        content = get_html(url)
        videoId = p_vid.search(content).groups()[0]
        
        ret.append(buildResource(url,title,number,channelId,videoId))
    return ret
    

def getAllEpisodes(url):
    html = get_html(url)
    channelId = p_channelId.search(html).groups()[0]
    tree = etree.HTML(html)
    pages = tree.xpath('//p[@class="fr"]/a[not(@class) or @class="now"]/@data-page')
    
    ret = '<html>'
    for page in pages:
        url = 'http://api2.v.pptv.com/api/page/episodes.js?page=%s&channel_id=%s'%(page,channelId)
        print url
        ret += json.loads(get_html(url)[1:-2])['html']
    ret += '</html>'
    
    print ret
    return ret


def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'letv'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()



if __name__ == '__main__':
    #非诚勿扰
    pprint.pprint(handle('http://www.pptv.com/page/904.html',100055,-1))

