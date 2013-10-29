#coding=utf-8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from videoCMS.conf import userList,clct_resource,IMG_INTERFACE_FF
from videoCMS.common.HttpUtil import getVideoUrl
from videoCMS.views.resource import saveResourceImage
import base64,Image
from bson import ObjectId

def play(request):
    DICT = {}
    videoId = request.GET.get('videoId')
    videoType = request.GET.get('videoType')

    resource = clct_resource.find_one({'videoType':videoType,'videoId':videoId})
    resourceId = str(resource['_id'])

    if request.method == 'GET':
        DICT['curImage'] = IMG_INTERFACE_FF%('600','*',resource['resourceImageUrl'])

        urls = getVideoUrl(videoType,videoId)
        if urls:
            DICT['videoUrl'] = urls[0]
        else:
            return HttpResponse('无法检测到视频地址，请到原网页观看')
        return render_to_response('videoPlay.htm',DICT)

    img = request.POST.get('image')[22:]
    img = base64.decodestring(img)
    try:
        Image.open(img)
    except:
        return HttpResponse('图片不正确！')
    file = saveResourceImage(img,resourceId)
    clct_resource.update({'_id':ObjectId(resourceId)},{'$set':{'resourceImageUrl':file}})

    return HttpResponseRedirect(request.get_full_path())
