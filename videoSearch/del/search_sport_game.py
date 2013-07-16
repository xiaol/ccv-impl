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
    result = module.handle(url,channelId,0)
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
    # 中超
    startSearch('handles.handle_iqiyi_list', 'http://list.iqiyi.com/www/17/1673-1674-----------2-1-1-1---.html',100095)
    # 欧冠
    startSearch('handles.handle_iqiyi_list', 'http://list.iqiyi.com/www/17/1673-1915-----------2-1-1-1---.html',100129)
    # 英超
    startSearch('handles.handle_iqiyi_list', 'http://list.iqiyi.com/www/17/1673-1677-----------2-1-1-1---.html',100130)
    # 极限运动
    startSearch('handles.handle_iqiyi_list', 'http://list.iqiyi.com/www/17/1711------------2-1-1-1---.html',100128)
    # NBA十佳
    startSearch('handles.handle_iqiyi_list', 'http://list.iqiyi.com/www/17/1688-1690-----------2-1-1-1---.html',100125)

if __name__ == '__main__':
    main()
#    pass
#    name = 'handles.handle_revenge2'
#    __import__('handles.handle_revenge2')
#    import sys
#    print sys.modules[name]