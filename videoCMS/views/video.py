from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from videoCMS.conf import userList

def play(request):
    DICT = {}
    url = request.GET.get('url')
    DICT['videoUrl'] = 'http://60.28.29.47:8015/' +url
    
    return render_to_response('videoPlay.htm',DICT)

