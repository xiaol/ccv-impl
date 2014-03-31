#coding=utf-8
import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re,pprint
from common.common import getCurTime
from common.Domain import Resource,Channel
from common.HttpUtil import get_html,getVideoIdByUrl
from setting import clct_channel


def handle(url,channelId,tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//div[@id="playinfo-container"]/a')
    channelName = tree.xpath('//title/text()')[0]
    channelName = channelName.split()[0]

    p_number = re.compile(u'\d+')
    ret = []
    for video in videoList:
        title = channelName + ' ' + video.xpath('./text()')[0]
        url = 'http://www.funshion.com' + video.xpath('./@href')[0]
        number = int(p_number.search(title).group())
        if number <= tvNumber:
            continue
        print url
        videoId = getVideoIdByUrl(url)
        item = buildResource(url, title, number, channelId, videoId)
        ret.append(item)

    return ret
    

def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'funshion'
    resource['videoId'] = videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()
    

if __name__ == '__main__':
    #pprint.pprint(handle('http://www.funshion.com/subject/107354',100550,3))
    #pprint.pprint(handle('http://www.funshion.com/subject/43280/',100550,700))
    pprint.pprint(handle('http://www.funshion.com/subject/113675/',101759,0))

