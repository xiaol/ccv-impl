#coding=utf-8
import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re,pprint
from common.common import getCurTime
from common.Domain import Resource
from common.HttpUtil import get_html


p_vid = re.compile('id_([^\._]+)')
p_reload = re.compile("y\.episode\.show\('(\w+?)'\)")
p_number = re.compile(u'更新至(\d+)')
p_title = re.compile(r'\stitle=["\'](.*?)["\'][\s>]')

#=========================================================



def handle(url,channelId,tvNumber):
    html = get_html(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//div[@class="yk-row-index"]')[0]\
                    .xpath('.//div[@class="v-meta-title"]/a')

    ret = []
    for video in videoList:
        try:
            title = etree.tostring(video,encoding="utf-8",method="html").decode("utf-8")
            title = p_title.search(title)
            if title:
                title = title.groups()[0]
            else:
                title = video.xpath('./text()')[0]
            url = video.xpath('./@href')[0]
            videoId = p_vid.search(url).groups()[0]
            item = buildResource(url,title,-1,channelId,videoId)
            ret.append(item)
        except:
            continue

    return ret
    



def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'youku'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()
    

if __name__ == '__main__':
    #pprint.pprint(handle('http://www.youku.com/show_page/id_z3f6eb098940f11e196ac.html',1,3))
    pprint.pprint(handle('http://www.youku.com/',100527,3))

