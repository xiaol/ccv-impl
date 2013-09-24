#coding=utf-8
import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from lxml import etree
import re,pprint,json
from common.common import getCurTime
from pymongo import Connection
from common.Domain import Resource,Channel
from common.HttpUtil import get_html,HttpUtil


p_1 = re.compile('http://(.*?)/')
p_url = re.compile('http://[\w\./]*')
p_sina = re.compile('http://video.sina.com.cn/v/b/(.*?)\.html')
p_youku = re.compile('http://v.youku.com/v_show/id_(.*?).html')
p_56 = re.compile('v_([^\.]+).html')

p_videos = [('sina',p_sina), ('youku',p_youku), ('56',p_56)]

def handle(channelId,access_token,since_id,page=1,count=20):
    httpUtil = HttpUtil()
    # 列表页
    url = 'https://api.weibo.com/2/statuses/home_timeline.json?' \
          'access_token=%s&since_id=%s&page=%s&count=%s&feature=3'%(access_token,since_id,page,count)
    print url
    html = get_html(url)
    videos = json.loads(html)['statuses']
    print len(videos)
    videoList  = []
    for video in  videos:
        item = {}
        if 'retweeted_status' in video:
            text = video['retweeted_status']['text']
        else:
            text = video['text']
        #print video['text']
        try:
            item['url'] = p_url.search(text).group()
            item['url'] = httpUtil.real_url(item['url'])
            print item['url']
            for p_video in p_videos:
                if p_video[1].search(item['url']):
                    item['videoType'] = p_video[0]
                    item['videoId'] = p_video[1].search(item['url']).groups()[0]
                    break
                else:
                    continue
            if 'videoType' not in item:
                continue
            item['title'] = text
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
    resource['type'] = 'video'
    resource['videoType'] = videoType
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    resource['modifyTime'] = getCurTime()
    
    return resource.getInsertDict()
    

if __name__ == '__main__':
    pprint.pprint(handle(0,'2.00JAa2ACfsSuoB59e11ed8f40Kt3ip','3625753381928262'))

