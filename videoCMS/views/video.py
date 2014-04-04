#coding=utf-8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from videoCMS.conf import *
from videoCMS.common.HttpUtil import getVideoUrl,get_raw_data
from videoCMS.views.resource import saveResourceImage
import base64,Image,StringIO
from bson import ObjectId
from videoCMS.common.ImageUtil import *

def getImageStreemIO(url_or_data):
    if url_or_data.startswith('http://'):
        return StringIO.StringIO(get_raw_data(url_or_data))
    else:
        img = url_or_data[22:]
        return StringIO.StringIO(base64.decodestring(img))


def style_1(request):
    img = Image.open(getImageStreemIO(request.POST.get('image1')))
    return img


def style_2(request):
    '''
     1,1,1 拼图
    '''
    img1 = Image.open(getImageStreemIO(request.POST.get('image1')))
    img2 = Image.open(getImageStreemIO(request.POST.get('image2')))
    img3 = Image.open(getImageStreemIO(request.POST.get('image3')))


    img1 = imgconvert(img1,None,252,432)
    img2 = imgconvert(img2,None,252,432)
    img3 = imgconvert(img3,None,252,432)

    img = Image.new('RGB',(768,432),'white')
    img.paste(img1,(0,0,252,432))
    img.paste(img2,(258,0,510,432))
    img.paste(img3,(516,0,768,432))
    return img

def style_3(request):
    '''
     1,2 拼图
    '''
    img1 = Image.open(getImageStreemIO(request.POST.get('image1')))
    img2 = Image.open(getImageStreemIO(request.POST.get('image2')))
    img3 = Image.open(getImageStreemIO(request.POST.get('image3')))


    img1 = imgconvert(img1,None,432,432)
    img2 = imgconvert(img2,None,330,213)
    img3 = imgconvert(img3,None,330,213)

    img = Image.new('RGB',(768,432),'white')
    img.paste(img1,(0,0,432,432))
    img.paste(img2,(436,0,768,213))
    img.paste(img3,(436,219,768,432))
    return img


def style_4(request):
    '''
     1,1,1 拼图
    '''
    img1 = Image.open(getImageStreemIO(request.POST.get('image1')))
    img2 = Image.open(getImageStreemIO(request.POST.get('image2')))


    img1 = imgconvert(img1,None,382,432)
    img2 = imgconvert(img2,None,382,432)

    img = Image.new('RGB',(768,432),'white')
    img.paste(img1,(0,0,382,432))
    img.paste(img2,(386,0,768,432))
    return img

def play(request):
    DICT = {}
    videoId = request.GET.get('videoId')
    videoType = request.GET.get('videoType')

    resource = clct_resource.find_one({'videoType':videoType,'videoId':videoId})
    resourceId = str(resource['_id'])


    if request.method == 'GET':
        DICT['curImage'] = IMG_INTERFACE_FF%('600','*',resource['resourceImageUrl'])
        DICT.update(resource)

        urls = getVideoUrl(videoType,videoId)
        if urls:
            DICT['videoUrl'] = urls[0]
        else:
            return HttpResponse('无法检测到视频地址，请到原网页观看')
        return render_to_response('videoPlay.htm', DICT)
    #取消截图
    clct_videoInfoTask.remove({'resourceId': resourceId}, mulit=True)

    #拼图
    style = int(request.POST['style'])

    if style == 1:
        img = style_1(request)
    elif style == 2:
        img = style_2(request)
    elif style == 3:
        img = style_3(request)
    elif style == 4:
        img = style_4(request)

    sio = StringIO.StringIO()
    img.save(sio,'jpeg',quality=90)
    file = saveResourceImage(sio.getvalue(), resourceId)
    print file
    clct_resource.update({'_id': ObjectId(resourceId)}, {'$set': {'resourceImageUrl': file, 'snapshot': ''}})

    return HttpResponseRedirect(request.get_full_path())
