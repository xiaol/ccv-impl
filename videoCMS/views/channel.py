#coding=utf8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import json,StringIO,re,time
from videoCMS.conf import clct_channel,clct_resource,IMAGE_DIR,IMG_INTERFACE,IMG_INTERFACE_FF,\
    clct_category,clct_cronJob
from videoCMS.conf import CHANNEL_IMAGE_WIDTH,CHANNEL_IMAGE_HEIGHT,searchHandleListAll
from bson import ObjectId
from videoCMS.common.Domain import Channel
from videoCMS.common.doubanMovie import extraInfos
from videoCMS.common.common import Obj2Str,getCurTime,formatHumanTime,validateTimeStr,antiFormatHumanTime
from videoCMS.common.ImageUtil import imgconvert
from videoCMS.common.db import getCategoryNameById,getCategoryIdByName,getCategoryList,getCategoryIdMapName
from videoCMS.views.login import *
import time

def getSkipLimit(DICT,skip=0,limit=10):
    _skip = DICT.get('skip',skip)
    _limit = DICT.get('limit',limit)
    return _skip,_limit


@NeedLogin
def index(request):
    spec = {}
    DICT = {}

    if checkLogin(request):
        DICT['username'] = request.session['username']

    
    page = int(request.GET['page']) if request.GET.get('page','') != '' else 1
    limit =int(request.GET['len']) if request.GET.get('len','') != '' else 10
    
    name = request.GET.get('name','')
    processed = request.GET.get('processed','')
    mongo = request.GET.get('mongo','')
    channelId = request.GET.get('channelId','')
    id = request.GET.get('id','')
    channelType = request.GET.get('channelType','')
    sort = request.GET.get('sort','')
    skip = limit * (page - 1)
    sortList = [('_id',-1)]
    
    if id != '':
        spec['_id'] = ObjectId(id)
    elif channelId != '':
        spec['channelId'] = int(channelId)
    elif name != '':
        spec['channelName'] = re.compile(name)
    elif mongo != '':
        spec = json.loads(mongo)
    if channelType != '' and channelType != u'全部':
        spec['channelType'] = getCategoryIdByName(channelType)
    if processed != "":
        spec['processed'] = True if processed=="true" else False
    if sort != "":
        if sort == 'createTime':
            sortList = [('createTime',-1)]
        elif sort == 'updateTime':
            sortList = [('updateTime',-1)]
        elif sort == 'modifyTime':
            sortList = [('modifyTime',-1)]
        elif sort == 'weight':
            sortList = [('weight',-1)]
        elif sort == 'subscribeNum':
            sortList = [('subscribeNum',-1)]
        
    channelList = list(clct_channel.find(spec).sort(sortList).skip(skip).limit(limit))
    CategoryIdMapName = getCategoryIdMapName()
    for one in channelList:
        one['id'] = str(one['_id'])
        one.pop('_id')
        one['channelImageUrl'] = IMG_INTERFACE + one['channelImageUrl']
        one['createTime'] = formatHumanTime(one['createTime'])
        one['searchTime'] = formatHumanTime(one['searchTime'])
        one['modifyTime'] = formatHumanTime(one['modifyTime'])
        one['updateTime'] = formatHumanTime(one['updateTime'])
        one['nextSearchTime'] = formatHumanTime(one['nextSearchTime'])
        one['channelType'] = CategoryIdMapName[one['channelType']]
    

    DICT['channelList'] = channelList
    
    DICT['page'] = page
    DICT['len'] = limit
    DICT['nextPage'] = page + 1
    DICT['prePage'] = page-1 if page>1 else 1
    DICT['name'] = name
    DICT['id'] = id
    DICT['channelId'] = channelId
    DICT['mongo'] = mongo
    DICT['findNum'] = clct_channel.find(spec).count()
    DICT['typeList'] = [u'全部'] + getCategoryList()
    DICT['channelType'] = channelType
    DICT['processed'] = processed
    DICT['navPage'] = 'channel'
    DICT['sort'] = sort
    return render_to_response('channelList.htm',DICT,context_instance=RequestContext(request))



def POST2Channel(request):
    channel = Channel()
    channel = Channel()
    if request.POST['channelId'] == '':
        channel['channelId'] = getMaxChannelId()
    else:
        channel['channelId'] = int(request.POST['channelId'])

    channel['tvNumber'] = request.POST.get('tvNumber')
    if channel['tvNumber'] == '':
        channel['tvNumber'] = 0
    try:
        channel['tvNumber'] = int(request.POST.get('tvNumber',0))
    except:
        pass

    channel['createTime'] = request.POST.get('createTime')
    channel['identifer'] = int(request.POST.get('identifer'))
    channel['duration'] = int(-1 if request.POST.get('duration') == '' else request.POST.get('duration'))
    channel['daysAhead'] = int(-1 if request.POST.get('daysAhead') == '' else request.POST.get('daysAhead'))
    channel['channelName'] = request.POST.get('channelName')
    channel['subtitle'] = request.POST.get('subtitle')
    channel['sourceWebsite'] = request.POST.get('sourceWebsite')
    channel['yyetsSeason'] = request.POST.get('yyetsSeason')
    channel['yyetsDownMode'] = request.POST.get('yyetsDownMode')
    channel['yyetsEncode'] = request.POST.get('yyetsEncode')
    channel['sourceList'] = filter(lambda a:a,request.POST.getlist('sourceList'))
    channel['searchHandleList'] = request.POST.getlist('searchHandleList')
    if len(channel['searchHandleList']) > len(channel['sourceList']):
        channel['searchHandleList'] = channel['searchHandleList'][:len(channel['sourceList'])]

    channel['channelType'] = getCategoryIdByName(request.POST.get('channelType'))
    channel['categoryType'] = getCategoryTypeById(channel['channelType'])
    channel['tagList'] = map(lambda a:a.strip(),request.POST.get('tagList').split(','))
    channel['updateTime'] = request.POST.get('updateTime')
    if channel['updateTime'] == '':channel['updateTime'] = getCurTime()
    if not validateTimeStr(channel['updateTime']):raise Exception('updateTime 格式不正确')
    channel['processed'] = True if request.POST.get('processed') == u'已处理' else False
    channel['isNewest'] = True if request.POST.get('isNewest') == u'是' else False
    channel['autoOnline'] = True if request.POST.get('autoOnline') == u'是' else False
    channel['isRecommend'] = True if request.POST.get('isRecommend') == u'是' else False
    channel['type'] = request.POST.get('type')
    channel['autoSub'] = True if request.POST.get('autoSub') == u'是' else False
    channel['onSquare'] = True if request.POST.get('onSquare') == u'是' else False
    channel['snapShot'] = True if request.POST.get('snapShot') == u'是' else False
    channel['weight'] = 0 if request.POST.get('weight') == '' else int(request.POST.get('weight'))
    channel['nextSearchTime'] = request.POST.get('nextSearchTime')
    if channel['nextSearchTime'] == "":channel['nextSearchTime'] = '99990101000000'
    if not validateTimeStr(channel['nextSearchTime']):raise Exception('nextSearchTime 格式不正确')
    channel['handleName'] = request.POST.get('handleName')
    channel['handleArgs'] = request.POST.get('handleArgs')
    channel['handleFrequents'] = request.POST.get('handleFrequents')
    #同步类别的视频类型 到 频道
    channel['videoClass'] = clct_category.find_one({'categoryId':channel['channelType']})['videoClass']
    #检查 字段
    if channel['channelName'] == '':
        raise Exception('频道名 不能为空')

    return channel

@NeedLogin
def update(request):
    id = request.GET.get('id','')
    if request.method == "GET":
        channel = clct_channel.find_one({'_id':ObjectId(id)})
        channel['tagList'] = ','.join(channel.get('tagList',[]))
        channel['channelImageUrl'] = IMG_INTERFACE_FF%(250,150,channel['channelImageUrl'])
        channel['resourceImageUrl'] = IMG_INTERFACE_FF%(250,150,channel['resourceImageUrl'])
        channel['poster'] = IMG_INTERFACE_FF%(250,150,channel['poster'])
        channel['channelType'] = getCategoryNameById(channel['channelType'])
        if len(channel['searchHandleList']) < len(channel['sourceList']):
            for i in xrange(len(channel['sourceList']) - len(channel['searchHandleList'])):
                channel['searchHandleList'].append("")
        channel['sourceSearchList'] = zip(channel['sourceList'],channel['searchHandleList'])
        
        DICT = Obj2Str(channel)
        DICT['info'] = ''
        DICT['typeList'] = getCategoryList()
        DICT['update'] = True
        DICT['navPage'] = 'channel'
        DICT['searchHandleListAll'] = json.dumps(searchHandleListAll)
        DICT['username'] = request.session['username']
        return render_to_response('channelUpdate.htm',DICT,context_instance=RequestContext(request))
    
    #更新
    channel = POST2Channel(request)

    channel['modifyTime'] = getCurTime()

    #更新图片
    img = request.FILES.get('channelImage',None)
    if img:channel['channelImageUrl'] = saveChannelImage(img.read(),id)
    img = request.FILES.get('poster',None)
    if img:channel['poster'] = savePosterImage(img.read(),id) 
    img = request.FILES.get('resourceImage',None)
    if img:
        channel['resourceImageUrl'] = saveResourceImage(img.read(),id) 
        #更新所有的resourceImage
        clct_resource.update({'channelId':channel['channelId'],'resourceImageUrl':''},{'$set':{'resourceImageUrl':channel['resourceImageUrl']}},multi=True)
    
    #更新资源的 channelId关联
    oldChannelId = clct_channel.find_one({'_id':ObjectId(id)})['channelId']
    clct_resource.update({'channelId':oldChannelId},{'$set':{'channelId':channel['channelId']}},multi=True)
    
    #更新 cateogoryId
    categoryId =  channel['channelType']
    clct_resource.update({'channelId':channel['channelId']}, {'$set':{'categoryId':categoryId}},multi=True)

    clct_channel.update({'_id':ObjectId(id)},{'$set':channel.getUpdateDict()})
    return HttpResponseRedirect('update?id='+id)


@NeedLogin
def add(request):
    if request.method == "GET":
        DICT = {}
        DICT['info'] = ''
        DICT['typeList'] = getCategoryList()
        DICT['navPage'] = 'channel'
        DICT['autoOnline'] = True
        DICT['searchHandleListAll'] = json.dumps(searchHandleListAll)
        DICT['username'] = request.session['username']
        return render_to_response('channelUpdate.htm',DICT,context_instance=RequestContext(request))
    
    channel = POST2Channel(request)

    channel['createTime'] = getCurTime()
    channel['modifyTime'] = getCurTime()


    id = clct_channel.insert(channel.getInsertDict(),safe=True)
    id = str(id)
    
    
    #保存封面
    img = request.FILES.get('channelImage',None)
    if img:
        filename = saveChannelImage(img.read(), id)
        clct_channel.update({'_id':ObjectId(id)},{'$set':{'channelImageUrl':filename}})
    
    img = request.FILES.get('poster',None)
    if img:
        filename = savePosterImage(img.read(), id)
        clct_channel.update({'_id':ObjectId(id)},{'$set':{'poster':filename}})
    
    img = request.FILES.get('resourceImage',None)
    if img:
        filename = saveResourceImage(img.read(), id)
        clct_channel.update({'_id':ObjectId(id)},{'$set':{'resourceImageUrl':filename}})
        #更新到所有
        clct_resource.update({'channelId':channel['channelId'],'resourceImageUrl':''},{'$set':{'resourceImageUrl':filename}},multi=True)
    
    #更新category更新时间
    clct_category.update({'categoryId':channel['channelType']},{'$set':{'updateTime':getCurTime()}})
    return HttpResponseRedirect('update?id='+id)

def getMaxChannelId():
    channel = list(clct_channel.find().sort([('channelId',-1)]).limit(1))[0]
    print channel
    return channel['channelId'] + 1


def getCategoryTypeById(id):
    return clct_category.find_one({'categoryId':id})['categoryType']

def saveChannelImage(img, id):
    '''
    #裁剪
    outimg = StringIO.StringIO()
    imgconvert(img,outimg,CHANNEL_IMAGE_WIDTH,CHANNEL_IMAGE_HEIGHT)
    #保存
    filename = 'videoCMS/channel/%s.jpg'%id
    with open(IMAGE_DIR + '/' + filename, 'wb') as f:
        f.write(outimg.getvalue())
    '''
    filename = 'videoCMS/channel/%s.jpg'% (id+ getCurTime())
    with open(IMAGE_DIR + '/' + filename, 'wb') as f:
        f.write(img)
     
    return filename.replace('/', '_')

def saveResourceImage(img, id):
    filename = 'videoCMS/channel/resource-%s.jpg'%(id + getCurTime())
    with open(IMAGE_DIR + '/' + filename, 'wb') as f:
        f.write(img)
     
    return filename.replace('/', '_')

def savePosterImage(img, id):
    filename = 'videoCMS/channel/poster-%s.jpg'%(id + getCurTime())
    with open(IMAGE_DIR + '/' + filename, 'wb') as f:
        f.write(img)
     
    return filename.replace('/', '_')

#========================================
@NeedLogin
def detail(request):
    id = request.GET.get('id','')
    if request.method == "GET":
        channel = clct_channel.find_one({'_id':ObjectId(id)})
        
        DICT = Obj2Str(channel)
        DICT['info'] = ''
        DICT['navPage'] = 'channel'
        return render_to_response('channelDetail.htm',DICT,context_instance=RequestContext(request))
    
    #更新
    channel = Channel()
    channel['channelId'] = int(request.POST.get('channelId'))
    channel['channelName'] = request.POST.get('channelName')
    channel['detailDirecter'] = request.POST.get('detailDirecter')
    channel['detailDistrict'] = request.POST.get('detailDistrict')
    channel['detailLanguage'] = request.POST.get('detailLanguage')
    channel['detailReleaseDate'] = request.POST.get('detailReleaseDate')
    channel['detailDoubanUrl'] = request.POST.get('detailDoubanUrl')
    channel['detailDuration'] = request.POST.get('detailDuration','')
    channel['detaildoubanScore'] = float(request.POST.get('detaildoubanScore',-1))
    channel['detailDescription'] = request.POST.get('detailDescription')
    channel['detailTrailerUrl'] = request.POST.get('detailTrailerUrl')
    channel['detailTrailerVideoType'] = request.POST.get('detailTrailerVideoType')
    channel['detailTrailerVideoId'] = request.POST.get('detailTrailerVideoId')
    channel['detailTotalTvNumber'] = int(request.POST.get('detailTotalTvNumber',-1))
    channel['detailLeadingRole'] = filter(lambda a:a,request.POST.getlist('detailLeadingRole'))
    channel['detailMovieCategory'] = filter(lambda a:a,request.POST.getlist('detailMovieCategory'))
    
    '''处理预告片'''
    trailers = zip(
    filter(lambda a:a,request.POST.getlist('detailTrailerVideoType')),
    request.POST.getlist('detailTrailerVideoId'),
    request.POST.getlist('detailTrailerTitle'),
    request.POST.getlist('detailTrailerUrl')
    )
    channel['detailTrailerList'] = [{"url":trailer[3], "title":trailer[2] , "videoType":trailer[0], "videoId":trailer[1]}
                                        for trailer in trailers]
        
    
    
    print channel.getUpdateDict()
    clct_channel.update({'_id':ObjectId(id)},{'$set':channel.getUpdateDict()})
    return HttpResponseRedirect('detail?id='+id)

def detailExtraDouban(request):
    channelId = int(request.GET.get('id',''))
    url = request.GET.get('url','')
    info = extraInfos(url)
    print info
    clct_channel.update({'channelId':channelId}, {'$set':info })
    return HttpResponse('ok')
#==========================================
@NeedLogin
def updateDuration(request):
    channelId = int(request.GET['channelId'])
    duration = int(request.GET['duration'])
    
    clct_resource.update({'channelId':channelId},{'$set':{'duration':duration}},multi=True)
    return HttpResponse('ok')


@NeedLogin
def deleteChannel(request):
    channelId = int(request.GET.get('channelId'))
    clct_channel.remove({'channelId':channelId})
    clct_resource.remove({'channelId':channelId},multi=True)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])




@NeedLogin
def pushChannel(request):
    from videoCMS.conf import jPushClient,JPUSH_APP_KEY

    cronTime = request.GET.get('cronTime')
    channelId = int(request.GET.get('pushChannelId'))
    title = request.GET.get('pushTitle')
    content = request.GET.get('pushContent')
    channel = clct_channel.find_one({'channelId':channelId})
    extras = \
    {
        'action':"OpenChannel",
        'channelId':channelId,
        'videoClass':channel['videoClass']
    }

    if cronTime == "":
        jPushClient.send_notification_by_appkey(JPUSH_APP_KEY, 1, 'des',title,content, 'android',extras=extras)
    else:
        task = {"type":"AndroidPush","pushChannelId":channelId,"pushTitle":title,"pushContent":content,"extras":extras}
        task['pushType'] = 'AppKey'
        task['cronTime'] = antiFormatHumanTime(cronTime)
        task['createTime'] = getCurTime()
        clct_cronJob.insert(task)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@NeedLogin
def updateSearchNow(request):
    channelId = int(request.GET['channelId'])
    channel = clct_channel.find_one({'channelId':channelId})
    handleFrequents = int(channel['handleFrequents'])
    tCur = time.time()
    tPreNext = time.mktime(time.strptime(channel['nextSearchTime'],'%Y%m%d%H%M%S'))
    
    tNext =  tPreNext + (-int(abs(tCur -tPreNext) / handleFrequents) - 2) * handleFrequents
    t = time.strftime('%Y%m%d%H%M%S',time.localtime(tNext + time.timezone))

    print time.timezone
    
    clct_channel.update({'channelId':channelId},{'$set':{'nextSearchTime':t}})
    return HttpResponse('ok')

@NeedLogin
def toggleProcessed(request):
    ret = {}
    channelId = int(request.GET.get('channelId'))
    channel = clct_channel.find_one({'channelId':channelId})

    clct_channel.update({'channelId':channelId},{'$set':{'processed':not channel['processed']}})

    ret['status'] = not channel['processed']
    
    return HttpResponse(json.dumps(ret))

@NeedLogin
def toggleRec(request):
    ret = {}
    channelId = int(request.GET.get('channelId'))
    channel = clct_channel.find_one({'channelId':channelId})

    clct_channel.update({'channelId':channelId},{'$set':{'isRecommend':not channel['isRecommend']}})

    ret['status'] = not channel['isRecommend']

    return HttpResponse(json.dumps(ret))

#===============================================
@NeedLogin
def resetWeight(request):
    channelId = int(request.GET.get("channelId"))
    clct_resource.update({"channelId":channelId},{"$set":{"weight":-1}},multi=True)
    return HttpResponse("ok")


def showJson(request):
    id = request.GET.get('id')
    one = clct_channel.find_one({'_id':ObjectId(id)})
    one['_id'] = str(one['_id'])
    return HttpResponse(json.dumps(one))

@NeedLogin
def search(request):
    kw = request.GET.get('keyword')
    ret = []
    for one in  clct_channel.find({'channelName':re.compile(kw)}).limit(10):
        one['id'] = str(one['_id'])
        one.pop('_id')
        ret.append(one)
    return HttpResponse(json.dumps(ret))

@NeedLogin
def setCompleted(request):
    channelId = int(request.GET.get("channelId"))
    clct_channel.update({"channelId":channelId},{"$set":{"nextSearchTime":'99990101000000'},
                                                  "$unset":{"searchMsg":1,"searchStatus":1}})

    return HttpResponse('ok')

@NeedLogin
def disperseUpdateTime(request):
    channelId = int(request.GET.get('channelId'))
    channel = clct_channel.find_one({'channelId':channelId})
    disperseResourceUpdateTime(channelId,channel['createTime'],channel['updateTime'])
    return HttpResponse('ok')


def disperseResourceUpdateTime(channelId, startTime, endTime):
    resourceIt = clct_resource.find({'channelId':channelId},timeout=False).sort([('number',1),('createTime',1)])
    SIZE = resourceIt.count()
    if SIZE == 0:
        return

    t_start = time.mktime(time.strptime(startTime,'%Y%m%d%H%M%S'))
    t_now = time.mktime(time.strptime(endTime,'%Y%m%d%H%M%S'))

    t_span = (t_now - t_start)/SIZE
    t_this = t_start

    #间隔过短，修改开始时间
    if t_span < 3600 :
        t_span = 3600
        t_start = t_now - t_span*SIZE

    for resource in resourceIt:
        t_this += t_span
        updateTime = time.strftime('%Y%m%d%H%M%S',time.localtime(t_this))
        print updateTime
        clct_resource.update({'_id':resource['_id']},{'$set':{'updateTime':updateTime}})