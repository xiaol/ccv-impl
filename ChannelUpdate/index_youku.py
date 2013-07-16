#coding=utf-8
from HttpUtil import HttpUtil
from lxml import etree
import re,pprint
from common import getCurTime
from pymongo import Connection
from Domain import Resource,Channel

p_vid = re.compile('id_([\w=]+?).html')
p_reload = re.compile("y\.episode\.show\('(\w+?)'\)")

con = Connection('60.28.29.49:20011')
clct_channel = con.iDown.channel
clct_resource = con.iDown.resource



def _w2f(s,filename):
    with open(filename,'w+') as f:
        f.write(s)

def insertChannel(name,channelId,url):
    ret = clct_channel.find_one({'channelId':channelId})
    if ret != None:
        print('exists channelId: ',ret['channelId'])
        return ret['channelId']
    
    channel = Channel()
    channel['channelName'] = name
    channel['channelId'] = channelId
    channel['oriUrl'] = url
    
    pprint.pprint(channel.getInsertDict())
    clct_channel.insert(channel.getInsertDict())
    return channelId




def listPageAnalysise(url,startId):
    httpUtil = HttpUtil()
    html = httpUtil.Get(url).decode('utf-8')
    tree = etree.HTML(html)
    pageList = tree.xpath('//div[@class="sRank_W"]//td[@class="show_title"]/a')
    pageList2 = []

    for i,page in enumerate(pageList):
        title = page.xpath('./@title')[0]
        url = page.xpath('./@href')[0]
        print('======== start %s %s======='%(title,url))
        channelId = insertChannel(title,startId + i,url)
        item = showPageAnalysise(channelId , url, '')
        #pageList2.append(item)
        print('find %d items in %s'%(len(item),title))
        import pprint
        pprint.pprint(item)
        clct_resource.insert(item)
    
    pprint.pprint(pageList2)
    return pageList2

def showPageAnalysise(channelId,url,year):
    html = getAllEpisodes(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//div//ul/li[@class="ititle" or @class="ititle_w"]/a')
    if not videoList:
        videoList = tree.xpath('//div[@id="episode"]//ul/li[not(@class)]/a')
        
    videoList2 = []
    for video in videoList:
        title = video.xpath('./@title')[0]
        url = video.xpath('./@href')[0]
        item = buildResource(url,title,-1,channelId)
        videoList2.append(item)
    #pprint.pprint(videoList2) 
    return videoList2
    

def getAllEpisodes(url):
    httpUtil = HttpUtil()
    html = httpUtil.Get(url).decode('utf-8')
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
        html = httpUtil.Get(url_e).decode('utf-8')
        ans += html
    ans += '</div></html>'
    #print ans
    return ans
    

def taskAnalysise(url,title,hot,channelId):
    task = {'type':'youku'}
    task['oriUrl'] = url
    task['videoId'] = p_vid.search(url).groups()[0]
    task['title'] = title
    task['source'] = 'indexYouku'
    task['channelId'] = channelId
    task['createTime'] = getCurTime()
    task['hot'] = hot
    return task    

def buildResource(url,title,hot,channelId):
    resource = Resource()
    resource['resourceName'] = title
    resource['hot'] = hot
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['source'] = 'indexYouku'
    resource['videoType'] = 'youku'
    resource['videoId'] =  p_vid.search(url).groups()[0]
    resource['createTime'] = getCurTime()
    return resource.getInsertDict()
    


def main():
    #动漫
    listPageAnalysise('http://comic.youku.com/top/',10000)
    #电视剧
    listPageAnalysise('http://tv.youku.com/top/',20000)
    #综艺
    listPageAnalysise('http://zy.youku.com/top/',30000)
    #纪录片
    listPageAnalysise('http://jilupian.youku.com/top/',40000)
    #ret = showPageAnalysise('',1,'http://www.youku.com/show_page/id_z7b09e50c32ba11e1b16f.html','2012')
    #pprint.pprint(ret)
    #print len(ret)

if __name__ == '__main__':
    main()