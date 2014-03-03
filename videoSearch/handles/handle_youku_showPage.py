#coding=utf-8
import os,sys
sys.path += [os.path.dirname(os.path.dirname(__file__))]

from lxml import etree
import re,pprint
from common.common import getCurTime
from pymongo import Connection
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel

p_vid = re.compile('id_([\w=]+?).html')
p_reload = re.compile("y\.episode\.show\('(\w+?)'\)")
p_title = re.compile(r'\stitle=["\'](.*?)["\'][\s>]')


def handle(url,channelId,tvNumber):
    return showPageAnalysise(url,channelId,tvNumber)


#=========================================================

def showPageAnalysise(url,channelId,tvNumber):
    html = getAllEpisodes(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//div//ul/li[@class="ititle" or @class="ititle_w"]/a')
    if not videoList:
        videoList = tree.xpath('//div[@id="episode"]//ul/li[not(@class)]/a')
        
    videoList2 = []
    for video in videoList:
        title = etree.tostring(video,encoding="utf-8",method="html").decode("utf-8")
        title = p_title.search(title).groups()[0]
        url = video.xpath('./@href')[0]
        item = buildResource(url,title,-1,channelId)
        
        videoList2.append(item)
    #pprint.pprint(videoList2) 
    return videoList2
    

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
        #print url_e
        html = get_html(url_e)
        ans += html
    ans += '</div></html>'
    #print ans
    return ans
    



def buildResource(url,title,hot,channelId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['hot'] = hot
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['type'] = 'video'
    #resource['source'] = 'indexYouku'
    resource['videoType'] = 'youku'
    resource['videoId'] =  p_vid.search(url).groups()[0]
    resource['createTime'] = getCurTime()
    return resource.getInsertDict()
    

if __name__ == '__main__':
    pprint.pprint(handle('http://www.youku.com/show_page/id_zc8725626907411e29498.html',100148 ,1))

