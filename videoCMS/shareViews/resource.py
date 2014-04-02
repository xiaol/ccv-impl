#coding=utf-8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from videoCMS.conf import userList
from videoCMS.conf import clct_channel,clct_resource
from bson import ObjectId
from videoCMS.common.HttpUtil import getVideoUrl
import re

p_Android = re.compile('android')
p_IOS = re.compile('ipad|iphone')

def index(request):
    DICT = {}

    #return HttpResponse(request.get_full_path())

    if request.GET.get('id','') == '' and  request.GET.get('channelid','') != '':
        id = clct_channel.find_one({'channelId':int(request.GET['channelid'])})['_id']
        return HttpResponseRedirect('/share/channel?id='+str(id))

    id = request.GET.get('id')
    resource = clct_resource.find_one({'_id':ObjectId(id) })
    if not resource:
    	return HttpResponse("视频被和谐了唉...")

    channel = clct_channel.find_one({'channelId':resource['channelId'] })

    channel['detailLeadingRole'] = '/'.join(channel['detailLeadingRole'])
    channel['detailMovieCategory'] = '/'.join(channel['detailMovieCategory'])

    DICT = channel
    DICT['resource'] = resource
    if resource:
        DICT['starList'] = [True] * int(channel['detaildoubanScore']/2)
        DICT['starList'].extend([False] * (5-len(DICT['starList'])))
        DICT['resourceImageUrl'] = "http://47.weiweimeishi.com/huohua_v2/imageinterfacev2/api/interface/image/disk/get/*/*/" + resource['resourceImageUrl']

        videoUrl = getVideoUrl(resource['videoType'], resource['videoId'])
        if len(videoUrl) != 0 and videoUrl[0].find('.mp4') != -1:
            DICT['videoUrl'] = videoUrl[0]
        else:
            DICT['videoUrl'] = resource['resourceUrl']

        if p_IOS.search(request.META['HTTP_USER_AGENT'].lower()) != None:
            DICT['ipaUrl'] = 'http://mp.weixin.qq.com/mp/redirect?url=https://itunes.apple.com/cn/app/kou-dai-shi-pin-zi-dong-li/id737702962?ls=1&mt=8'
        elif p_Android.search(request.META['HTTP_USER_AGENT'].lower()) != None:
            DICT['apkUrl'] = 'http://weiweimeishi.lx.coop.kukuplay.com/PocketPlayer/PocketPlayer_share.apk'
    
    return render_to_response('share_resource.htm', DICT)
