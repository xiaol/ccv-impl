from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from videoCMS.conf import userList,clct_cmsMessage
from login import NeedLogin

@NeedLogin
def unread(request):
    DICT = {}
    username = request.session['username']
    result = clct_cmsMessage.find({'to':{'$in':['',username]},'readed':{'$exists':False}})
    result = list(result)
    count = len(result)

    return render_to_response('message.htm',locals(),context_instance=RequestContext(request))


@NeedLogin
def readed(request):
    DICT = {}
    username = request.session['username']
    result = clct_cmsMessage.find({'to':{'$in':['',username]}, 'readed':True})
    result = list(result)
    count = len(result)

    return render_to_response('message.htm',locals(),context_instance=RequestContext(request))


@NeedLogin
def all(request):
    DICT = {}
    username = request.session['username']
    result = clct_cmsMessage.find({'to':{'$in':['',username]}})
    result = list(result)
    count = len(result)
    return render_to_response('message.htm',locals(),context_instance=RequestContext(request))