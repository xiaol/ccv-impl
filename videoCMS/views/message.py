from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from videoCMS.conf import userList,clct_cmsMessage
from login import NeedLogin
from bson import ObjectId


def getMessageNum(request):
    username = request.session['username']
    unreadNum = clct_cmsMessage.find({'to':{'$in':['',username]},'readed':{'$exists':False}}).count()
    readedNum = clct_cmsMessage.find({'to':{'$in':['',username]},'readed':True}).count()

    return {'unreadMessageNum':unreadNum,'readedMessageNum':readedNum,'allMessageNum':unreadNum+readedNum}



@NeedLogin
def unread(request):
    DICT = {}
    username = request.session['username']
    result = clct_cmsMessage.find({'to':{'$in':['',username]},'readed':{'$exists':False}}).sort([('_id',-1)])
    result = list(result)
    for one in result:one['id'] = str(one['_id'])
    count = len(result)

    return render_to_response('message.htm',locals(),context_instance=RequestContext(request,processors=[getMessageNum]))


@NeedLogin
def readed(request):
    DICT = {}
    username = request.session['username']
    result = clct_cmsMessage.find({'to':{'$in':['',username]}, 'readed':True}).sort([('_id',-1)])
    result = list(result)
    for one in result:one['id'] = str(one['_id'])
    count = len(result)

    return render_to_response('message.htm',locals(),context_instance=RequestContext(request,processors=[getMessageNum]))


@NeedLogin
def all(request):
    DICT = {}
    username = request.session['username']
    result = clct_cmsMessage.find({'to':{'$in':['',username]}}).sort([('_id',-1)])
    result = list(result)
    for one in result:one['id'] = str(one['_id'])
    count = len(result)
    return render_to_response('message.htm',locals(),context_instance=RequestContext(request,processors=[getMessageNum]))


@NeedLogin
def flagRead(request):
    clct_cmsMessage.update({'_id':ObjectId(request.GET.get('id'))},{'$set':{'readed':True}})
    return HttpResponseRedirect(request.META['HTTP_REFERER'])