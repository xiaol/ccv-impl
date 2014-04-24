#coding=utf-8
import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from lxml import etree
import re,pprint
from common.common import getCurTime
from common.Domain import Resource
from common.HttpUtil import get_html

p_vids = [re.compile('"videoId":"([^"]+)"'),
         re.compile('videoid="([^"]+)"')]
p_tvId = re.compile(r'tvId:\s+?(\d+)')
p_number = re.compile('(\d+)')


def handle(url,channelId,tvNumber):
    tree = etree.HTML(getAllEpisode(url))
    videos = tree.xpath('//li/p/a')
    print tvNumber
    print len(videos)
    ret = []
    for video in videos:
        url = video.xpath('./@href')[0]
        title = video.xpath('./text()')[0]
        if title.find(u'预告片') != -1:
            continue
        number = int(p_number.search(title).groups()[0])

        html = get_html(url)
        tvid = p_tvId.search(html).groups()[0]
        videoId = None
        for p_vid in p_vids:
            try:
                videoId = p_vid.search(html).groups()[0]
                videoId = tvid + '__' + videoId
                break
            except:
                pass
        if videoId == None:
            continue
        ret.append(buildResource(url,title,number,channelId,videoId))
    
    return ret


def getAllEpisode(url):
    content = get_html(url)
    tree = etree.HTML(content)
    urlList = tree.xpath('//div[@j-tab-cnt="pagelist"]//div[contains(@id,"j-album")]/text()')
    urlList = ['http://www.iqiyi.com'+ url for url in urlList]
    ret = '<html>'
    p = re.compile('#.*?$')
    for url in urlList:
        url = p.sub('',url)
        content  = get_html(url)
        ret += content
    return ret+ '</html>'


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
    #pprint.pprint(handle('http://www.iqiyi.com/dianshiju/mwdxn.html',100540,1))
    #pprint.pprint(handle('http://www.iqiyi.com/dianshiju/hxsxd.html',100540,1))
    #pprint.pprint(handle('http://www.iqiyi.com/a_19rrgi9xtd.html', 100540, 1))
    pprint.pprint(handle('http://www.iqiyi.com/a_19rrgi6x25.html', 100540, 1))

