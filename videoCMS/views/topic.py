#coding=utf8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import json,StringIO,re
from videoCMS.conf import *
from bson import ObjectId
from videoCMS.common.Domain import Topic
from videoCMS.common.common import Obj2Str,getCurTime,antiFormatHumanTime,formatHumanTime
from videoCMS.common.HttpUtil import HttpUtil
from videoCMS.common.ImageUtil import imgconvert
from videoCMS.common.db import getCategoryList
#from videoCMS.views.channel import saveResourceImage
from videoSearch.common.videoInfoTask import addVideoInfoTask
import urllib2
from videoCMS.common.db import getCategoryNameById,getCategoryIdByName,getCategoryList,getCategoryIdMapName
from videoCMS.views.login import *
from videoCMS.common.anquanbao import PrefetchCache,GetProgress
from login import NeedLogin


@NeedLogin
def index(request):
    spec = {}
    DICT = {}

    page = int(request.GET['page']) if request.GET.get('page','') != '' else 1
    limit =int(request.GET['len']) if request.GET.get('len','') != '' else 10
    
    name = request.GET.get('name','')
    mongo = request.GET.get('mongo','')
    isOnline = request.GET.get('isOnline','all')
    id = request.GET.get('id','')
    skip = limit * (page - 1)
    sort = request.GET.get('sort','createTime')
    
    if id != '':
        spec['_id'] = ObjectId(id)
    elif name != '':
        spec['title'] = re.compile(name)

    if isOnline == 'true':
        spec['isOnline'] = True
    elif isOnline == 'false':
        spec['isOnline'] = False
    if mongo != '':
        spec.update(json.loads(mongo))

    if sort == '':
        sort = 'createTime'
    if sort == 'weight':
        sortParams = [('weight',-1),('number',-1),('createTime',-1)]
    elif sort == 'createTime':
        sortParams = [('createTime',-1)]
    elif sort == 'updateTime':
        sortParams = [('updateTime',-1)]

        

    topicList = list(clct_topic.find(spec).sort(sortParams).skip(skip).limit(limit))
    for one in topicList:
        one['id'] = str(one['_id'])
        one['imageUrl'] = IMG_INTERFACE_FF%(96,96,one['picture'])
        one['createTime'] = formatHumanTime(one['createTime'])
        one['updateTime'] = formatHumanTime(one['updateTime'])
        one['scheduleGoOnline'] = formatHumanTime(one['scheduleGoOnline'])



    DICT['nextPage'] = page + 1
    DICT['prePage'] = page-1 if page>1 else 1
    DICT['findNum'] = clct_topic.find(spec).count()
    DICT['navPage'] = 'topic'
    DICT['typeList'] = [u'全部'] + getCategoryList()
    DICT.update(locals())

    return render_to_response('topicList.htm',DICT,context_instance=RequestContext(request))


def POST2Topic(request):
    ret = Topic()
    ret['title'] = request.POST.get('title','')
    ret['weight'] = int(request.POST.get('weight',0))
    ret['description'] = request.POST.get('description','')
    ret['isOnline'] = True if request.POST.get('isOnline') == u'是' else False
    ret['isIOS'] = True if request.POST.get('isIOS') == u'是' else False
    ret['content'] = json.loads(request.POST.get('content'))
    ret['scheduleGoOnline'] = antiFormatHumanTime(request.POST.get('scheduleGoOnline',''))

    return ret

@NeedLogin
def update(request):
    id = request.GET.get('id','')
    if request.method == "GET":
        topic = clct_topic.find_one({'_id':ObjectId(id)})
        DICT = Obj2Str(topic)
        DICT['info'] = ''
        DICT['update'] = True
        DICT['navPage'] = 'topic'
        DICT['imageUrl'] = IMG_INTERFACE_FF%(250,150,topic['picture'])

        content = []
        for item in topic['content']:
            if item['type'] == 'resource':
                resource = clct_resource.find_one({'_id':ObjectId(item['resourceId'])})
                resource['type'] = 'resource'
                content.append(resource)
            elif item['type'] == 'channel':
                channel = clct_channel.find_one({'channelId':item['channelId']})
                channel['type'] = 'channel'
                content.append(channel)
        for item in content:
            item['id'] = str(item['_id'])
            item.pop('_id')
        DICT['content'] = json.dumps(content)

        return render_to_response('topicUpdate.htm',DICT,context_instance=RequestContext(request))
    
    #更新
    topic = POST2Topic(request)
    topic['modifyTime'] = getCurTime()


        
    img = request.FILES.get('picture',None)
    if img:
        topic['picture'] = saveTopicImage(img.read(),id)
    
    
    clct_topic.update({'_id':ObjectId(id)},{'$set':topic.getUpdateDict()})

    addScheduleGoOnline(id,topic['scheduleGoOnline'])

    return HttpResponseRedirect('update?id='+id)


@NeedLogin
def add(request):
    if request.method == "GET":
        DICT = {}
        DICT['info'] = ''
        DICT['navPage'] = 'topic'
        return render_to_response('topicUpdate.htm',DICT,context_instance=RequestContext(request))
    
    topic = POST2Topic(request)
    now = getCurTime()
    topic['createTime'] = now
    topic['modifyTime'] = now
    topic['updateTime'] = now

    if topic['title'] == '':raise Exception('专题名 不能为空')

    
    id = clct_topic.insert(topic.getInsertDict())
    id = str(id)
    img = request.FILES.get('picture',None)
    if img:
        filename = saveTopicImage(img.read(),id)
        clct_resource.update({'_id':ObjectId(id)},{'$set':{'picture':filename}})

    addScheduleGoOnline(id,topic['scheduleGoOnline'])

    return HttpResponseRedirect('update?id='+id)


def saveTopicImage(img, id):
    filename = 'videoCMS/topic/%s.jpg'%(id + getCurTime())
    with open(IMAGE_DIR + '/' + filename, 'wb') as f:
        f.write(img)
    return filename.replace('/', '_')


def showJson(request):
    id = request.GET.get('id')
    one = clct_topic.find_one({'_id':ObjectId(id)})
    one['_id'] = str(one['_id'])
    return HttpResponse(json.dumps(one))


def addResourceToNewestBaBa(request):
    resourceId = request.GET.get('resourceId')
    topic = list(clct_topic.find({'isIOS':True}).sort([('updateTime',-1)]).limit(1))[0]
    item = {"resourceId": resourceId,"type": "resource"}
    print clct_topic.update({'_id':topic['_id']},{'$push':{'content':item}})
    return HttpResponse('已经添加至 '+topic['title'])


def addScheduleGoOnline(topicId,cronTime):
    if cronTime == '' or cronTime < getCurTime():
        return
    if clct_cronJob.find_one({'type':'BaBaGoOnline','topicId':topicId}) == None:
        clct_cronJob.insert({'type':'BaBaGoOnline','topicId':topicId,'cronTime':cronTime})
    else:
        clct_cronJob.update({'type':'BaBaGoOnline','topicId':topicId},{'$set':{'cronTime':cronTime}})


#==============================================================
@NeedLogin
def toggleOnlineStatus(request):
    ret = {}
    id = ObjectId(request.GET.get('id'))
    topic = clct_topic.find_one({'_id':id})

    if topic['isOnline'] == True:
        clct_topic.update({'_id':id},{'$set':{'isOnline':False,'modifyTime':getCurTime()}})
    else:
        up = {'isOnline':True,'modifyTime':getCurTime()}
        if topic['updateTime'] == '00000000000000':
            up['updateTime'] = getCurTime()
        clct_topic.update({'_id':id},{'$set':up})
    ret['status'] = not topic['isOnline']
    return HttpResponse(json.dumps(ret))