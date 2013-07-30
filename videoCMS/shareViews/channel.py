from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from videoCMS.conf import userList,clct_channel,clct_resource
from bson import ObjectId


def index(request):
    DICT = {}
    
    id = request.GET.get('id')
    channel = clct_channel.find_one({'_id':ObjectId(id) })
    resource = clct_resource.find_one({'channelId':str(channel['_id'])})
    DICT = channel
    if resource:
        DICT['videoType'] = resource['videoType']
        DICT['videoId'] = resource['videoId']
        if resource['videoType'] in [u'huohua', u'bt' ,u'torrent']:
            DICT['videoUrl'] = 'http://test.weiweimeishi.com/' + resource['videoId']
        else:
            DICT['videoUrl'] = resource['resourceUrl']

    
    return render_to_response('shareDir/share_channel.htm',DICT)