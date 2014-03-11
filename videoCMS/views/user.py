#coding=utf-8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from videoCMS.conf import *
from login import NeedLogin
import time,collections,json
from statistics2 import  getDaySequence,getStartEndDateTime






def staticByUid(uid,t_start,t_end,startTime,endTime,timespan):

    channelList = list(clct_channel.find({'editor':uid},{'_id':0,'channelId':1,'channelName':1}))
    channelIdList = [one['channelId'] for one in channelList]

    fieldMap = {'_id':1,'updateTime':1,'source':1,'channelId':1}

    #注意 这里所有的视频都是 属于此uid的，其他作者的不做统计
    resourceList = list(clct_resource.find({'editor':uid,'updateTime':{'$gte':startTime,'$lt':endTime}},fieldMap))
    resourceSet = set([str(one['_id']) for one in resourceList])
    resourceManualList = list(clct_resource.find({'editor':uid,'source':'manual','updateTime':{'$gte':startTime,'$lt':endTime}},fieldMap))
    resourceManualSet = set([str(one['_id']) for one in resourceManualList])
    resourceSpiderList = list(clct_resource.find({'editor':uid,'source':'spider','updateTime':{'$gte':startTime,'$lt':endTime}},fieldMap))
    resourceSpiderSet = set([str(one['_id']) for one in resourceSpiderList])


    '''===================== 原始统计 ===================='''
    print startTime,endTime
    '''30000 下载  30008 播放
    '''
    fieldMap = {'_id':0}
    logs = [one for one in clct_statisticsLog.find(\
        {'date':{'$gte':startTime[:8], '$lt':endTime[:8],}, "operationCode":{"$in":[30008,30000]}},fieldMap)]

    result = {}
    '''
    {
        10010:
        {
            '20140101':[0,0],
            '20140102':[0,0]
        }
    }
    '''

    #为 编辑负责的频道创建默认的统计数据
    for channelId in channelIdList:
        result[channelId] = {}
    #统计日志
    for log in logs:
        if log['resourceId'] not in resourceSet:
            continue
        #按频道统计
        if 'channelId' in log:
            if log['channelId'] not in result:
                result[log['channelId']] = {}
            if log['date'] not in result[log['channelId']]:
                result[log['channelId']][log['date']] = [0,0,0,0]  # [下载(人工)，下载(爬虫)，播放(人工), 播放(爬虫)]
            if log['operationCode'] == 30000:
                if log['resourceId'] in resourceManualSet:
                    result[log['channelId']][log['date']][0] += log['count']
                elif log['resourceId'] in resourceSpiderSet:
                    result[log['channelId']][log['date']][1] += log['count']
            elif log['operationCode'] == 30008:
                if log['resourceId'] in resourceManualSet:
                    result[log['channelId']][log['date']][2] += log['count']
                elif log['resourceId'] in resourceSpiderSet:
                    result[log['channelId']][log['date']][3] += log['count']


    '''===================== 下载/播放 合计统计 ===================='''
    #获取日期序列
    daySequence = getDaySequence(t_start,t_end)
    # 合计统计
    resultSum = {}
    '''
    {
        '20140101':[0,0,0,0],
        '20140102':[0,0,0,0]
    }
    '''
    for day in daySequence:
        resultSum[day]=[0,0,0,0]
    for channelResult in result.values():
        for day in channelResult:
            resultSum[day] = map(lambda a,b:a+b ,resultSum[day],channelResult[day])

    #按照日期排序，并且转置,[[下载(人工)第1天,下载(人工)第2天],[下载(爬虫)第1天,下载(爬虫)第2天],[...],[...]]
    s_sum = [item[1] for item in sorted(resultSum.items(),key=lambda a:a[0])]
    s_sum = map(list,zip(*s_sum))

    ''' ========= 按频道内 统计 =============== '''
    s_channel = {}
    for channel in result:
        s_channel[channel] = {}
        data = []
        for day in daySequence:
            data.append(result[channel].get(day,[0,0,0,0]))
        #从 [[1,1],[2,2],[3,3]] 转换为 [[1,2,3],[1,2,3]]
        data = map(list,zip(*data))
        s_channel[channel]['data'] = data
        s_channel[channel]['sum'] = map(sum,data)
        s_channel[channel]['download'] = sum(data[0]) + sum(data[1])
        s_channel[channel]['play'] = sum(data[2]) + sum(data[3])
        s_channel[channel]['resourceManualNum'] = 0
        s_channel[channel]['resourceSpiderNum'] = 0



    '''===================== 统计视频增量 ====================='''
    createSum = {}
    for day in daySequence:
        createSum[day] = [0,0] # [人工增加数量, 爬虫增加数量]
    for resource in resourceList:
        day = resource['updateTime'][:8]
        if resource['source'] == 'manual':
            createSum[day][0] += 1
            s_channel[resource['channelId']]['resourceManualNum'] += 1
        elif resource['source'] == 'spider':
            createSum[day][1] += 1
            s_channel[resource['channelId']]['resourceSpiderNum'] += 1
    s_create_sum = [item[1] for item in sorted(createSum.items(),key=lambda a:a[0])]
    s_create_sum = map(list,zip(*s_create_sum))


    '''===========  合并频道统计到 channelList  =========='''
    for channel in channelList:
        channelId = channel['channelId']
        s_channel[channelId]['newNum'] = s_channel[channelId]['resourceManualNum'] + s_channel[channelId]['resourceSpiderNum']
        channel.update(s_channel[channelId])

    if timespan != 1:
        pass

    return daySequence,s_sum,channelList,s_create_sum,len(resourceManualSet),len(resourceSpiderSet),len(resourceSet)





@NeedLogin
def index(request):
    DICT = {}
    DICT['info'] = ''
    DICT["startDate"],DICT["endDate"],t_start,t_end,startTime,endTime = getStartEndDateTime(request)
    uid = int(request.GET.get('id',-1))
    DICT['timespan'] = request.GET.get('timespan',u'天')
    if DICT['timespan']  == u'天':
        timespan = 24*3600
    elif DICT['timespan']  == u'周':
        timespan = 7*24*3600



    if uid == -1: uid = request.session['id']
    editor = clct_cmsEditor.find_one({'id':uid})
    DICT.update(editor)

    #统计数据

    labels,s_sum,channelList,s_create_sum,newManualNum,newSpiderNum,newNum = staticByUid(uid,t_start,t_end,startTime,endTime,timespan)

    #====  通用数据
    DICT['uid'] = uid
    DICT['labels'] = json.dumps(labels) # 日期序列


    #======= 新增视频 合计统计  =============
    DICT['newNum'] = newNum #新增视频数量
    DICT['newManualNum'] = newManualNum #新增人工视频数量
    DICT['newSpiderNum'] = newSpiderNum #新增爬虫视频数量
    DICT['s_create_sum'] = s_create_sum #新增视频详细统计

    #======= 下载/播放 合计统计  =============
    DICT['s_sum'] = json.dumps(s_sum)   # 下载播放合计统计 [[下载(人工)...],[下载(爬虫)...],[播放(人工)...],[播放(爬虫)...]]
    #临时变量
    _s0=sum(s_sum[0]); _s1=sum(s_sum[1]); _s2=sum(s_sum[2]); _s3=sum(s_sum[3])
    # [下载合计，下载合计(人工),下载合计(爬虫),播放合计，播放合计(人工), 播放(爬虫)合计]
    DICT['sumNum'] = [_s0+_s1, _s0, _s1, _s2+_s3, _s2, _s3 ]
    # [平均下载(合计)，平均下载(人工),平均下载(爬虫) ,平均播放(合计), 平均播放(人工), 平均播放(爬虫)]
    DICT['sumNumAverage'] = [(_s0+_s1)/max(newNum*1.0,1.0), _s0/max(newManualNum*1.0,1.0), _s1/max(newSpiderNum*1.0,1.0), \
                             (_s2+_s3)/max(newNum*1.0,1.0), _s2/max(newManualNum*1.0,1.0), _s3/max(newSpiderNum*1.0,1.0) ]

    DICT['sumNumAverage'] = map(round,DICT['sumNumAverage'],[1]*6)

    #======== 分频道统计===========
    DICT['channelList'] = channelList # 分频道统计
    DICT['channelListStr'] = json.dumps(channelList) # 频道列表


    print DICT
    return render_to_response('userIndex.htm',DICT,context_instance=RequestContext(request))


@NeedLogin
def edit(request):
    DICT = {}
    DICT['info'] = ''

    uid = int(request.GET.get('id',-1))
    if uid == -1: uid = request.session['id']
    editor = clct_cmsEditor.find_one({'id':uid})
    DICT.update(editor)

    print DICT

    return render_to_response('userEdit.htm',DICT,context_instance=RequestContext(request))


@NeedLogin
def add(request):
    DICT = {}
    DICT['info'] = ''

    if request.method == 'GET':
        return render_to_response('userIndex.htm',DICT,context_instance=RequestContext(request))


    return HttpResponseRedirect('/user/index?id=')



@NeedLogin
def list_(request):
    DICT = {}
    DICT['info'] = ''
    userList = clct_cmsEditor.find()
    DICT['userList'] = userList

    return render_to_response('userList.htm',DICT,context_instance=RequestContext(request))