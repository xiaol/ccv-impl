#coding=utf-8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from videoCMS.conf import userList
from videoCMS.common.HttpUtil import getVideoUrl

def play(request):
    DICT = {}
    #url = request.GET.get('url')
    #DICT['videoUrl'] = 'http://60.28.29.47:8015/' +url
    videoId = request.GET.get('videoId')
    videoType = request.GET.get('videoType')

    urls = getVideoUrl(videoType,videoId)

    if urls:
        DICT['videoUrl'] = urls[0]
    else:
        return HttpResponse('无法检测到视频地址，请到原网页观看')
    return render_to_response('videoPlay.htm',DICT)

