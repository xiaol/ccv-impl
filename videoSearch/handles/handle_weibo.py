#coding=utf-8
import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from lxml import etree
import re,pprint,json
from common.common import getCurTime
from pymongo import Connection
from common.Domain import Resource,Channel
from common.HttpUtil import get_html,HttpUtil
from setting import TOKEN,APP_KEY
from setting import clct_channel


p_1 = re.compile('http://(.*?)/')
p_url = re.compile('http://[\w\./]*')
p_sina = re.compile('http://video.sina.com.cn/v/b/(.*?)\.html')
    

def handle(weibo_uid,channelId,tvNumber,page=1,count=20):
    httpUtil = HttpUtil()
    # 列表页
    url = 'https://api.weibo.com/2/statuses/user_timeline.json?source=%s&access_token=%s&uid=%s&page=%s&count=%s'%(APP_KEY,TOKEN,weibo_uid,page,count)
    print url
    html = get_html(url)
    videos = json.loads(html)['statuses']
    videoList  = []
    for video in  videos:
        item = {}
        if 'retweeted_status' in video:
            continue
        #print video['text']
        try:
            item['url'] = p_url.search(video['text']).group()
            item['url'] = httpUtil.real_url(item['url'])
            if item['url'].find('http://video.sina.com.cn') != -1:
                item['videoType'] = 'sina'
                item['videoId'] = p_sina.search(item['url']).groups()[0]
            else:
                continue
            item['title'] = video['text']
        except:
            continue
        #print item
        videoList.append(buildResource(item['url'] , item['title'], channelId, item['videoType'], item['videoId']))

    return videoList




def buildResource(url,title,channelId,videoType,videoId):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['type'] = 'video'
    resource['videoType'] = videoType
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    resource['modifyTime'] = getCurTime()
    
    return resource.getInsertDict()
    

if __name__ == '__main__':
    pprint.pprint(handle('2214257545',int(13),1,100))

