#coding=utf-8
import redis
from setting import clct_channel,clct_resource,clct_userWeibo
import imp,sys
from pprint import pprint
import json
from common.common import getCurTime
from common.videoInfoTask import addVideoInfoTask
from handlesWeibo.handle_weibo import handle
from setting import clct_userWeibo


def insertResouce(weiboList, channelId, snapShot = False, updateTvNumber = False):
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
            weibo['resourceId'] = str(ret['_id'])
        except:
            print("insert Error!")
            ret  = clct_resource.find_one({'videoType':resource['videoType'], 'videoId':resource['videoId']})
            weibo['resourceId'] = str(ret['_id'])

        else:
            '''新增 截图任务'''
            if snapShot:
                mp4box = True if resource['videoType'] == 'sohu_url' else False
                addVideoInfoTask(resource['channelId'],str(ret),resource['videoId'],resource['videoType'],mp4box,force=True)


    #清除 视频权重
    clct_resource.update({'channelId':channelId,'weight':{'$ne':-1}},{'$set':{'weight':-1}},multi=True)

    return weiboList

def insertWeibo(weiboList):
    t = getCurTime()
    for weibo in weiboList:
        userWeibo = weibo['userWeibo']
        userWeibo['createTime'] = t
        userWeibo['resourceId'] = weibo.get('resourceId','')

        print("Insert ",userWeibo['weiboId'],userWeibo['sinaId'],userWeibo['sinaName'])
        try:
            ret = clct_userWeibo.insert(userWeibo , safe=True)
        except:
            print("Insert Error!")
            #ret  = clct_userWeibo.find_one({'weiboId':userWeibo['weiboId'],})
        else:
            pass


def process(isNew, access_token, sinaId, sinaName, channelId):
    if isNew:
        since_id,page,count = 0,1,10
    else:
        page,count = 1,20
        x = clct_userWeibo.find_one({'sinaId':'sinaId'},sort=[('weiboId',-1)])
        if x is None:
            since_id = 0
        else:
            since_id  = x['weiboId']

    weiboList = handle(channelId, access_token, since_id, sinaId, sinaName, page, count)
    weiboList = insertResouce(weiboList, channelId, True)
    insertWeibo(weiboList)


def main():
    redisHost = redis.Redis('localhost', 6379)
    while True:
        #try:
        originalMsg = redisHost.blpop('weibo')
        msg = json.loads(originalMsg[1])
        process(msg['isNew'], msg['access_token'],msg['sinaId'],msg['sinaName'], 0)
        '''except TypeError:
            print "Can't parse json string."
        except KeyError:
            print "Can't find requested keys."
        except :
            print "Something bad happened."'''


if __name__ == '__main__':
    main()