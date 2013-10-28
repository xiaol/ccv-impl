#coding=utf8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
import json,StringIO,re,os
from videoCMS.conf import clct_resource,clct_preresource,clct_channel,clct_tag,IMAGE_DIR,IMG_INTERFACE,IMG_INTERFACE_FF
from videoCMS.conf import CHANNEL_IMAGE_WIDTH,CHANNEL_IMAGE_HEIGHT
from bson import ObjectId
from videoCMS.common.Domain import Resource,Tag
from videoCMS.common.common import Obj2Str,getCurTime
from videoCMS.common.ImageUtil import imgconvert
from videoCMS.common.db import getCategoryList
import urllib2
from videoSearch.ed2k.telnet import startEd2k,startBT

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

def index(request):
    spec = {}
    DICT = {}
    page = int(request.GET['page']) if request.GET.get('page','') != '' else 1
    limit =int(request.GET['len']) if request.GET.get('len','') != '' else 10
    
    name = request.GET.get('name','')
    mongo = request.GET.get('mongo','')
    id = request.GET.get('id','')
    channelId = request.GET.get('channelId','')
    skip = limit * (page - 1)
    
    if id != '':
        spec['_id'] = ObjectId(id)
    elif name != '':
        spec['resourceName'] = re.compile(name)
    elif channelId != '':
        spec['channelId'] = int(channelId)
        DICT['title'] = clct_channel.find_one(spec)['channelName']
        print DICT['title']
    elif mongo != '':
        spec = json.loads(mongo)

    resourceList = list(clct_preresource.find(spec).sort([('_id',-1)]).skip(skip).limit(limit))
    for one in resourceList:
        one['id'] = str(one['_id'])
        one.pop('_id')


    DICT['resourceList'] = resourceList
    
    DICT['page'] = page
    DICT['len'] = limit
    DICT['nextPage'] = page + 1
    DICT['prePage'] = page-1 if page>1 else 1
    DICT['name'] = name
    DICT['id'] = id
    DICT['channelId'] = channelId
    DICT['mongo'] = mongo
    DICT['findNum'] = clct_preresource.find(spec).count()
    DICT['navPage'] = 'preresource'
    DICT['username'] = request.session['username']
    return render_to_response('preresourceList.htm',DICT)


def update(request):
    id = request.GET.get('id','')
    if request.method == "GET":
        channel = clct_preresource.find_one({'_id':ObjectId(id)})
        channel['tagList'] = ','.join(channel.get('tagList',[]))
        #channel['channelImageUrl'] = IMG_INTERFACE_FF%(250,150,channel['channelImageUrl'])
        DICT = Obj2Str(channel)
        DICT['info'] = ''
        DICT['update'] = True
        DICT['navPage'] = 'preresource'
        DICT['username'] = request.session['username']
        return render_to_response('preresourceUpdate.htm',DICT)
    
    #更新
    resource = Resource()
    resource['videoId'] = request.POST.get('videoId')
    resource['videoType'] = request.POST.get('videoType')
    resource['resourceName'] = request.POST.get('resourceName')
    resource['channelId'] = int(request.POST.get('channelId'))
    resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['isOnline'] = True if request.POST.get('channelId') == u'是' else False
    resource['tagList'] = map(lambda a:a.strip(),request.POST.get('tagList').split(','))
    resource['modifyTime'] = getCurTime()
#    img = request.FILES.get('channelImage',None)
#    if img:
#        resource['channelImageUrl'] = saveChannelImage(img.read(),id) 
    clct_preresource.update({'_id':ObjectId(id)},{'$set':resource.getUpdateDict()})
    return HttpResponseRedirect('update?id='+id)



#==============================================================
p = re.compile('\|file\|([^\|]+?)\|')

def addEd2k(request):
    if request.method == "GET":
        DICT = {}
        DICT['info'] = ''
        DICT['navPage'] = 'preresource'
        DICT['username'] = request.session['username']
        return render_to_response('preresourceAddEd2k.htm',DICT)
    
    resource  = Resource()
    resource['resourceName'] = request.POST.get('resourceName')
    if resource['resourceName'] == '':raise Exception('资源名 不能为空')
    resource['channelId'] = int(request.POST.get('channelId'))
    resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['isOnline'] = True if request.POST.get('channelId') == u'是' else False
    resource['tagList'] = map(lambda a:a.strip(),request.POST.get('tagList').split(','))
    for tag in resource['tagList']:
        if tag == '':continue
        if clct_tag.find_one({'name':tag}) == None:createTag(tag)
        addTagRef(tag, 1)
    
    resource['createTime'] = getCurTime()
    resource['resourceUrl'] = request.POST.get('videoURL')
    resource['videoType'] = 'bt'
    filename = p.search(resource['resourceUrl']).groups()[0]
    resource['videoId'] = filename
    resource['type'] = 'video'
    
    if clct_preresource.find_one({'resourceUrl':resource['resourceUrl']}) != None:
        msg =  '已存在下载队列\nexist in download queue...exit'
        raise Exception(msg)
    if clct_resource.find_one({'resourceUrl':resource['resourceUrl']}) != None:
        msg =  '已下载资源\ndownloaded...exit'
        raise Exception(msg)
    #开始任务
    startEd2k(resource['resourceUrl'].encode('utf-8'))
    #插入
    id = clct_preresource.insert(resource.getInsertDict())
    id = str(id)
    return HttpResponseRedirect('update?id='+id)



def addTorrent(request):
    if request.method == "GET":
        DICT = {}
        DICT['info'] = ''
        DICT['navPage'] = 'preresource'
        return render_to_response('preresourceAddBT.htm',DICT)
    resource  = Resource()
    resource['channelId'] = int(request.POST.get('channelId'))
    channel = clct_channel.find_one({'channelId':resource['channelId']})
    
    resource['resourceName'] = request.POST.get('resourceName')
    if resource['resourceName'] == '':raise Exception('资源名 不能为空')
    resource['categoryId'] = channel['channelType']
    resource['resourceImageUrl'] = channel['resourceImageUrl']
    resource['duration'] = channel['duration']
    resource['isOnline'] = True if request.POST.get('channelId') == u'是' else False
    resource['tagList'] = map(lambda a:a.strip(),request.POST.get('tagList').split(','))
    for tag in resource['tagList']:
        if tag == '':continue
        if clct_tag.find_one({'name':tag}) == None:createTag(tag)
        addTagRef(tag, 1)
    
    resource['createTime'] = getCurTime()
    #resource['resourceUrl'] = request.POST.get('videoURL')
    resource['videoType'] = 'torrent'
    resource['videoId'] = request.POST.get('videoId')
    resource['type'] = 'video'
    resource['downloadType'] = 'torrent'
    resource['transcodeCoderate'] = request.POST.get('transcodeCoderate')
    resource['transcodeFramerate'] = request.POST.get('transcodeFramerate')
    resource['transcodeDimension'] = request.POST.get('transcodeDimension')
    resource['transcodeOutputname'] = request.POST.get('transcodeOutputname')
    
    if clct_preresource.find_one({'videoType':resource['videoType'],'videoId':resource['videoId']}) != None:
        msg =  '已存在下载队列\nexist in download queue...exit'
        raise Exception(msg)
    if clct_resource.find_one({'videoType':resource['videoType'],'videoId':resource['videoId']}) != None:
        msg =  '已下载资源\ndownloaded...exit'
        raise Exception(msg)
    
    
    '''保存BT文件,并且上传到 MLDONKEY服务器'''
    btFile = request.FILES.get('btFile',None)
    if not btFile:
        raise Exception('没有上传文件!!')
    filename = os.path.dirname(os.path.dirname(__file__)) + '/upload/' + btFile.name
    with open(filename,'w') as f:
        f.write(btFile.read())
    
    cmd = "scp \"%s\" root@60.28.29.38:/root/.mldonkey/torrents/upload"%filename

    if os.system(cmd):
        import subprocess
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = ''
        for line in p.stdout.readlines():
            out += line
        retval = p.wait()
        raise Exception(out)
        raise Exception('种子文件拷贝到MLDONKEY服务器失败!!!')
        #pass
    os.remove(filename)
    #开始任务
    startBT('/root/.mldonkey/torrents/upload/' + btFile.name.encode('utf-8'))
    
    #插入
    id = clct_preresource.insert(resource.getInsertDict())
    id = str(id)
    return HttpResponseRedirect('update?id='+id)


if __name__ == '__main__':
    pass