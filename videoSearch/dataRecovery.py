#coding=utf-8
import redis
from setting import clct_channel,clct_resource,clct_userWeibo,clct_playLog, clct_user, clct_userRecommend, debug
import imp,sys
from pprint import pprint
import json ,time, re
from common.HttpUtil import get_html,HttpUtil
from bson import ObjectId
import urllib2
from common.common import getCurTime,strB2Q,strQ2B
from common.Domain import Resource
from common.videoInfoTask import addVideoInfoTask
from bson.objectid import ObjectId

__author__ = 'Ivan liu'

def main():
    rets = clct_userRecommend.find({'isViewed':-1,'snapshot':"doingGif"})

    for ret in rets:
        retR = clct_resource.find_one({'_id':ObjectId(ret['resourceId'])})
        if retR['isOnline']:
            clct_userRecommend.update({'uuid':ret['uuid'], 'resourceId':ret['resourceId']},{'$set':{'snapshot':'done'}})
        else:
            clct_userRecommend.update({'uuid':ret['uuid'], 'resourceId':ret['resourceId']},{'$set':{'snapshot':retR['snapshot']}})



if __name__ == '__main__':
    main()
