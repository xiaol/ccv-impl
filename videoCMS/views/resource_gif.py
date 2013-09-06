#coding=utf8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
import json,StringIO,re,os
from videoCMS.conf import clct_resource,clct_channel,clct_tag,IMAGE_DIR,IMG_INTERFACE,IMG_INTERFACE_FF
from bson import ObjectId
from videoCMS.common.Domain import Resource,Tag,CDNSyncTask
from videoCMS.common.common import Obj2Str,getCurTime,antiFormatHumanTime,formatHumanTime,getCurDate

from videoCMS.common.db import getCategoryList
#from videoCMS.views.channel import saveResourceImage
from videoSearch.common.videoInfoTask import addVideoInfoTask
from resource import addTagRef,createTag
import uuid,Image


def POST2Resource(request):
    #更新
    resource = Resource()
    resource['videoId'] = request.POST.get('videoId').strip()
    resource['videoType'] = "gif"#request.POST.get('videoType').strip()
    resource['resourceName'] = request.POST.get('resourceName')
    resource['channelId'] = int(request.POST.get('channelId'))
    resource['weight'] = float(request.POST.get('weight'))
    channel = clct_channel.find_one({'channelId':resource['channelId']})
    resource['categoryId'] = channel['channelType']
    resource['duration'] = int(float(request.POST.get('duration')))
    resource['resourceSize'] = -1 if request.POST.get('resourceSize') == '' else int(request.POST.get('resourceSize'))
    resource['isOnline'] = True if request.POST.get('channelId') == u'是' else False
    resource['tagList'] = map(lambda a:a.strip(),request.POST.get('tagList').split(','))
    resource['modifyTime'] = getCurTime()
    resource['scheduleGoOnline'] = antiFormatHumanTime(request.POST.get('scheduleGoOnline',''))
    resource['number'] = request.POST.get('number')
    resource['resourceUrl'] = request.POST.get('resourceUrl')
    resource['type'] = 'gif'

    try:
        resource['number'] = int(resource['number'])
    except:
        pass
    return resource


def update(request):
    id = request.GET.get('id','')
    if request.method == "GET":
        resource = clct_resource.find_one({'_id':ObjectId(id)})
        resource['tagList'] = ','.join(resource.get('tagList',[]))
        resource['resourceImageUrl'] = IMG_INTERFACE_FF%(250,150,resource['resourceImageUrl'])
        resource['gifUrl'] = IMG_INTERFACE_FF%('*','*',resource['gifUrl'])
        resource['scheduleGoOnline'] = formatHumanTime(resource['scheduleGoOnline'])

        DICT = Obj2Str(resource)
        DICT['info'] = ''
        DICT['update'] = True
        DICT['navPage'] = 'resource'
        return render_to_response('resourceGifUpdate.htm',DICT)

    resource = POST2Resource(request)

        

    #如果更新了GIF，则封面封面由GIF生成。否则单独更新
    img = request.FILES.get('gifUrl',None)
    if img:
        imgdata = img.read()
        resource['gifUrl'] = saveGifImage(imgdata,resource['channelId'],id)
        resource['videoId'] = resource['gifUrl']
        resource['resourceImageUrl'] = saveGif2Static(imgdata,resource['channelId'],id)
    else:
        img = request.FILES.get('resourceImage',None)
        if img:
            resource['resourceImageUrl'] = saveResourceImage(img.read(),resource['channelId'],id)
    
    clct_resource.update({'_id':ObjectId(id)},{'$set':resource.getUpdateDict()})
    return HttpResponseRedirect('update?id='+id)


def add(request):
    if request.method == "GET":
        DICT = {}
        DICT['info'] = ''
        DICT['typeList'] = getCategoryList()
        DICT['navPage'] = 'resource'
        DICT['videoType'] = 'gif'
        DICT['weight'] = -1
        DICT['duration'] = -1
        DICT['resourceSize'] = -1
        return render_to_response('resourceGifUpdate.htm',DICT)

    resource = POST2Resource(request)

    for tag in resource['tagList']:
        if clct_tag.find_one({'name':tag}) == None:
            createTag(tag)
        addTagRef(tag, 1)
    if resource['resourceName'] == '':raise Exception('资源名 不能为空')
    if resource['videoType'] == '':raise Exception('videoType 不能为空')

    img = request.FILES.get('gifUrl',None)
    if img:
        _uuid = str(uuid.uuid4())
        imgdata = img.read()
        resource['gifUrl'] = saveGifImage(imgdata,resource['channelId'],_uuid)
        resource['videoId'] = resource['gifUrl']
        resource['resourceImageUrl'] = saveGif2Static(imgdata,resource['channelId'],_uuid)
    else:
        raise Exception('未选择图片')

    id = clct_resource.insert(resource.getInsertDict())

    return HttpResponseRedirect('update?id='+str(id))



def saveResourceImage(img,channel, id):
    date = getCurDate()
    filename = 'videoCMS/resource/%s/%s/%s.jpg'%(channel,date,id+getCurTime())
    fullpath = IMAGE_DIR + '/' + filename
    path = os.path.dirname(fullpath)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(fullpath, 'wb') as f:
        f.write(img)
    return filename.replace('/', '_')



def saveGifImage(img,channel, id):
    date = getCurDate()
    filename = 'videoCMS/gif/%s/%s/%s.gif'% (channel,date,id+ getCurTime())
    fullpath = IMAGE_DIR + '/' + filename
    path = os.path.dirname(fullpath)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(fullpath, 'wb') as f:
        f.write(img)
    return filename.replace('/', '_')

def saveGif2Static(data,channel,id):
    date = getCurDate()
    filename = 'videoCMS/resource/%s/%s/%s.gif'% (channel,date,id+ getCurTime())
    fullpath = IMAGE_DIR + '/' + filename
    path = os.path.dirname(fullpath)
    if not os.path.exists(path):
        os.makedirs(path)
    mem = StringIO.StringIO(data)
    #mem.write(data)
    img = Image.open(mem)
    img.save(fullpath)
    return filename.replace('/', '_')