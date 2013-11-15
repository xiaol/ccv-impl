#coding=utf-8
#__author__ = 'Ivan liu'

from setting import clct_channel,clct_resource,clct_userWeibo,clct_playLog, clct_user, clct_userRecommend, debug
import imp,sys
from pprint import pprint
import json ,time, re
from common.HttpUtil import get_html,HttpUtil
from bson import ObjectId
from common.videoInfoTask import addVideoInfoTask

def main():
    retC = clct_channel.find_one({'channelId':100270})
    if retC is not None:
        retR = clct_resource.find({'channelId':retC['channelId']})
        for resource in retR:
            mp4box = True if resource['videoType'] == 'sohu_url' else False
            addVideoInfoTask(resource['channelId'],str(resource['_id']),resource['videoId'],resource['videoType'],mp4box,force=True,goOnline=True)

if __name__ == '__main__':
    main()
