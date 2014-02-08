#coding=utf-8
import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re,pprint
from common.common import getCurTime
from pymongo import Connection
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel,clct_resource


p_vid = re.compile('id_([\w=]+?).html')
p_reload = re.compile("y\.episode\.show\('(\w+?)'\)")
p_number = re.compile(u'更新至(\d+)')
p_title = re.compile(r'\stitle=["\'](.*?)["\'][\s>]')

#=========================================================



def handle(url,channelId,tvNumber):
    html = getAllEpisodes(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//div[@id="episode"]//ul/li[not(@class)]/a')

    treeOrigin = etree.HTML(get_html(url))
    numberList = p_number.search(treeOrigin.xpath('//div[@class="basenotice"]/text()')[0])
    if numberList:
        number = int(numberList.groups()[0])
    else:
        number = len(videoList)
    if number <= tvNumber:
        return []
    
    
    ret = []
    for video in videoList:
        title = etree.tostring(video,encoding="utf-8",method="html").decode("utf-8")
        title = p_title.search(title).groups()[0]
        if title.find(u"预告") >= 0:
            continue
        url = video.xpath('./@href')[0]
        videoId = p_vid.search(url).groups()[0]
        number = int(video.xpath('./text()')[0])
        if number <= tvNumber:
            continue
        item = buildResource(url,title,number,channelId,videoId)
        ret.append(item)
    return ret
    

def getAllEpisodes(url):
    html = get_html(url)
    matchs = p_reload.findall(html)
    if not matchs: 
        return html
    ans = '<html><div id="episode">'
    url = url.replace('show_page','show_episode')
    for match in matchs:
        #print match
        reload = match
        url_e = url + '?dt=json&divid=%s&__rt=1&__ro=r%s'%(reload,reload)
        print url_e
        html = get_html(url_e)
        ans += html
    ans += '</div></html>'
    #print ans
    return ans



def buildResource(url,title,number,channelId,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['number'] = number
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['type'] = 'video'
    resource['videoType'] = 'youku'
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    
    return resource.getInsertDict()
    

if __name__ == '__main__':
    #pprint.pprint(handle('http://www.youku.com/show_page/id_z3f6eb098940f11e196ac.html',1,3))
    pprint.pprint(handle('http://www.youku.com/show_page/id_z3a35da1c63ba11e3a705.html',100527,0))

