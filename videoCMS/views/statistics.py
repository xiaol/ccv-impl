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
            if not resource:
                resource2channelMap[resourceId] = (None, None)
            else:
                    resource2channelMap[resourceId] = (resource['channelId'],resource['categoryId'])
            #print "channelId not hit"
        return resource2channelMap[resourceId][0]

    def _getCategoryId(resourceId):
        if resourceId not in resource2channelMap:
            resource = clct_resource.find_one({'_id':ObjectId(resourceId)}, {'channelId':1,'categoryId':1})
            if not resource:
                resource2channelMap[resourceId] = (None, None)
            else:
                resource2channelMap[resourceId] = (resource['channelId'],resource['categoryId'])
            #print "categoryId not hit",resourceId
        else:
            pass
            #print 'hit'
        return resource2channelMap[resourceId][1]


    return _getChannelId, _getCategoryId

'''
def CacheChannel(channelIdList):
    channelMap = {}
    print 'channelIdList len:',len(channelIdList)
    begin = 0
    while begin < len(channelIdList):
        if begin + 100 > len(channelIdList):
            ids = channelIdList[begin:]
        else:
            ids = channelIdList[begin : begin+100]
        for channel in clct_channel.find({'channelId':{'$in':ids}}):
            channelMap[channel['channelId']] = channel
        begin += 100
'''

def getCategoryDetailList():

    return list(clct_category.find())



def category(request):
    DICT = {}
    categoryList = getCategoryDetailList()


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
    DICT['navPage'] = 'statistics'
    DICT['title'] = '分类统计'

    return render_to_response("statisticsCategory.htm",DICT)




def channel(request):
    DICT = {}

    DICT["startDate"],DICT["endDate"],t_start,t_end,startTime,endTime = getStartEndDateTime(request)
    categoryName = request.GET.get('categoryName',"全部")
    limit = int(request.GET.get('limit',20))
    sort = request.GET.get('sort','downplayNum')

    spec = {}
    if categoryName != u"全部":
        filterCategoryId = getCategoryIdByName(categoryName)
    else:
        filterCategoryId = None
    print 'filterCategoryId:',filterCategoryId
    spec['createTime'] = {'$gte':startTime, '$lte':endTime}
    spec["operationCode"] = {"$in":[10001, 10004]}

    #开始统计
    logs = list(clct_operationLog.find(spec))

    print '初始化getChannelId'
    getChannelId,getCategorylId = CacheResources([one['resourceId'] for one in logs])

    print '开始统计'
    result = {}
    '''
        {
            channelId:(下载数，播放数, 总数)
        }
    '''
    for log in logs:
        #print log
        resourceId = log['resourceId']
        if resourceId == 'default':
            continue
        categoryId = getCategorylId(resourceId)
        if filterCategoryId and filterCategoryId != categoryId:
            continue 
        channelId = getChannelId(resourceId)
        if not channelId:
            continue
        if channelId not in result:
            result[channelId] = [0,0,0]
        #下载
        if log['operationCode'] == 10001:
            result[channelId][0] += 1
        #播放
        if log['operationCode'] == 10004:
            result[channelId][1] += 1
        #总数
        result[channelId][2] += 1

    #将结果转化成 数组
    L = []
    for key in result:
        item = {}
        item['channelId'] = key
        item['data'] = result[key]
        L.append(item)
    #排序
    if sort == 'downplayNum':
        L.sort(key=lambda a:a['data'][2], reverse=True)
    elif sort == 'downloadNum':
        L.sort(key=lambda a:a['data'][0], reverse=True)
    elif sort == 'playNum':
        L.sort(key=lambda a:a['data'][1], reverse=True)


    L = L[:limit]

    for one in L:
        channel = clct_channel.find_one({'channelId':one['channelId']})
        if not channel:
            print 'channelId not exists:',one['channelId']
            continue
        one['channelName'] = channel['channelName']
        one['subscribeNum'] = channel['subscribeNum']
        one['categoryName'] = getCategoryNameById(channel['channelType'])


    DICT['result'] = L
    DICT['categoryList'] = [u'全部'] + getCategoryList()
    DICT['categoryName'] = categoryName
    DICT['sort'] = sort
    DICT['limit'] = limit
    DICT['navPage'] = 'statistics'
    DICT['title'] = '频道下载/播放统计'
    return render_to_response('statisticsChannel.htm',DICT)


def channelSub(request):
    DICT = {}
    categoryName = request.GET.get('categoryName',"全部")
    limit = int(request.GET.get('limit',20))
    mongo = request.GET.get('mongo','')



    spec = {}
    if categoryName != u"全部":
        spec['channelType'] = getCategoryIdByName(categoryName)
    if mongo:
        spec = json.loads(mongo)

    L = list(clct_channel.find(spec).sort([('subscribeNum',-1)]).limit(limit))
    for one in L:
        one['categoryName'] = getCategoryNameById(one['channelType'])
    DICT['result'] = L
    DICT['categoryList'] = [u'全部'] + getCategoryList()
    DICT['categoryName'] = categoryName
    DICT['limit'] = limit
    DICT['navPage'] = 'statistics'
    DICT['title'] = '频道下载/播放统计'
    DICT['mongo'] = mongo
    return render_to_response('statisticsChannelSub.htm',DICT)



def resource(request):
    DICT = {}

    DICT["startDate"],DICT["endDate"],t_start,t_end,startTime,endTime = getStartEndDateTime(request)
    categoryName = request.GET.get('categoryName',"全部")
    channelId = request.GET.get('channelId',"")
    limit = int(request.GET.get('limit',20))
    sort = request.GET.get('sort','downplayNum')

    if channelId != "":
        filterChannelId = int(channelId)
    else:
        filterChannelId = None
    if categoryName != u"全部":
        filterCategoryId = getCategoryIdByName(categoryName)
    else:
        filterCategoryId = None
    print 'filterCategoryId:',filterCategoryId

    spec = {}
    spec['createTime'] = {'$gte':startTime, '$lte':endTime}
    spec["operationCode"] = {"$in":[10001, 10004]}


    #开始统计
    logs = list(clct_operationLog.find(spec))

    print '初始化getChannelId'
    getChannelId,getCategorylId = CacheResources([one['resourceId'] for one in logs])

    print '开始统计'
    result = {}
    '''
        {
            resourceId:(下载数，播放数, 总数)
        }
    '''
    for log in logs:
        #print log
        resourceId = log['resourceId']
        if resourceId == 'default':
            continue
        categoryId = getCategorylId(resourceId)
        if filterCategoryId and filterCategoryId != categoryId:
            continue 
        channelId = getChannelId(resourceId)
        if filterChannelId and  channelId != channelId:
            continue

        if resourceId not in result:
            result[resourceId] = [0,0,0]
        #下载
        if log['operationCode'] == 10001:
            result[resourceId][0] += 1
        #播放
        if log['operationCode'] == 10004:
            result[resourceId][1] += 1
        #总数
        result[resourceId][2] += 1

    #将结果转化成 数组
    L = []
    for key in result:
        item = {}
        item['resourceId'] = key
        item['channelId'] = getChannelId(resourceId)
        item['categoryId'] = getCategoryId(resource)
        item['data'] = result[key]
        L.append(item)
    #排序
    if sort == 'downplayNum':
        L.sort(key=lambda a:a['data'][2], reverse=True)
    elif sort == 'downloadNum':
        L.sort(key=lambda a:a['data'][0], reverse=True)
    elif sort == 'playNum':
        L.sort(key=lambda a:a['data'][1], reverse=True)


    L = L[:limit]

    for one in L:
        channel = clct_channel.find_one({'channelId':one['channelId']})
        if not channel:
            print 'channelId not exists:',one['channelId']
            continue
        one['channelName'] = channel['channelName']
        one['categoryName'] = getCategoryNameById(channel['channelType'])


    DICT['result'] = L
    DICT['categoryList'] = [u'全部'] + getCategoryList()
    DICT['categoryName'] = categoryName
    DICT['sort'] = sort
    DICT['limit'] = limit
    DICT['navPage'] = 'statistics'
    DICT['title'] = '频道下载/播放统计'
    return render_to_response('statisticsChannel.htm',DICT)