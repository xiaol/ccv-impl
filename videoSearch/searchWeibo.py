#coding=utf-8
import redis
from setting import clct_channel,clct_resource,clct_userWeibo, debug
import imp,sys
from pprint import pprint
import json ,time, os
from common.common import getCurTime
from common.videoInfoTask import addVideoInfoTask
from handlesWeibo.handle_weibo import handle, handleGif
from setting import clct_channel, clct_resource, GIF_SERVER, GIF_SERVER_PORT, GIF_SERVER_DIR, GIF_TEMP_DIR

redisUrl = 'localhost'
if not debug:
    redisUrl = 'h48'


def insertResouce(weiboList, channelId, snapShot = False, updateTvNumber = False):
    '''更新时间 频道updateTime'''

    updateMap = {'updateTime':getCurTime()}
    clct_channel.update({'channelId':channelId},{'$set':updateMap})

    '''入库'''
    t = getCurTime()
    for weibo in weiboList:
        resource = weibo['resource']
        resource['createTime'] = t
        resource['type'] = 'video'
        resource['resourceName'] = weibo['userWeibo']['title']
        resource['resourceUrl'] = weibo['userWeibo']['videoUrl']
        resource['categoryId'] = 0
        resource['isOnline'] = False
        resource['source'] = 'weibo'
        resource['updateTime'] = weibo['userWeibo']['updateTime']
        print("insert ",resource['videoType'],resource['videoId'], resource['resourceUrl'])
        resource['weight'] = -1
        try:
            ret = clct_resource.insert(resource , safe=True)
            weibo['userWeibo']['resourceId'] = str(ret)
        except Exception,e:
            print("insert Error!",e)
            ret  = clct_resource.find_one({'videoType':resource['videoType'], 'videoId':resource['videoId']})
            weibo['userWeibo']['resourceId'] = str(ret['_id'])

        else:
            '''新增 截图任务'''
            if snapShot:
                mp4box = True if resource['videoType'] == 'sohu_url' else False
                addVideoInfoTask(resource['channelId'],str(ret),resource['videoId'],resource['videoType'],mp4box,force=True,goOnline=True,priority=1)

    return weiboList

def insertWeibo(weiboList):
    t = getCurTime()

    for weibo in weiboList:
        userWeibo = weibo['userWeibo']
        userWeibo['createTime'] = t
        try:
            ret = clct_userWeibo.insert(userWeibo , safe=True)
        except Exception,e:
            print("Insert Error!",e)
            #ret  = clct_userWeibo.find_one({'weiboId':userWeibo['weiboId'],})
        else:
            pass


def process(isNew, access_token, sinaId, sinaName, channelId):
    if isNew:
        since_id,page,count = 0,1,10
    else:
        page,count = 1,100
        x = clct_userWeibo.find_one({'sinaId':sinaId},sort=[('weiboId',-1)])
        if x is None:
            since_id = 0
        else:
            since_id  = x['weiboId']
            print("latest weibo id:",since_id)

    weiboList = handle(channelId, access_token, since_id, sinaId, sinaName, page, count)
    weiboList = insertResouce(weiboList, channelId, True)
    print("Insert ",sinaId, sinaName)
    insertWeibo(weiboList)


def processGif(isNew, access_token, sinaId, sinaName, channelId,since_id,page,count):
    gifList = handleGif(channelId, access_token, since_id, sinaId, sinaName, page, count)

    for gifMap in gifList:
        one = gifMap['resource']
        one['isOnline'] = True
        one['duration'] = -1
        one['categoryId'] = 0
        one['type'] = 'gif'

    #拷贝本地gif和png到47服务器 然后删除本地图片
    cmd = 'scp -P %d -r %s/videoCMS/gif_resource/%d %s:%s' \
          % (GIF_SERVER_PORT, GIF_TEMP_DIR, channelId, GIF_SERVER, GIF_SERVER_DIR)
    os.popen(cmd)
    cmd = 'rm -f %s/videoCMS/gif_resource/%d/*.*' % (GIF_TEMP_DIR, channelId)
    os.popen(cmd)

    gifList = insertResouce(gifList, channelId, True)
    print("Insert gif ",sinaId, sinaName)
    insertWeibo(gifList)

def main():
    redisHost = redis.Redis(redisUrl, 6379)
    while True:
        try:
            originalMsg = redisHost.blpop('weibo')   #timeout=3
            if originalMsg is None:
                #time.sleep(2)
                continue
            start = time.time()
            msg = json.loads(originalMsg[1])
            process(msg['isNew'], msg['access_token'],msg['sinaId'],msg['sinaName'], 1)
            elapsed = (time.time() - start)
            print("Time used:",elapsed)

        except Exception,e:
            print e


if __name__ == '__main__':
    main()
