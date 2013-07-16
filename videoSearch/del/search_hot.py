#coding=utf-8
from setting import clct_channel,clct_resource
import imp,sys
from pprint import pprint
from common.common import getCurTime
from common.videoInfoTask import addVideoInfoTask

def insertResouce(resouceList,channelId):
    #更新时间 频道updateTime
    clct_channel.update({'channelId':channelId},{'$set':{'updateTime':getCurTime()}})
    #入库
    t = getCurTime()
    for resource in resouceList:
        resource['createTime'] = t
        
    ret = clct_resource.insert(resouceList)
    '''新增 截图任务'''
    for id,resource in zip(ret,resouceList):
        mp4box = True if resource['videoType'] == 'sohu_url' else False
        addVideoInfoTask(resource['channelId'],str(id),resource['videoId'],resource['videoType'],mp4box,force=True)
    

def startSearch(handleName,url,channelId):
    #获取模块
    __import__(handleName)
    module = sys.modules[handleName]
    channel = clct_channel.find_one({'channelId':channelId})
    resourceImageUrl = channel['resourceImageUrl']
    #抽取
    result = module.handle(url,channelId)
    pprint(result)
    
    for one in result:
        if channel['autoOnline'] == False:
            one['isOnline'] = False
        one['resourceImageUrl'] = resourceImageUrl
        one['duration'] = channel['duration']
    #入库
    if len(result) != 0:
        insertResouce(result,channelId)


def main():
    #新闻热点
    #startSearch('handles.handle_youku_template1', 'http://news.youku.com/hotnews/all',100047)
    
    # Youtube国外精选
    #startSearch('handles.handle_weibo', '2214257545',100052)
    
    #微博最热
    #startSearch('handles.handle_weibo', '2141823055',100050)
    
    #内涵搞笑
    #startSearch('handles.handle_jimu', 'http://www.jimu.tv/video/ajax/list/all.html?start=0&count=20&rank=hot',100049)
    #时光网预告片
    startSearch('handles.handle_mtime', 'http://www.mtime.com/trailer/',100055)


if __name__ == '__main__':
    main()
