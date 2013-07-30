from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from videoCMS.conf import userList
from videoCMS.conf import clct_channel,clct_resource
from bson import ObjectId


def index(request):
    DICT = {}
    
    id = request.GET.get('id')
    resource = clct_resource.find_one({'_id':ObjectId(id) })
    if not resource:
    	pass
    DICT['videoType'] = resource['videoType']
    DICT['videoId'] = resource['videoId']
    
    if resource['videoType'] in [u'huohua', u'bt' ,u'torrent']:
        DICT['videoUrl'] = 'http://test.weiweimeishi.com/' + resource['videoId']
        return render_to_response('share_resource.htm',DICT)
    return HttpResponseRedirect(resource['resourceUrl'])
    
