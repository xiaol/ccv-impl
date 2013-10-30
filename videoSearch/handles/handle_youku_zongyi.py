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




#=========================================================

def handle(url,channelId,tvNumber):
    html = getAllEpisodes(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//div//ul/li[@class="ititle" or @class="ititle_w"]')
    if not videoList:
        videoList = tree.xpath('//div[@id="episode"]//ul/li[not(@class)]')
    
    videoList2 = []
    for video in videoList:
        title = video.xpath('./a/@title')[0]
        url = video.xpath('./a/@href')[0]
        number = video.xpath('./label/text()')[0]
        print('number:',number,'tvNumber:',tvNumber)
        if number <= tvNumber:
            continue
        item = buildResource(url,title,number,-1,channelId)
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


def buildResource(url,title,number,hot,channelId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['hot'] = hot
    resource['number'] = number
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['type'] = 'video'
    resource['videoType'] = 'youku'
    resource['videoId'] =  p_vid.search(url).groups()[0]
    resource['createTime'] = getCurTime()
    return resource.getInsertDict()
    

if __name__ == '__main__':
    #pprint.pprint(handle('http://www.youku.com/show_page/id_z1e2a5fe0b6b511e1b16f.html',1))
    pprint.pprint(handle('http://www.youku.com/show_page/id_z0ca9051c242511e38b3f.html',100148,''))

