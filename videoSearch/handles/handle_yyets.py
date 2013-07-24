#coding=utf-8
import sys,os,re
sys.path += [os.path.dirname(os.path.dirname(__file__))]

from common.HttpUtil import get_html
from lxml import etree
from common.Domain import Resource
from setting import clct_channel
from common.common import getCurTime
import urllib


p = re.compile('\|file\|([^\|]+?)\|')
pse  = re.compile('[Ss](\d+)[Ee](\d+)')

def extractTasks(url,channelId,season=None,format="MP4",type="ed2k"):
    tree = etree.HTML(get_html(url))
    if season:
        xpath = '//div[@class="box_1"]/ul[@season="%s"]/li[@format="%s"]/span[@class="r"]/a[@type="%s"]/@href'%(season,format,type)
    else:
        xpath = '//div[@class="box_1"]/ul/li[@format="%s"]/span[@class="r"]/a[@type="%s"]/@href'%(format,type)
    urls = tree.xpath(xpath)
    ans = []
    for url in urls:
        filename = p.search(url).groups()[0]
        filename = urllib.unquote(filename).decode('utf-8')
        name = filename[:filename.find('.')]
        number = 0
        if season:
            print filename
            try:
                m = pse.search(filename)
                name += ' 第%s季第%s集'%(m.groups()[0],m.groups()[1])
                number = m.groups()[1]
            except:
                print '[error] %s can\'t be recognized '
                continue
        #ans.append({'name':name,'url':url,'filename':filename})
        channel = clct_channel.find_one({'channelId':channelId})
        resourceImageUrl = channel['resourceImageUrl']
        resource = Resource()
        resource['resourceName'] = name
        resource['resourceImageUrl'] = resourceImageUrl
        resource['channelId'] = channelId
        resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
        resource['createTime'] = getCurTime()
        resource['resourceUrl'] = url
        resource['type'] = 'video'
        resource['videoType'] = 'bt'
        resource['videoId'] = filename
        resource['number'] = int(number)
        ans.append(resource.getInsertDict())
    return ans    
    
if __name__ =='__main__':
    #extractTasks('http://www.yyets.com/resource/10733',100866 )
    print extractTasks('http://www.yyets.com/resource/10220',100866 )