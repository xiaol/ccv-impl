#coding=utf-8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from videoCMS.conf import userList
from videoCMS.conf import clct_channel,clct_resource
from bson import ObjectId
from videoCMS.common.HttpUtil import getVideoUrl


def index(request):
    DICT = {}
    
    id = request.GET.get('id')
    resource = clct_resource.find_one({'_id':ObjectId(id) })
    if not resource:
    	return HttpResponse("视频被和谐了唉...")

    channel = clct_channel.find_one({'channelId':resource['channelId'] })

    channel['detailLeadingRole'] = '/'.join(channel['detailLeadingRole'])
    channel['detailMovieCategory'] = '/'.join(channel['detailMovieCategory'])

    DICT = channel
    if resource:
        DICT['starList'] = [True] * int(channel['detaildoubanScore']/2)
        DICT['starList'].extend([False] * (5-len(DICT['starList'])))
        DICT['videoType'] = resource['videoType']
        DICT['videoId'] = resource['videoId']
        DICT['channelName'] = channel["channelName"]
        DICT['resourceImageUrl'] = "http://47.weiweimeishi.com/huohua_v2/imageinterfacev2/api/interface/image/disk/get/*/*/" + resource['resourceImageUrl']
        if resource['videoType'] in [u'huohua', u'bt' ,u'torrent']:
            DICT['videoUrl'] = 'http://test.weiweimeishi.com/' + resource['videoId']
        else:
            videoUrl = getVideoUrl(resource['videoType'], resource['videoId'])
            if resource['videoType'] == u'baidupan' or len(videoUrl) != 0 and videoUrl.find('.mp4') != -1:
                DICT['videoUrl'] = videoUrl[0]
        if 'videoUrl' not in DICT:
            DICT['videoUrl'] = resource['resourceUrl']

    DICT['apkUrl'] = 'http://www.weiweimeishi.com/static/file/PocketPlayer1.5.1_official_website.apk'
    
    return render_to_response('share_resource.htm',DICT)
    
