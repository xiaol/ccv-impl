#coding=utf8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import json,StringIO,re
from videoCMS.conf import clct_category,IMAGE_DIR,IMG_INTERFACE,IMG_INTERFACE_FF,clct_channel,clct_resource
from videoCMS.conf import CHANNEL_IMAGE_WIDTH,CHANNEL_IMAGE_HEIGHT,CATEGORY_TYPE_MAP,CATEGORY_VIDEO_CLASS_MAP
from bson import ObjectId
from videoCMS.common.Domain import Category
from videoCMS.common.common import Obj2Str,getCurTime,formatHumanTime
from login import NeedLogin
from videoCMS.common.ImageUtil import imgconvert
from pymongo.errors import OperationFailure


def getSkipLimit(DICT,skip=0,limit=10):
    _skip = DICT.get('skip',skip)
    _limit = DICT.get('limit',limit)
    return _skip,_limit


@NeedLogin
def index(request):
    spec = {}
    DICT = {}
    page = int(request.GET['page']) if request.GET.get('page','') != '' else 1
    limit =int(request.GET['len']) if request.GET.get('len','') != '' else 10
    
    name = request.GET.get('name','')
    mongo = request.GET.get('mongo','')
    id = request.GET.get('id','')
    skip = limit * (page - 1)
    sort = request.GET.get('sort','')
    sortList = [('_id',-1)]
    
    if id != '':
        spec['_id'] = ObjectId(id)
    elif name != '':
        spec['categoryName'] = re.compile(name)
    elif mongo != '':
        spec = json.loads(mongo)
    if sort != "":
        if sort == 'createTime':
            sortList = [('createTime',-1)]
        elif sort == 'weight':
            sortList = [('weight',-1)]

    categoryList = list(clct_category.find(spec).sort(sortList).skip(skip).limit(limit))
    for one in categoryList:
        one['id'] = str(one['_id'])
        one.pop('_id')
        one['imageUrl'] = IMG_INTERFACE + one['imageUrl']
        one['createTime'] = formatHumanTime(one['createTime'])
        one['modifyTime'] = formatHumanTime(one['modifyTime'])
    
    
    DICT = {}
    DICT['categoryList'] = categoryList
    
    DICT['page'] = page
    DICT['len'] = limit
    DICT['nextPage'] = page + 1
    DICT['prePage'] = page-1 if page>1 else 1
    DICT['name'] = name
    DICT['id'] = id
    DICT['mongo'] = mongo
    DICT['findNum'] = clct_category.find(spec).count()
    DICT['navPage'] = 'category'
    DICT['sort'] = sort

    return render_to_response('categoryList.htm',DICT,context_instance=RequestContext(request))

@NeedLogin
def update(request):
    id = request.GET.get('id','')
    if request.method == "GET":
        category = clct_category.find_one({'_id':ObjectId(id)})
        category['imageUrl'] = IMG_INTERFACE_FF%(250,150,category['imageUrl'])
        category['logoUrl'] = IMG_INTERFACE_FF%(250,150,category['logoUrl'])
        DICT = Obj2Str(category)
        DICT['info'] = ''
        DICT['update'] = True
        DICT['categoryTypeList'] = CATEGORY_TYPE_MAP.keys()
        '''数字 转 文字'''
        for k in CATEGORY_TYPE_MAP:
            if CATEGORY_TYPE_MAP[k] == DICT['categoryType']:
                DICT['categoryType'] = k
        
        DICT['videoClassList'] = CATEGORY_VIDEO_CLASS_MAP.keys()
        for k in CATEGORY_VIDEO_CLASS_MAP:
            if CATEGORY_VIDEO_CLASS_MAP[k] == DICT['videoClass']:
                DICT['videoClass'] = k
                
        DICT['navPage'] = 'category'
        return render_to_response('categoryUpdate.htm',DICT,context_instance=RequestContext(request))
    
    oldCategory = clct_category.find_one({'_id':ObjectId(id)})
    #更新
    category = Category()
    category['categoryId'] = int(request.POST['categoryId'])
    category['categoryName'] = request.POST['categoryName']
    category['subtitle'] = request.POST['subtitle']
    category['modifyTime'] = getCurTime()
    category['weight'] = 0 if request.POST.get('weight') == '' else int(request.POST.get('weight'))
    category['categoryType'] = CATEGORY_TYPE_MAP[request.POST.get('categoryType')]
    category['videoClass'] = CATEGORY_VIDEO_CLASS_MAP[request.POST.get('videoClass')]
    category['isOnline'] = True if request.POST.get('isOnline') == u'是' else False
    category['isFirst'] = True if request.POST.get('isFirst') == u'是' else False

    #更新关联频道 categoryId aka channelType
    if oldCategory['categoryId'] != category['categoryId']:
        clct_channel.update({'channelType':oldCategory['categoryId']},{'$set':{'channelType':category['categoryId']}},multi=True)
    
    #更新关联视频的 categoryId aka channelType
    channelIds = [channel['channelId']  for channel in clct_channel.find({'channelType':category['categoryId']},{'channelId':1})]
    clct_resource.update({'channelId':{'$in':channelIds}}, {'$set':{'categoryId':category['categoryId']}},multi =True)

    #更新频道videoClass
    clct_channel.update({'channelType':category['categoryId']},{'$set':{'videoClass':category['videoClass']}},multi=True)
    

    #更新categoryType 强兴趣 段兴趣
    clct_channel.update({'channelType':category['categoryId']},{'$set':{'categoryType':category['categoryType']}},multi=True)



    #更新图片
    img = request.FILES.get('categoryImage',None)
    if img:
        category['imageUrl'] = saveCategoryImage(img.read(),id)
    img = request.FILES.get('logoUrl',None)
    if img:
        category['logoUrl'] = saveCategoryImage(img.read(),id)
    
    clct_category.update({'_id':ObjectId(id)},{'$set':category.getUpdateDict()})
    return HttpResponseRedirect('update?id='+id)


@NeedLogin
def add(request):
    if request.method == "GET":
        DICT = {}
        DICT['info'] = ''
        DICT['categoryTypeList'] = CATEGORY_TYPE_MAP.keys()
        DICT['videoClassList'] = CATEGORY_VIDEO_CLASS_MAP.keys()
        DICT['navPage'] = 'category'
        return render_to_response('categoryUpdate.htm',DICT,context_instance=RequestContext(request))
    
    category  = Category()
    if request.POST['categoryId'] == '':
        category['categoryId'] = getMaxChannelId()
    else:
        category['categoryId'] = int(request.POST['categoryId'])
    category['categoryName'] = request.POST['categoryName']
    category['subtitle'] = request.POST['subtitle']
    category['weight'] = 0 if request.POST.get('weight') == '' else int(request.POST.get('weight'))
    category['createTime'] = getCurTime()
    category['modifyTime'] = getCurTime()
    category['categoryType'] = CATEGORY_TYPE_MAP[request.POST.get('categoryType')]
    category['videoClass'] = CATEGORY_VIDEO_CLASS_MAP[request.POST.get('videoClass')]
    category['isOnline'] = True if request.POST.get('isOnline') == u'是' else False
    category['isFirst'] = True if request.POST.get('isFirst') == u'是' else False
    clct_channel.update({'channelType':category['categoryId']},{'$set':{'videoClass':category['videoClass']}},multi=True)
    if category['categoryName'] == '':
        raise Exception('分类名 不能为空')
    clct_channel.update({'channelType':category['categoryId']},{'$set':{'categoryType':category['categoryType']}},multi=True)

    id = clct_category.insert(category.getInsertDict(),safe=True)
    id = str(id)
    print request.FILES
    img = request.FILES.get('categoryImage',None)
    #保存封面
    if img:
        filename = saveCategoryImage(img.read(), id)
        clct_category.update({'_id':ObjectId(id)},{'$set':{'imageUrl':filename}})
    return HttpResponseRedirect('update?id='+id)

def getMaxChannelId():
    channel = list(clct_category.find().sort([('categoryId',-1)]).limit(1))[0]
    print channel
    return channel['categoryId'] + 1
    

def saveCategoryImage(img, id):
    '''
    #裁剪
    outimg = StringIO.StringIO()
    imgconvert(img,outimg,CHANNEL_IMAGE_WIDTH,CHANNEL_IMAGE_HEIGHT)
    #保存
    filename = 'videoCMS/channel/%s.jpg'%id
    with open(IMAGE_DIR + '/' + filename, 'wb') as f:
        f.write(outimg.getvalue())
    '''
    
    filename = 'videoCMS/category/%s.jpg'% (id+ getCurTime())
    with open(IMAGE_DIR + '/' + filename, 'wb') as f:
        f.write(img)
     
    return filename.replace('/', '_')

#===============================================
@NeedLogin
def resetWeight(request):
    categoryId = int(request.GET.get("categoryId"))
    clct_channel.update({"categoryId":categoryId},{"$set":{"weight":0}},multi=True)
    return HttpResponse("ok")


def showJson(request):
    id = request.GET.get('id')
    one = clct_category.find_one({'_id':ObjectId(id)})
    one['_id'] = str(one['_id'])
    return HttpResponse(json.dumps(one))
