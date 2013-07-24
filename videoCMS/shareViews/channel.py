from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from videoCMS.conf import userList



def index(request):
    DICT = {}
    
    return render_to_response('shareDir/resoure.html',DICT)