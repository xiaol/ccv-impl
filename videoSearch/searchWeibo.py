#coding=utf-8
import redis
from setting import clct_channel,clct_resource
import imp,sys
from pprint import pprint
from common.common import getCurTime
from common.videoInfoTask import addVideoInfoTask
from handlesWeibo.handle_weibo import handle
from setting import clct_userWeibo


def insertResouce(weiboList,channelId,snapShot = False, updateTvNumber = False):
    '''更新时间 频道updateTime'''

    updateMap = {'updateTime':getCurTime()}
    clct_channel.update({'channelId':channelId},{'$set':updateMap})

    '''入库'''
    t = getCurTime()
    for weibo in weiboList:
        resource = weibo['resource']
        resource['createTime'] = t
        print("insert ",resource['videoType'],resource['videoId'])
        resource['weight'] = -1
        try:
            ret = clct_resource.insert(resource , safe=True)
            weibo['resourceId'] = ret['_id']
        except:
            print("insert Error!")
            ret  = clct_resource.find_one({'videoType':resource['videoType'], 'videoId':resource['videoId']})
            weibo['resourceId'] = ret['_id']

        else:
            print("insert Ok!")

            '''新增 截图任务'''
            if snapShot:
                mp4box = True if resource['videoType'] == 'sohu_url' else False
                addVideoInfoTask(resource['channelId'],str(ret),resource['videoId'],resource['videoType'],mp4box,force=True)


    #清除 视频权重
    clct_resource.update({'channelId':channelId,'weight':{'$ne':-1}},{'$set':{'weight':-1}},multi=True)

    return weiboList

def insertWeibo(weiboList):
    pass

def proccess(item):
    weiboList = handle()
    weiboList = insertResouce(weiboList)
    insertWeibo(weiboList)



def main():
    while True:
        #item = redisHost.blpop('xx')
        proccess(item)



if __name__ == '__main__':
    main()