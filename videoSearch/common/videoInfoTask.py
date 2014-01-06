#coding=utf-8
#import sys,os
#sys.path += [os.path.abspath(os.path.dirname(__file__))]
#print(sys.path)
from Domain import VideoInfoTask
try:
    from setting import clct_videoInfoTask,clct_resource
except:
    from ..setting import clct_videoInfoTask,clct_resource
from bson import ObjectId

def  addVideoInfoTask(channelId, resourceId, videoId, videoType, mp4box = False, force = False, goOnline = False, type= 'snap',priority=0):
    '''
        错误的resourceId
    '''
    videoInfoTask = VideoInfoTask()
    videoInfoTask['channelId'] = channelId
    videoInfoTask['resourceId'] = resourceId
    videoInfoTask['videoId'] = videoId
    videoInfoTask['videoType'] = videoType
    videoInfoTask['mp4box'] = mp4box
    videoInfoTask['force'] = force
    videoInfoTask['goOnline'] = goOnline
    videoInfoTask['type'] = type
    videoInfoTask['priority'] = priority
    
    resource = clct_resource.find_one({'_id':ObjectId(resourceId)})
    if resource == None:
        return False
    #已经有截图，强制刷新
    if resource['resourceImageUrl'] != '' and not force:
        return False
    if clct_videoInfoTask.find_one({'resourceId':videoInfoTask['resourceId']}):
        clct_videoInfoTask.remove({'resourceId':videoInfoTask['resourceId']},mulit=True)
    clct_videoInfoTask.insert(videoInfoTask.getInsertDict())
    clct_resource.update({'_id':ObjectId(resourceId)},{'$set':{"snapshot": "pending"}})
    return True
