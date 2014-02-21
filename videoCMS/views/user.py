from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from videoCMS.conf import *
from login import NeedLogin
import time,collections,json
from statistics2 import  getDaySequence


def staticResourceByUid(uid,days=7):
    t_start = time.time()- 7*24*3600
    t_end = time.time()
    startDate = time.strftime('%Y%m%d',time.localtime(t_start))
    endDate = time.strftime('%Y%m%d',time.localtime(t_end))
    resourceList = clct_resource.find({'editor':uid,'createTime':{'$gte':startDate,'$lte':endDate}},{'_id':1})
    resourceSet = set([str(one['_id']) for one in resourceList])

    print startDate,endDate
    logs = [one for one in clct_statisticsLog.find({'date':{'$gte':startDate, '$lte':endDate,}, "operationCode":{"$in":[30008,30000]}})]

    result = {}
    for log in logs:
        if log['resourceId'] not in resourceSet:
            continue
        if log['date'] not in result:
            result[log['date']] = [0,0]
        if log['operationCode'] == 30000:
            result[log['date']][0] += log['count']
        elif log['operationCode'] == 30008:
            result[log['date']][1] += log['count']


    daySequence = getDaySequence(t_start,t_end)
    s = []
    for day in daySequence:
        s.append(result.get(day,[0,0]))

    print s,daySequence,result
    return daySequence,s


@NeedLogin
def index(request):
    DICT = {}
    DICT['info'] = ''

    uid = int(request.GET.get('id',-1))
    if uid == -1: uid = request.session['id']
    editor = clct_cmsEditor.find_one({'id':uid})
    DICT.update(editor)

    resourceList = clct_resource.find({'editor':uid})

    DICT['resourceNum'] = resourceList.count()
    DICT['resourceList'] = []
    DICT['uid'] = uid
    for one in clct_resource.find({'editor':uid}).sort([('_id',-1)]).limit(10):
        one['id'] =str(one['_id'])
        DICT['resourceList'].append(one)

    daySequeue,statistics = staticResourceByUid(uid,7)

    DICT['daySequeue'] = json.dumps(daySequeue)
    DICT['statistics'] = json.dumps(map(list,zip(*statistics)))

    print DICT['statistics']
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