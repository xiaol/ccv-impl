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
        addVideoInfoTask(resource['channelId'],str(id),resource['videoId'],resource['videoType'],mp4box)

def startSearch(handleName,url,channelId):
    #获取模块
    __import__(handleName)
    module = sys.modules[handleName]
    channel = clct_channel.find_one({'channelId':channelId})
    resourceImageUrl = channel['resourceImageUrl']
    #抽取
    result = module.handle(url,channelId)
    pprint(result)
    if channel['autoOnline'] == False:
        for one in result:
            one['isOnline'] = False
            one['resourceImageUrl'] = resourceImageUrl
            one['duration'] = channel['duration']
            
    #入库
    if len(result) != 0:
        insertResouce(result,channelId)
    

def main():

    # 日韩花美男
    #startSearch('handles.handle_youku_showPage', 'http://www.iqiyi.com/dianshiju/jjdph45.html',100123)
    # 熟女偷拍
    startSearch('handles.handle_baomihua_specialEdition', 'http://app.baomihua.com/u/1673',100121)
    # 宅男女神
    #startSearch('handles.handle_baomihua_specialEdition1', 'http://app.baomihua.com/u/1346',100120)
    # 惹火自拍
    #startSearch('handles.handle_baomihua_specialEdition1', 'http://app.baomihua.com/u/1772',100119)

if __name__ == '__main__':
    main()
#    pass
#    name = 'handles.handle_revenge2'
#    __import__('handles.handle_revenge2')
#    import sys
#    print sys.modules[name]