from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from videoCMS.conf import userList

def index(request):
    DICT = {}
    DICT['info'] = ''
    DICT['username'] = request.session['username']
    return render_to_response('about.htm',DICT,context_instance=RequestContext(request))
