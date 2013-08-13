#coding=utf8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
import json,StringIO,re,time
from videoCMS.conf import clct_resource,clct_category,clct_channel,clct_tag,IMAGE_DIR,IMG_INTERFACE,IMG_INTERFACE_FF,clct_cdnSync
from videoCMS.conf import CHANNEL_IMAGE_WIDTH,CHANNEL_IMAGE_HEIGHT,clct_videoInfoTask,clct_operationLog
from bson import ObjectId
from videoCMS.common.Domain import Resource,Tag,CDNSyncTask
from videoCMS.common.common import Obj2Str,getCurTime
from videoCMS.common.ImageUtil import imgconvert
from videoCMS.common.db import getCategoryList
from videoCMS.views.channel import saveResourceImage
from videoSearch.common.videoInfoTask import addVideoInfoTask
import urllib2,copy
from videoCMS.common.db import getCategoryNameById,getCategoryIdByName,getCategoryList,getCategoryIdMapName
from videoCMS.views.login import *

'''
def _GetCategorylId():
    channel2categoryMap= {}
    def _getCategorylId(channelId):
        if channelId in channel2categoryMap:
            return channel2categoryMap[channelId]
        else:
            categoryId = clct_channel.find_one({'channelId':channelId})['channelType']
            channel2categoryMap[channelId] = categoryId
            return categoryId
    return _getCategorylId
'''
#================================================
def getStartEndDateTime(request):
    startDate = request.GET.get('startDate','')
    endDate = request.GET.get('endDate','')
    if startDate == "":
        startDate = time.strftime('%Y/%m/%d',time.localtime(time.time() - 7*24*3600))
    if endDate == "":
        endDate = time.strftime('%Y/%m/%d',time.localtime())
    print startDate,endDate
    #时间戳
    t_start = time.mktime(time.strptime(startDate,'%Y/%m/%d'))
    t_end = time.mktime(time.strptime(endDate,'%Y/%m/%d')) + 24*3600
    #数据库查询
    startTime = time.strftime('%Y%m%d000000', time.localtime(t_start))
    endTime = time.strftime('%Y%m%d000000',time.localtime(t_end))

    return startDate,endDate,t_start,t_end,startTime,endTime

#================================================


def CacheResources(resourceIdList):
    '''预先缓存resourceIdList'''
    resource2channelMap = {}
    begin = 0
    print 'resourceIdList len:',len(resourceIdList)
    resourceIdList = list(set(resourceIdList))
    print 'uni len:',len(resourceIdList)


    while begin < len(resourceIdList):
        if begin + 100 > len(resourceIdList):
            ids = resourceIdList[begin:]
        else:
            ids = resourceIdList[begin : begin+100]
        obids = []
        for one in ids:
            try:
                obids.append(ObjectId(one))
            except:
                pass
        for resource in clct_resource.find({'_id':{'$in':obids}}, {'channelId':1,'categoryId':1}):
            resource2channelMap[str(resource['_id'])] = (resource['channelId'],resource['categoryId'])
        begin += 100

    print 'map len:',len(resource2channelMap.keys())

    def _getChannelId(resourceId):
        if resourceId not in resource2channelMap:
            resource = clct_resource.find_one({'_id':ObjectId(resourceId)}, {'channelId':1,'categoryId':1})
            resource2channelMap[resourceId] = (resource['channelId'],resource['categoryId'])
            #print "channelId not hit"
        return resource2channelMap[resourceId][0]

    def _getCategoryId(resourceId):
        if resourceId not in resource2channelMap:
            resource = clct_resource.find_one({'_id':ObjectId(resourceId)}, {'channelId':1,'categoryId':1})
            resource2channelMap[resourceId] = (resource['channelId'],resource['categoryId'])
            #print "categoryId not hit",resourceId
        else:
            pass
            #print 'hit'
        return resource2channelMap[resourceId][1]


    return _getChannelId, _getCategoryId



def getCategoryList():

    return list(clct_category.find())



def category(request):
    DICT = {}
    categoryList = getCategoryList()


    DICT["startDate"],DICT["endDate"],t_start,t_end,startTime,endTime = getStartEndDateTime(request)

    '''初始化 矩阵(其实是字典)''' 
    result = {}
    row = {}
    for one in categoryList:
        row[one['categoryId']] = [0,0]
    t = t_start
    while t < t_end:
        date = time.strftime('%Y%m%d',time.localtime(t))
        result[date] = copy.deepcopy(row)
        t += 24*3600

    '''
        {
            date:{
                categoryId:(0,0)
            }
        }
    '''
    '''填充 矩阵'''
    logs = list(clct_operationLog.find({'createTime':{'$gte':startTime, '$lte':endTime},"operationCode":{"$in":[10001, 10004]}}))
    print len(logs)

    print '初始化getChannelId'
    getChannelId,getCategorylId = CacheResources([one['resourceId'] for one in logs])

    print '开始统计'
    for i,log in enumerate(logs):
        #下载
        #print i
        try:
            if log['operationCode'] == 10001:
                date = log['createTime'][:8]
                categoryId = getCategorylId(log['resourceId'])
                result[date][categoryId][0] += 1
            elif log['operationCode'] == 10004:
                date = log['createTime'][:8]
                categoryId = getCategorylId(log['resourceId'])
                result[date][categoryId][1] += 1
        except:
            #print 'error:',log['resourceId']
            pass

    print '得到有序坐标行列'
    days = sorted(result.keys())
    categories = sorted(row.keys())

    sortedResult = [{"data":[result[day][category] for category in categories],"day":day} for day in days]


    categoryMap = {}
    for one in categoryList:
        categoryMap[one['categoryId']] = one
    DICT['days'] = days
    DICT['categories'] = categories
    DICT['categoryNames'] = [categoryMap[id]['categoryName'] for id in categories]
    DICT['sortedResult'] = sortedResult


    return render_to_response("statisticsCategory.htm",DICT)




def channel(request):
    DICT["startDate"],DICT["endDate"],t_start,t_end,startTime,endTime = getStartEndDateTime(request)
    categoryName = request.GET.get('categoryName',"全部")
    
    #

    spec = {}
    if categoryName != u"全部":
        spec["categoryId"] = getCategoryIdByName(categoryName)



def resource(request):
    pass