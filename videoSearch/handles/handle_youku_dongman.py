#coding=utf-8
import os,sys
from compiler.pycodegen import EXCEPT
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
p_number = re.compile(u'更新至(\d+)')
p_totalNumber = re.compile(u'共(\d+)集')
p_title_number = re.compile(u'第(\d+)')
p_title = re.compile(r'title="(.*?)" href=')

#=========================================================

def handle(url,channelId,tvNumber):
    #剧集网页
    html = getAllEpisodes(url)
    videosTree = etree.HTML(html)
    videoList = videosTree.xpath('//div[@id="episode"]//ul/li[not(@class)]/a')
    
    #原始网页
    #tree = etree.HTML(get_html(url))

    '''判断是否 剧集数 与网站标示一致'''
    #curNumber = None
    # try:
    #     curNumber = int(p_number.search(tree.xpath('//div[@class="basenotice"]/text()')[0]).groups()[0])
    # except:
    #     pass
    # if curNumber:
    #     assert curNumber == len(videoList)
    
    '''抽取'''
    ret = []
    for i, video in enumerate(videoList):
        title = etree.tostring(video,encoding="utf-8",method="html").decode()
        title = p_title.search(title).groups()[0]
        url = video.xpath('./@href')[0]
        number = p_title_number.search(title)
        if number:
            number = int(number.groups()[0])
        else:
            number = i+1
        if number <= tvNumber:
            continue
        videoId = p_vid.search(url).groups()[0]
        ret.append(buildResource(url,title,number,channelId,videoId))
    
    '''判断是否完结'''
    try:
        totalNumber = int(p_totalNumber.search(tree.xpath('//div[@class="basenotice"]/text()')[0]).groups()[0])
        if totalNumber == len(videoList):
            ret.append("over")
    except:
        pass
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
        #print url_e
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
    pprint.pprint(handle('http://www.youku.com/show_page/id_z7f0f6662322e11e2b2ac.html',100254,12))
    #pprint.pprint(handle('http://www.youku.com/show_page/id_zf33e2e705bd111e2b356.html',100253,31))

