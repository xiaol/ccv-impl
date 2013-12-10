#coding=utf8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import json,StringIO,re
from videoCMS.conf import clct_tag,IMAGE_DIR,IMG_INTERFACE,IMG_INTERFACE_FF
from videoCMS.conf import CHANNEL_IMAGE_WIDTH,CHANNEL_IMAGE_HEIGHT,CHANNEL_TYPE_LIST
from bson import ObjectId
from videoCMS.common.Domain import Tag
from videoCMS.common.common import Obj2Str
from videoCMS.common.ImageUtil import imgconvert

def getSkipLimit(DICT,skip=0,limit=10):
    _skip = DICT.get('skip',skip)
    _limit = DICT.get('limit',limit)
    return _skip,_limit



def index(request):
    spec = {}
    DICT = {}
    page = int(request.GET['page']) if request.GET.get('page','') != '' else 1
    limit =int(request.GET['len']) if request.GET.get('len','') != '' else 10
    
    name = request.GET.get('name','')
    mongo = request.GET.get('mongo','')
    id = request.GET.get('id','')
    skip = limit * (page - 1)
    
    if id != '':
        spec['_id'] = ObjectId(id)
    elif name != '':
        spec['name'] = re.compile(name)
    elif mongo != '':
        spec = json.loads(mongo)

    tagList = list(clct_tag.find(spec).sort([('_id',-1)]).skip(skip).limit(limit))
    for one in tagList:
        one['id'] = str(one['_id'])
        one.pop('_id')
    
    DICT = {}
    
    DICT['page'] = page
    DICT['len'] = limit
    DICT['nextPage'] = page + 1
    DICT['prePage'] = page-1 if page>1 else 1
    DICT['name'] = name
    DICT['id'] = id
    DICT['mongo'] = mongo
    DICT['findNum'] = clct_tag.find(spec).count()
    DICT['tagList'] = tagList
    DICT['navPage'] = 'tag'
    return render_to_response('tag.htm',DICT,context_instance=RequestContext(request))


def update(request):
    id = request.GET.get('id','')
    if request.method == "GET":
        channel = clct_tag.find_one({'_id':ObjectId(id)})
        DICT = Obj2Str(channel)
        DICT['info'] = ''
        DICT['update'] = True
        DICT['navPage'] = 'tag'
        return render_to_response('tagUpdate.htm',DICT,context_instance=RequestContext(request))
    
    #更新
    channel = Tag()
    channel['name'] = request.POST.get('name')
    
    clct_tag.update({'_id':ObjectId(id)},{'$set':channel.getUpdateDict()})
    return HttpResponseRedirect('update?id='+id)



def add(request):
    if request.method == "GET":
        DICT = {}
        DICT['info'] = ''
        DICT['navPage'] = 'tag'
        return render_to_response('tagUpdate.htm',DICT,context_instance=RequestContext(request))
    
    channel  = Tag()
    channel['name'] = request.POST['name']
    if channel['name'] == '':
        raise Exception('频道名 不能为空')
    id = clct_tag.insert(channel.getInsertDict())
    id = str(id)
    #保存封面
    return HttpResponseRedirect('update?id='+id)

