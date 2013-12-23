#coding=utf8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
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
    clct_tag.update({'name':name},{'$inc':{'refNum':addNum}})

def addTag(name,addNum=1):
    if clct_tag.find_one({'name':name}) == None:
        createTag(name,addNum)
    else:
        addTagRef(name,addNum)


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
    isOnline = request.GET.get('isOnline','all')
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
        immm = one['resourceImageUrl']
        one['resourceImageUrl'] = IMG_INTERFACE_FF%(96,96,immm)
        one['resourceImageUrlOri'] = IMG_INTERFACE_FF%('*','*',immm)
        channel = clct_channel.find_one({'channelId':one['channelId']})
        if channel == None:
            one['channelName'] = "not found channel:"+str(one['channelId'])
        else:
            one['channelName'] = channel['channelName']
        one['createTime'] = formatHumanTime(one['createTime'])
        one['updateTime'] = formatHumanTime(one['updateTime'])
        one['scheduleGoOnline'] = formatHumanTime(one['scheduleGoOnline'])



    DICT['nextPage'] = page + 1
    DICT['prePage'] = page-1 if page>1 else 1
    DICT['findNum'] = clct_resource.find(spec).count()
    DICT['navPage'] = 'resource'
    DICT['typeList'] = [u'全部'] + getCategoryList()
    DICT.update(locals())

    return render_to_response('resourceList.htm',DICT,context_instance=RequestContext(request))


def POST2Resource(request):
    resource  = Resource()
    resource['videoId'] = request.POST.get('videoId').strip()
    resource['videoType'] = request.POST.get('videoType').strip()
    resource['resourceName'] = request.POST.get('resourceName')
    resource['channelId'] = int(request.POST.get('channelId'))
    resource['weight'] = float(request.POST.get('weight'))
    channel = clct_channel.find_one({'channelId':resource['channelId']})
    resource['categoryId'] = channel['channelType']
    resource['duration'] = int(float(-1 if request.POST.get('duration') == '' else request.POST.get('duration')))
    resource['resourceSize'] = -1 if request.POST.get('resourceSize') == '' else int(request.POST.get('resourceSize'))
    resource['isOnline'] = True if request.POST.get('isOnline') == u'是' else False
    resource['tagList'] = [tag for tag in map(lambda a:a.strip(),request.POST.get('tagList').replace(u'，',',').split(',')) if tag!='']
    resource['scheduleGoOnline'] = antiFormatHumanTime(request.POST.get('scheduleGoOnline',''))
    resource['number'] = request.POST.get('number')
    resource['resourceUrl'] = request.POST.get('resourceUrl')
    resource['subtitle'] = request.POST.get('subtitle')
    resource['isLD'] = True if request.POST.get('isLD') == u'是' else False
    resource['isRecommend'] = True if request.POST.get('isRecommend') == u'是' else False
    resource['recReason'] = request.POST.get('recReason')
    resource['updateTime'] = request.POST.get('updateTime')
    resource['resolution'] = int(request.POST.get('resolution',-1))
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
        resource['resourceImageUrl2'] = IMG_INTERFACE_FF%(250,150,resource['resourceImageUrl2'])
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
        return render_to_response('resourceUpdate.htm',DICT,context_instance=RequestContext(request))
    
    #更新
    resource = POST2Resource(request)
    resource['modifyTime'] = getCurTime()

    #更新tag
    oldresource = clct_resource.find_one({'_id':ObjectId(id)})
    for tag in oldresource['tagList']:
        addTagRef(tag,-1)
    for tag in resource['tagList']:
        addTag(tag,1)
    ##
    ##待 补充 对tag 引用次数的修改
        
    img = request.FILES.get('resourceImage',None)
    if img:
        resource['resourceImageUrl'] = saveResourceImage(img.read(),id)

    img = request.FILES.get('resourceImage2',None)
    if img:
        resource['resourceImageUrl2'] = saveResourceImage(img.read(),id+'-2-')
    
    
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
        return render_to_response('resourceUpdate.htm',DICT,context_instance=RequestContext(request))
    
    resource = POST2Resource(request)
    now = getCurTime()
    resource['createTime'] = now
    resource['modifyTime'] = now
    resource['updateTime'] = now

    for tag in resource['tagList']:
        addTag(tag, 1)
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

    img = request.FILES.get('resourceImage2',None)
    if img:
        resource['resourceImageUrl2'] = saveResourceImage(img.read(),id+'-2-')
    
    #增加截图任务
    if resource['videoType'] not in [u'bt',u'huohua']:
        ret = addVideoInfoTask(resource['channelId'],str(id),resource['videoId'],resource['videoType'],force=True)
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
        clct_resource.update({'_id':id},{'$set':up})
    newestResource = clct_resource.find({'channelId':resource['channelId']}).sort([('updateTime',-1)]).limit(1)[0]
    clct_channel.update({'channelId':resource['channelId']},{'$set':{'updateTime':newestResource['updateTime']}})
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
    if clct_resource.find_one(ret):
        ret['exists'] = True
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


def search(request):
    kw = request.GET['keyword']
    ret = list(clct_resource.find({'resourceName':re.compile(kw)}).limit(10))
    for one in ret:
        one['id'] = str(one['_id'])
        one.pop('_id')
    return HttpResponse(json.dumps(ret))

def searchId(request):
    id = ObjectId(request.GET['id'])
    ret = list(clct_resource.find({'_id':ObjectId(id)}))
    for one in ret:
        one['id'] = str(one['_id'])
        one.pop('_id')
    return HttpResponse(json.dumps(ret))


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