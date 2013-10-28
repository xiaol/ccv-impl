#coding=utf8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
import json,StringIO,re
from videoCMS.conf import clct_resource,clct_channel,clct_tag,IMAGE_DIR,IMG_INTERFACE,IMG_INTERFACE_FF,clct_cdnSync
from videoCMS.conf import CHANNEL_IMAGE_WIDTH,CHANNEL_IMAGE_HEIGHT,clct_videoInfoTask
from bson import ObjectId
from videoCMS.common.Domain import Resource,Tag,CDNSyncTask
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

def getSkipLimit(DICT,skip=0,limit=10):
    _skip = DICT.get('skip',skip)
    _limit = DICT.get('limit',limit)
    return _skip,_limit

def createTag(name,refNum=0):
    tag = Tag()
    tag['name'] = name
    tag['createTime'] = getCurTime()
    tag['modifyTime'] = getCurTime()
    tag['refNum'] = refNum
    print tag.getInsertDict()
    clct_tag.insert(tag.getInsertDict())


def addTagRef(name,addNum):
    clct_tag.update({'name':name},{'$inc':{'refNum':1}})

@NeedLogin
def index(request):
    spec = {}
    DICT = {}
    
    if checkLogin(request):
        DICT['username'] = request.session['username']
        
    
    page = int(request.GET['page']) if request.GET.get('page','') != '' else 1
    limit =int(request.GET['len']) if request.GET.get('len','') != '' else 10
    
    name = request.GET.get('name','')
    mongo = request.GET.get('mongo','')
    id = request.GET.get('id','')
    channelId = request.GET.get('channelId','')
    videoType = request.GET.get('videoType','')
    videoId = request.GET.get('videoId','')
    skip = limit * (page - 1)
    channelType = request.GET.get('channelType','')
    startTime = request.GET.get('startTime','')
    endTime = request.GET.get('endTime','')
    sort = request.GET.get('sort','createTime')
    
    if id != '':
        spec['_id'] = ObjectId(id)
    elif name != '':
        spec['resourceName'] = re.compile(name)
    elif channelId != '':
        spec['channelId'] = int(channelId)
        DICT['title'] = clct_channel.find_one(spec)['channelName']
        print DICT['title']
    elif videoType != '':
        spec['videoType'] = videoType
    elif videoId != '':
        spec['videoId'] = videoId


    if channelType != '' and channelType != u'全部':
        spec['categoryId'] = getCategoryIdByName(channelType)
        pass
    if startTime != '':
        spec['createTime'] = {"$gte":startTime}
    if endTime != '':
        if 'createTime' not in spec:
            spec['createTime'] = {}
        spec['createTime'].update({"$lte":endTime})
    if mongo != '':
        spec.update(json.loads(mongo))

    if sort == '':
        sort = 'createTime'
    if sort == 'weight':
        sortParams = [('weight',-1),('number',-1),('createTime',-1)]
    elif sort == 'createTime':
        sortParams = [('createTime',-1)]
    elif sort == 'playNumber':
        sortParams = [('playNumber',-1)]
    elif sort == 'downloadNumber':
        sortParams = [('downloadNumber',-1)]
    elif sort == 'invalidTime':
        sortParams = [('validTime',-1)]
        

    resourceList = list(clct_resource.find(spec).sort(sortParams).skip(skip).limit(limit))
    for one in resourceList:
        one['id'] = str(one['_id'])
        one.pop('_id')
        one['resourceImageUrl'] = IMG_INTERFACE_FF%(96,96,one['resourceImageUrl'])
        channel = clct_channel.find_one({'channelId':one['channelId']})
        if channel == None:
            one['channelName'] = "not found channel:"+str(one['channelId'])
        else:
            one['channelName'] = channel['channelName']
        one['createTime'] = formatHumanTime(one['createTime'])
        one['updateTime'] = formatHumanTime(one['updateTime'])
        one['scheduleGoOnline'] = formatHumanTime(one['scheduleGoOnline'])

    DICT['resourceList'] = resourceList
    
    DICT['page'] = page
    DICT['len'] = limit
    DICT['nextPage'] = page + 1
    DICT['prePage'] = page-1 if page>1 else 1
    DICT['name'] = name
    DICT['id'] = id
    DICT['channelId'] = channelId
    DICT['videoType'] = videoType
    DICT['videoId'] = videoId

    DICT['mongo'] = mongo
    DICT['findNum'] = clct_resource.find(spec).count()
    DICT['navPage'] = 'resource'
    DICT['typeList'] = [u'全部'] + getCategoryList()
    DICT['channelType'] = channelType
    DICT['sort'] = sort
    DICT['startTime'] = startTime
    DICT['endTime'] = endTime
    
    return render_to_response('resourceList.htm',DICT)


def POST2Resource(request):
    resource  = Resource()
    resource['videoId'] = request.POST.get('videoId').strip()
    resource['videoType'] = request.POST.get('videoType').strip()
    resource['resourceName'] = request.POST.get('resourceName')
    resource['channelId'] = int(request.POST.get('channelId'))
    resource['weight'] = float(request.POST.get('weight'))
    channel = clct_channel.find_one({'channelId':resource['channelId']})
    resource['categoryId'] = channel['channelType']
    resource['duration'] = int(-1 if request.POST.get('duration') == '' else request.POST.get('duration'))
    resource['resourceSize'] = -1 if request.POST.get('resourceSize') == '' else int(request.POST.get('resourceSize'))
    resource['isOnline'] = True if request.POST.get('isOnline') == u'是' else False
    resource['tagList'] = map(lambda a:a.strip(),request.POST.get('tagList').split(','))

    resource['scheduleGoOnline'] = antiFormatHumanTime(request.POST.get('scheduleGoOnline',''))
    resource['number'] = request.POST.get('number')
    resource['resourceUrl'] = request.POST.get('resourceUrl')
    resource['subtitle'] = request.POST.get('subtitle')
    resource['isLD'] = request.POST.get('isLD')
    resource['updateTime'] = request.POST.get('updateTime')

    try:
        resource['number'] = int(resource['number'])
    except:
        pass

    return resource

@NeedLogin
def update(request):
    id = request.GET.get('id','')
    if request.method == "GET":
        resource = clct_resource.find_one({'_id':ObjectId(id)})
        resource['tagList'] = ','.join(resource.get('tagList',[]))
        resource['resourceImageUrl'] = IMG_INTERFACE_FF%(250,150,resource['resourceImageUrl'])
        resource['scheduleGoOnline'] = formatHumanTime(resource['scheduleGoOnline'])
        DICT = Obj2Str(resource)
        DICT['username'] = request.session['username']
        DICT['info'] = ''
        DICT['update'] = True
        DICT['navPage'] = 'resource'
        channel = clct_channel.find_one({'channelId':resource['channelId']})
        if channel != None:
            DICT['channelName'] = channel['channelName']
            DICT['channelObId'] = str(channel['_id'])
        else:
            DICT['channelName'] = '频道不存在'
        return render_to_response('resourceUpdate.htm',DICT)
    
    #更新
    resource = POST2Resource(request)
    resource['modifyTime'] = getCurTime()
        
    img = request.FILES.get('resourceImage',None)
    if img:
        resource['resourceImageUrl'] = saveResourceImage(img.read(),id)
    
    
    clct_resource.update({'_id':ObjectId(id)},{'$set':resource.getUpdateDict()})
    return HttpResponseRedirect('update?id='+id)


@NeedLogin
def add(request):
    if request.method == "GET":
        DICT = {}
        DICT['info'] = ''
        DICT['typeList'] = getCategoryList()
        DICT['navPage'] = 'resource'
        DICT['number'] = -1
        DICT['username'] = request.session['username']
        return render_to_response('resourceUpdate.htm',DICT)
    
    resource = POST2Resource(request)
    now = getCurTime()
    resource['createTime'] = now
    resource['updateTime'] = now

    for tag in resource['tagList']:
        if clct_tag.find_one({'name':tag}) == None:
            createTag(tag)
        addTagRef(tag, 1)
    if resource['resourceName'] == '':raise Exception('资源名 不能为空')
    if resource['videoType'] == '':raise Exception('videoType 不能为空')
    if resource['videoId'] == '':raise Exception('videoId 不能为空')
    
    id = clct_resource.insert(resource.getInsertDict())
    id = str(id)
    img = request.FILES.get('resourceImage',None)
    if img:
        filename = saveResourceImage(img.read(),id) 
        clct_resource.update({'_id':ObjectId(id)},{'$set':{'resourceImageUrl':filename}})
    else:
        channel = clct_channel.find_one({'channelId':resource['channelId']})
        clct_resource.update({'_id':ObjectId(id)},{'$set':{'resourceImageUrl':channel['resourceImageUrl']}})
    
    #增加截图任务
    if resource['videoType'] not in [u'bt',u'huohua']:
        ret = addVideoInfoTask(resource['channelId'],str(id),resource['videoId'],resource['videoType'],force=True)
        if ret:
            clct_resource.update({'_id':ObjectId(id)},{'$set':{'snapshot':'doing'}})
    #更新 频道更新时间
    clct_channel.update({'channelId':resource['channelId']},{'$set':{'updateTime':getCurTime()}})
    return HttpResponseRedirect('update?id='+id)

'''
def saveChannelImage(img, id):

    #裁剪
    outimg = StringIO.StringIO()
    imgconvert(img,outimg,CHANNEL_IMAGE_WIDTH,CHANNEL_IMAGE_HEIGHT)
    #保存
    filename = 'videoCMS/channel/%s.jpg'% id+ getCurTime()
    with open(IMAGE_DIR + '/' + filename, 'wb') as f:
        f.write(outimg.getvalue())
        
    return filename.replace('/', '_')
'''
def saveResourceImage(img, id):
    filename = 'videoCMS/resource/%s.jpg'%(id + getCurTime())
    with open(IMAGE_DIR + '/' + filename, 'wb') as f:
        f.write(img)
    return filename.replace('/', '_')

#==============================================================
@NeedLogin
def toggleOnlineStatus(request):
    ret = {}
    id = ObjectId(request.GET.get('id'))
    resource = clct_resource.find_one({'_id':id})

    if resource['isOnline'] == True:
        clct_resource.update({'_id':id},{'$set':{'isOnline':False,'modifyTime':getCurTime()}})
    else:
        up = {'isOnline':True,'modifyTime':getCurTime()}
        if resource['updateTime'] == '00000000000000':
            up['updateTime'] = getCurTime()
        clct_resource.update({'_id':id},{'$set':{'isOnline':True,'modifyTime':getCurTime()}})
    ret['status'] = not resource['isOnline']
    
    return HttpResponse(json.dumps(ret))

#=============================================================
@NeedLogin
def getVideoId(request):
    url = request.POST.get('url')
    ret = {}
    query = {'url':url}
    print query
    resp = json.loads(urllib2.urlopen('http://60.28.29.38:9090/api/getVideoId',json.dumps(query)).read())
    ret['videoType'] = resp['videoType']
    ret['videoId'] = resp['videoId']
    return HttpResponse(json.dumps(ret))


#==============================================================
@NeedLogin
def deleteResource(request):
    resourceId = request.GET.get('resourceId')
    clct_resource.remove({'_id':ObjectId(resourceId)})
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@NeedLogin
def deleteChannelResource(request):
    channelId = int(request.GET.get('channelId'))
    clct_resource.remove({'channelId':channelId})
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

#==============================================================

@NeedLogin
def refreshSnapshot(request):
    id = request.GET.get('id')
    resource = clct_resource.find_one({'_id':ObjectId(id)})
    ret = addVideoInfoTask(resource['channelId'],str(id),resource['videoId'],resource['videoType'],force=True)
    if ret:
        clct_resource.update({'_id':ObjectId(id)},{'$set':{'snapshot':'doing'}})
        return HttpResponse('ok')
    else:
        return HttpResponse('failed')
    
#==============================================================

@NeedLogin
def stopSnapshot(request):
    id = request.GET.get('id')
    clct_resource.update({'_id':ObjectId(id)},{'$set':{'snapshot':''}})
    clct_videoInfoTask.remove({'resourceId':id},mulit=True)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

#==============================================================
@NeedLogin
def CdnSync(request):
    
    sync = CDNSyncTask()
    sync['']
    clct_cdnSync.insert()
    pass
@NeedLogin
def prefetchCDN(request):
    videoId = "/" + request.GET.get("videoId")
    ret = PrefetchCache(videoId)
    clct_resource.update({'videoId':videoId[1:]},{'$set':{'cdn':'waiting'}})
    return HttpResponse(ret)

@NeedLogin
def queryCDN(request):
    videoId = "/" + request.GET.get("videoId")
    ret = GetProgress(videoId)
    return HttpResponse(ret)

def showJson(request):
    id = request.GET.get('id')
    one = clct_resource.find_one({'_id':ObjectId(id)})
    one['_id'] = str(one['_id'])
    return HttpResponse(json.dumps(one))

@NeedLogin
def getVideoUrl(request):
    videoId = request.GET.get('videoId')
    videoType = request.GET.get('videoType')
    
    data = {"request-body":{"getVideoUrl":{"videoType":videoType,"videoId":videoId}}}

    httpUtil = HttpUtil()
    result = httpUtil.Post('http://60.28.29.38:9090/api/huohuaId2Url',json.dumps(data))

    return HttpResponse(result)

@NeedLogin
def unsetInvalid(request):
    id = request.GET.get('id')
    clct_resource.update({'_id':ObjectId(id)},{'$unset':{'validTime':1}})
    return HttpResponse('ok')

#==============================================================
'''
def addEd2k(request):
    if request.method == "GET":
        DICT = {}
        DICT['info'] = ''
        return render_to_response('resourceAddEd2k.htm',DICT)
    
    resource  = Resource()
    resource['resourceName'] = request.POST.get('resourceName')
    resource['channelId'] = int(request.POST.get('channelId'))
    resource['isOnline'] = True if request.POST.get('channelId') == u'是' else False
    resource['tagList'] = map(lambda a:a.strip(),request.POST.get('tagList').split(','))
    for tag in resource['tagList']:
        if tag == '':continue
        if clct_tag.find_one({'name':tag}) == None:
            createTag(tag)
        addTagRef(tag, 1)
    if resource['resourceName'] == '':
        raise Exception('资源名 不能为空')
    
    id = clct_resource.insert(resource.getInsertDict())
    id = str(id)
    return HttpResponseRedirect('update?id='+id)
'''


if __name__ == '__main__':
    getVideoId('http://yule.iqiyi.com/20130521/c9113c27539bb1c3.html')