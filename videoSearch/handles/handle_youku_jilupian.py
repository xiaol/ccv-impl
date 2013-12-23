#coding=utf-8
import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re,pprint
from common.common import getCurTime
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel

p_vid = re.compile('id_([\w=]+?).html')
p_reload = re.compile("y\.episode\.show\('(\w+?)'\)")
p_title = re.compile(r'\stitle=["\'](.*?)["\'][\s>]')


def handle(url,channelId,tvNumber):
    html = getAllEpisodes(url)
    tree = etree.HTML(html)
    videoList = tree.xpath('//div[@id="episode"]//ul/li[@class="ititle" or @class="ititle_w"]')
        
    ret = []
    for video in videoList:
        try:
            title = etree.tostring(video,encoding="utf-8",method="html").decode("utf-8")
            title = p_title.search(title).groups()[0]
            url = video.xpath('./a/@href')[0]
            number = int(video.xpath('./label/text()')[0])
        except:
            continue
        if number <= tvNumber:
                continue
        item = buildResource(url,title,number,-1,channelId)
        ret.append(item)
    #pprint.pprint(videoList2) 
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
    



def buildResource(url,title,number,hot,channelId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['hot'] = hot
    resource['number'] = number
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = 'youku'
    resource['videoId'] =  p_vid.search(url).groups()[0]
    resource['createTime'] = getCurTime()
    return resource.getInsertDict()
    

if __name__ == '__main__':
    pprint.pprint(handle('http://www.youku.com/show_page/id_z9bf39884b4f311e0a046.html', 100000, 1))

