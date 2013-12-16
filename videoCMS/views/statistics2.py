#coding=utf8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import json,StringIO,re,time
from videoCMS.conf import clct_resource,clct_category,clct_channel,clct_tag,IMAGE_DIR,IMG_INTERFACE,IMG_INTERFACE_FF,clct_cdnSync
from videoCMS.conf import clct_playLog
from videoCMS.conf import CHANNEL_IMAGE_WIDTH,CHANNEL_IMAGE_HEIGHT,clct_videoInfoTask,clct_operationLog,clct_statisticsLog,clct_user,clct_subscribeLog,clct_searchLog
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


#================================================
def getStartEndDateTime(request):
    startDate = request.GET.get('startDate','')
    endDate = request.GET.get('endDate','')
    if startDate == "":
        startDate = time.strftime('%Y/%m/%d',time.localtime(time.time() - 7*24*3600))
    if endDate == "":
        endDate = time.strftime('%Y/%m/%d',time.localtime())
    if request.GET.get('today',None) != None:
        endDate = startDate
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
            resource = None
            try:
                resource = clct_resource.find_one({'_id':ObjectId(resourceId)}, {'channelId':1,'categoryId':1})
            except:
                pass
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


def index(request):
    return HttpResponseRedirect('/statistics2/categoryDetail?today=')


# 使用 statisticLog 标，进行二次统计，大大节约时间
def category(request):
    DICT = {}
    categoryList = getCategoryDetailList()
    DICT["startDate"],DICT["endDate"],t_start,t_end,startTime,endTime = getStartEndDateTime(request)

    '''初始化 矩阵(其实是字典)'''
    result = {}
    row = {}
    for one in categoryList:
        row[one['categoryId']] = {30000:0,30001:0,30002:0,30003:0,30004:0,30005:0,30006:0,30007:0,30008:0,30009:0,30010:0}
    t = t_start
    while t < t_end:
        date = time.strftime('%Y%m%d',time.localtime(t))
        result[date] = copy.deepcopy(row)
        t += 24*3600

    '''
    在线播放:      30010 获取地址失败， 30009 播放失败，  30008 播放成功
    手动下载:      30005 获取地址失败， 30001 下载失败，  30000 下载成功
    自动下载:      30004 获取地址失败， 30003 下载失败，  30002 下载成功
    本地播放:      30007 播放失败，  30006 播放成功
    '''
    spec = {'date':{'$gte':startTime, '$lte':endTime},"operationCode":{"$in":[30010, 30009, 30008,30005,30001,30000,30004,30003,30002,30007,30006]}}
    logs = list(clct_statisticsLog.find(spec,{'operationCode':1, 'date':1, 'resourceId':1, 'count':1}))
    print len(logs)

    print '初始化getChannelId'
    getChannelId,getCategorylId = CacheResources([one['resourceId'] for one in logs])

    print '开始统计'
    for i,log in enumerate(logs):
        #下载
        try:
            categoryId = getCategorylId(log['resourceId'])
            if log['operationCode'] not in result[log['date']][categoryId]:
                result[log['date']][categoryId][log['operationCode']] = 0
            result[log['date']][categoryId][log['operationCode']] += log['count']
        except:
            pass

    print '得到有序坐标行列'
    days = sorted(result.keys())
    categories = sorted(row.keys())

    sortedResult = [{"data":[result[day][category] for category in categories],"day":day,"date": '/'.join([day[:4],day[4:6],day[6:]]) } for day in days]

    categoryMap = {}
    for one in categoryList:
        categoryMap[one['categoryId']] = one
    DICT['days'] = days
    DICT['categories'] = categories
    DICT['categoryNames'] = [categoryMap[id]['categoryName'] for id in categories]
    DICT['sortedResult'] = sortedResult
    #DICT['sortedResultSegs'] = sortedResultSegs
    DICT['navPage'] = 'statistics'
    DICT['title'] = '分类统计'

    return render_to_response("statisticsCategory2.htm",DICT,context_instance=RequestContext(request))



def categoryDetail(request):
    DICT = {}
    categoryList = getCategoryDetailList()
    DICT["startDate"],DICT["endDate"],t_start,t_end,startTime,endTime = getStartEndDateTime(request)

    '''初始化 矩阵(其实是字典)'''
    result = {}
    for one in categoryList:
        result[one['categoryId']] = {}
        result[one['categoryId']] =  {30000:0,30001:0,30002:0,30003:0,30004:0,30005:0,30006:0,30007:0,30008:0,30009:0,30010:0}

    '''
    在线播放:      30010 获取地址失败， 30009 播放失败，  30008 播放成功
    手动下载:      30005 获取地址失败， 30001 下载失败，  30000 下载成功
    自动下载:      30004 获取地址失败， 30003 下载失败，  30002 下载成功
    本地播放:      30007 播放失败，  30006 播放成功
    GIF:          30012 加载成功，  30013 加载失败
    '''
    spec = {'date':{'$gte':startTime[:8], '$lt':endTime[:8]},"operationCode":{"$in":[30010, 30009, 30008,30005,30001,30000,30004,30003,30002,30007,30006]}}
    logs = list(clct_statisticsLog.find(spec,{'operationCode':1, 'date':1, 'resourceId':1, 'count':1}))
    print len(logs)

    print '初始化getChannelId'
    getChannelId,getCategorylId = CacheResources([one['resourceId'] for one in logs])

    print '开始统计'
    for i,log in enumerate(logs):
        #下载
        try:
            categoryId = getCategorylId(log['resourceId'])
            if log['operationCode'] not in result[categoryId]:
                result[categoryId][log['operationCode']] = 0
            result[categoryId][log['operationCode']] += log['count']
        except:
            pass

    print '得到有序坐标行列'
    categories = sorted(result.keys())

    categoryMap = {}
    for c in categoryList:
        categoryMap[c['categoryId']] = c

    sortedResult = [{"data":result[categoryId] ,"category": categoryMap[categoryId]} for categoryId in categories]

    #累加
    sumDict = {}
    for key in sortedResult[0]['data'].keys():
        sumDict[key] = sum([one['data'][key]  for one in sortedResult])


    categoryMap = {}
    for one in categoryList:
        categoryMap[one['categoryId']] = one
    DICT['categories'] = categories
    DICT['categoryNames'] = [categoryMap[id]['categoryName'] for id in categories]
    DICT['sortedResult'] = sortedResult
    DICT['sumDict'] = sumDict
    DICT['navPage'] = 'statistics'
    DICT['title'] = '分类统计'

    return render_to_response("statisticsCategory2Detail.htm",DICT,context_instance=RequestContext(request))


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
    spec['date'] = {'$gte':startTime, '$lte':endTime}

    '''
    在线播放:      30010 获取地址失败， 30009 播放失败，  30008 播放成功
    手动下载:      30005 获取地址失败， 30001 下载失败，  30000 下载成功
    自动下载:      30004 获取地址失败， 30003 下载失败，  30002 下载成功
    本地播放:      30007 播放失败，  30006 播放成功
    '''
    spec["operationCode"] = {"$in":[30008,30000]}

    #开始统计
    logs = list(clct_statisticsLog.find(spec,{'className':0, 'msg':0}))

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
        if log['operationCode'] in [30000]:
            result[channelId][0] += log['count']
        #播放
        if log['operationCode'] == 30008:
            result[channelId][1] += log['count']
        #总数
        result[channelId][2] += log['count']

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
    return render_to_response('statisticsChannel.htm',DICT,context_instance=RequestContext(request))


def search(request):
    DICT = {}

    DICT["startDate"],DICT["endDate"],t_start,t_end,startTime,endTime = getStartEndDateTime(request)
    limit = int(request.GET.get('limit',20))
    spec = {}
    spec['date'] = {'$gte':startTime[:8], '$lt':endTime[:8]}

    #读取channel列表
    mapScript = '''
    function()
    {
        if(this.createTime >= "%s" && this.createTime < "%s")
        emit(this.keyword,1);
    }
    '''%(startTime[:8],endTime[:8])
    reduceScript= '''
    function(key,values)
    {
        return values.length;
    }
    '''
    print (startTime[:8],endTime[:8])
    clct_searchStatistic = clct_searchLog.map_reduce(mapScript,reduceScript,"searchStatistics")
    print clct_searchStatistic
    L = list(clct_searchStatistic.find().sort([('value',-1)]).limit(limit))
    for one in L:
        one['id'] = one['_id']
    DICT['result'] = L
    DICT['limit'] = limit
    DICT['navPage'] = 'statistics'
    DICT['title'] = '频道下载/播放统计'
    return render_to_response('statisticsSearch.htm',DICT,context_instance=RequestContext(request))

def channelSub2(request):
    DICT = {}

    DICT["startDate"],DICT["endDate"],t_start,t_end,startTime,endTime = getStartEndDateTime(request)
    categoryName = request.GET.get('categoryName',"全部")
    limit = int(request.GET.get('limit',20))
    sort = request.GET.get('sort','increaseNum')

    spec = {}
    if categoryName != u"全部":
        filterCategoryId = getCategoryIdByName(categoryName)
    else:
        filterCategoryId = None
    print 'filterCategoryId:',filterCategoryId
    spec['date'] = {'$gte':startTime[:8], '$lt':endTime[:8]}

    #开始统计
    logs = list(clct_subscribeLog.find(spec))
    #读取channel列表
    channelList = list(clct_channel.find({'channelId':{'$in':list(set([log['channelId'] for log in logs]))}},
                       {'channelId':1,'channelType':1,'channelName':1}))
    channelMap = {}
    for channel in channelList:
        channelMap[channel['channelId']] = channel


    print '开始统计'
    result = {}
    '''
        {
            channelId:(首次订阅数,FEED订阅数,详情订阅数,未知订阅数,总订阅数,取消订阅数,净增加订阅数)
        }
    '''
    for log in logs:
        #过滤不要的类别
        if filterCategoryId:
            if log['channelId'] not in channelMap:
                continue
            if channelMap[log['channelId']]['channelType'] != filterCategoryId:
                continue
        if log['channelId'] not in result:
            result[log['channelId']] = [0,0,0,0,0,0,0]
        if log['action'] == 'unsub':
            result[log['channelId']][5] += log['number']
            result[log['channelId']][6] -= log['number']
        else:
            if log['from'] == 'first':
                result[log['channelId']][0] += log['number']
            elif log['from'] == 'feed':
                result[log['channelId']][1] += log['number']
            elif log['from'] == 'channelDetail':
                result[log['channelId']][2] += log['number']
            else:
                result[log['channelId']][3] += log['number']
            result[log['channelId']][4] += log['number']
            result[log['channelId']][6] += log['number']


    #将结果转化成 数组
    L = []
    for key in result:
        item = {}
        item['channelId'] = key
        item['data'] = result[key]
        L.append(item)
    #排序
    if sort == 'subNum':
        L.sort(key=lambda a:a['data'][4], reverse=True)
    elif sort == 'unsubNum':
        L.sort(key=lambda a:a['data'][5], reverse=True)
    elif sort == 'increaseNum':
        L.sort(key=lambda a:a['data'][6], reverse=True)
    elif sort == 'otherSubNum':
        L.sort(key=lambda a:a['data'][3], reverse=True)

    L = L[:limit]
    for one in L:
        channel = clct_channel.find_one({'channelId':one['channelId']})
        if not channel:
            print 'channelId not exists:',one['channelId']
            continue
        one['categoryName'] = getCategoryNameById(channel['channelType'])
        one['channelName'] = channel['channelName']

    DICT['result'] = L
    DICT['sort'] = sort
    DICT['limit'] = limit
    DICT['categoryList'] = [u'全部'] + getCategoryList()
    DICT['categoryName'] = categoryName
    DICT['navPage'] = 'statistics'
    DICT['title'] = '频道下载/播放统计'
    return render_to_response('statisticsChannelSub2.htm',DICT,context_instance=RequestContext(request))



def channelSub(request):
    DICT = {}
    categoryName = request.GET.get('categoryName',"全部")
    limit = int(request.GET.get('limit',20))
    mongo = request.GET.get('mongo','')
    spec = {}
    if categoryName != u"全部":
        spec['channelType'] = getCategoryIdByName(categoryName)
    if mongo:
        spec.update(json.loads(mongo))

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
    return render_to_response('statisticsChannelSub.htm',DICT,context_instance=RequestContext(request))


def autoResource(request):
    DICT = {}

    DICT["startDate"],DICT["endDate"],t_start,t_end,startTime,endTime = getStartEndDateTime(request)
    spec = {}
    spec['createTime'] = {'$gte':startTime, '$lte':endTime}
    #10011 自动下载启动  10101 自动下载成功
    spec["operationCode"] = {"$in":[10011, 10101]}

    result = {}
    #初始化 result
    t = t_start
    while t < t_end:
        date = time.strftime('%Y%m%d',time.localtime(t))
        result[date] = {"startNum":0,"sucNum":0}
        t += 24*3600
    #开始统计
    logs = list(clct_operationLog.find(spec,{'className':0, 'msg':0}))
    for log in logs:
        date = log['createTime'][:8]
        if log['operationCode'] == 10011:
            result[date]['startNum'] += 1
        elif log['operationCode'] == 10101:
            result[date]['sucNum'] += 1

    #转换结果到数组
    L = result.items()
    L.sort(key=lambda a:a[0])

    '''
        [
            (date,{'startNum':0,'sucNum':0}),
            ...
        ]
    '''
    DICT['result'] = L

    return render_to_response('statisticsAutoResource.htm',DICT,context_instance=RequestContext(request))

def resource(request):
    DICT = {}

    DICT["startDate"],DICT["endDate"],t_start,t_end,startTime,endTime = getStartEndDateTime(request)
    categoryName = request.GET.get('categoryName',"全部")
    channelId = request.GET.get('channelId',"")
    limit = int(request.GET.get('limit',20))
    sort = request.GET.get('sort','downplayNum')

    DICT['channelId'] = channelId

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
    spec['date'] = {'$gte':startTime, '$lte':endTime}
    #10001 手动下载成功  10004 播放成功
    spec["operationCode"] = {"$in":[30000,30008]}


    #开始统计
    logs = list(clct_statisticsLog.find(spec,{'className':0, 'msg':0}))

    print '初始化getChannelId'
    getChannelId,getCategoryId = CacheResources([one['resourceId'] for one in logs])

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
        categoryId = getCategoryId(resourceId)
        if filterCategoryId and filterCategoryId != categoryId:
            continue 
        channelId = getChannelId(resourceId)
        if filterChannelId and  filterChannelId != channelId:
            continue

        if resourceId not in result:
            result[resourceId] = [0,0,0]
        #下载
        if log['operationCode'] == 30000:
            result[resourceId][0] += log['count']
        #播放
        if log['operationCode'] == 30008:
            result[resourceId][1] += log['count']
        #总数
        result[resourceId][2] += log['count']

    #将结果转化成 数组
    L = []
    for key in result:
        item = {}
        if key == 'default':
            continue
        item['resourceId'] = key
        item['channelId'] = getChannelId(key)
        item['categoryId'] = getCategoryId(key)
        if item['categoryId'] == None or item['channelId'] == None:
            continue
        item['categoryName'] = getCategoryNameById(item['categoryId'])
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
            one['channelName'] = 'channel deleted'
        else:
            one['channelName'] = channel['channelName']

        resource = clct_resource.find_one({'_id':ObjectId(one['resourceId'])})
        if not resource:
            one['resourceName'] = "deleted resource"
        else:
            one['resourceName'] =  resource['resourceName']
        


    DICT['result'] = L
    DICT['categoryList'] = [u'全部'] + getCategoryList()
    DICT['categoryName'] = categoryName

    DICT['sort'] = sort
    DICT['limit'] = limit
    DICT['navPage'] = 'statistics'
    DICT['title'] = '视频 下载/播放统计'
    return render_to_response('statisticsResource.htm',DICT,context_instance=RequestContext(request))


def weiboUser(request):
    DICT = {"data":[]}

    weiboUsers = list(clct_user.find({'sinaId':{'$ne':''}},{"sinaId":1,"name":1}))

    DICT['data'] = list(weiboUsers)
    DICT['number'] = len(weiboUsers)

    return render_to_response("statisticsWeiboUser.htm",DICT,context_instance=RequestContext(request))



def playTime(request):
    day7 = time.strftime('%Y%m%d000000',time.localtime(time.time()-7*24*3600))
    day = time.strftime('%Y%m%d%H%M%S',time.localtime())

    logs = clct_playLog.find({'operationTime':{'$gte':day7,'$lte':day}},{'operationTime':1,'playTime':1})
    R = {}
    for log in logs:
        t = log['operationTime'][:8]
        if t not in R:
            R[t] = float(log['playTime'])/1000/3600
        else:
            R[t] += float(log['playTime'])/1000/3600
    for key in R:
        R[key] = int(R[key])
    result =  sorted(R.items(),key=lambda a:a[0],reverse=True)
    DICT = {'result':result}
    return render_to_response("statisticsPlayTime.htm",DICT,context_instance=RequestContext(request))