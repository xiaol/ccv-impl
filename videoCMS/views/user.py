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

    resourceList = clct_resource.find({'$or':[{'editor':uid},{'channelId':{'$in':channelIdList}}],'createTime':{'$gte':startTime,'$lt':endTime}},{'_id':1})
    resourceSet = set([str(one['_id']) for one in resourceList])

    print startTime,endTime
    logs = [one for one in clct_statisticsLog.find({'date':{'$gte':startTime[:8], '$lt':endTime[:8],}, "operationCode":{"$in":[30008,30000]}})]

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
    resultSum = {}
    '''
    {
        '20140101':[0,0],
        '20140102':[0,0]
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
                result[log['channelId']][log['date']] = [0,0]
            if log['operationCode'] == 30000:
                result[log['channelId']][log['date']][0] += log['count']
            elif log['operationCode'] == 30008:
                result[log['channelId']][log['date']][1] += log['count']

        #合计统计
        if log['date'] not in resultSum:
            resultSum[log['date']] = [0,0]
        if log['operationCode'] == 30000:
            resultSum[log['date']][0] += log['count']
        elif log['operationCode'] == 30008:
            resultSum[log['date']][1] += log['count']


    daySequence = getDaySequence(t_start,t_end)
    s_sum = []
    for day in daySequence:
        s_sum.append(resultSum.get(day,[0,0]))
    #从 [[1,1],[2,2],[3,3]] 转换为 [[1,2,3],[1,2,3]]
    s_sum = map(list,zip(*s_sum))

    s_channel = {}
    for channel in result:
        s_channel[channel] = {}
        data = []
        for day in daySequence:
            data.append(result[channel].get(day,[0,0]))
        #从 [[1,1],[2,2],[3,3]] 转换为 [[1,2,3],[1,2,3]]
        data = map(list,zip(*data))
        s_channel[channel]['data'] = data
        s_channel[channel]['download'] = sum(data[0])
        s_channel[channel]['play'] = sum(data[1])


    #print daySequence
    #print s_sum
    #print s_channel
    #print channelList
    return daySequence,s_sum,s_channel,channelList,len(resourceSet)


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

    #手工添加的视频
    resourceList = clct_resource.find({'editor':uid,'source':'manual'})
    DICT['resourceNum'] = resourceList.count()
    DICT['resourceList'] = []
    DICT['uid'] = uid
    for one in resourceList.sort([('_id',-1)]).limit(10):
        one['id'] =str(one['_id'])
        DICT['resourceList'].append(one)
    #选择日期内 手工视频
    DICT['periodResourceNum'] =clct_resource.find({'editor':uid,'source':'manual','createTime':{'$gte':startTime,'$lt':endTime}}).count()
    #今日昨日视频数
    yesterdayStart = time.strftime("%Y%m%d000000",time.localtime(time.time()-24*3600))
    todayStart= time.strftime("%Y%m%d000000",time.localtime(time.time()))
    todayEnd= time.strftime("%Y%m%d000000",time.localtime(time.time()+24*3600))
    #print yesterdayStart,todayStart,todayEnd

    DICT['yesterdayResourceNum'] =clct_resource.find({'editor':uid,'source':'manual','createTime':{'$gte':yesterdayStart,'$lt':todayStart}}).count()
    DICT['todayResourceNum'] =clct_resource.find({'editor':uid,'source':'manual','createTime':{'$gte':todayStart,'$lt':todayEnd}}).count()
    #统计数据

    labels,s_sum,s_channel,channelList,newNum = staticByUid(uid,t_start,t_end,startTime,endTime,timespan)

    DICT['labels'] = json.dumps(labels)
    DICT['s_sum'] = json.dumps(s_sum)
    DICT['s_channel'] = json.dumps(s_channel)
    DICT['channelList'] = channelList
    DICT['channelListStr'] = json.dumps(channelList)
    DICT['newNum'] = newNum
    DICT['averagePlay'] =  round(sum(s_sum[1]) *1.0/ newNum,2) if newNum else 0
    DICT['uid'] = uid
    #print DICT
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