#coding=utf-8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from videoCMS.conf import userList,clct_cmsMessage
from login import NeedLogin
from bson import ObjectId
from videoCMS.common.common import  getCurTime






def getMessageNum(request):
    username = request.session['username']
    uid = int(request.session['id'])
    unreadNum = clct_cmsMessage.find({'to':{'$in':['',uid]},'readed':{'$exists':False},'mark':{'$exists':False}}).count()
    readedNum = clct_cmsMessage.find({'to':{'$in':['',uid]},'readed':True}).count()
    markedNum = clct_cmsMessage.find({'to':{'$in':['',uid]},'readed':{'$exists':False},'mark':{'$exists':True}}).count()
    return {'unreadMessageNum':unreadNum,'readedMessageNum':readedNum,'allMessageNum':unreadNum+readedNum,'markedMessageNum':markedNum}



@NeedLogin
def unread(request):
    DICT = {}
    uid = request.session['id']
    result = clct_cmsMessage.find({'to':{'$in':['',uid]},'readed':{'$exists':False},'mark':{'$exists':False}}).sort([('_id',-1)])
    result = list(result)
    for one in result:one['id'] = str(one['_id'])
    count = len(result)

    return render_to_response('message.htm',locals(),context_instance=RequestContext(request,processors=[getMessageNum]))


@NeedLogin
def readed(request):
    DICT = {}
    uid = request.session['id']
    result = clct_cmsMessage.find({'to':{'$in':['',uid]}, 'readed':True}).sort([('_id',-1)])
    result = list(result)
    for one in result:one['id'] = str(one['_id'])
    count = len(result)

    return render_to_response('message.htm',locals(),context_instance=RequestContext(request,processors=[getMessageNum]))


@NeedLogin
def all(request):
    DICT = {}
    uid = request.session['id']
    result = clct_cmsMessage.find({'to':{'$in':['',uid]}}).sort([('_id',-1)])
    result = list(result)
    for one in result:one['id'] = str(one['_id'])
    count = len(result)
    return render_to_response('message.htm',locals(),context_instance=RequestContext(request,processors=[getMessageNum]))


@NeedLogin
def flagRead(request):
    clct_cmsMessage.update({'_id':ObjectId(request.GET.get('id'))},{'$set':{'readed':True}})
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@NeedLogin
def flagUnread(request):
    clct_cmsMessage.update({'_id':ObjectId(request.GET.get('id'))},{'$unset':{'readed':True}})
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def markMessage(request):
    id = request.GET['id']
    mark = request.GET['mark']
    clct_cmsMessage.update({'_id':ObjectId(id)},{'$set':{'mark':mark}})
    return  HttpResponse('ok')


@NeedLogin
def marked(request):
    DICT = {}
    uid = request.session['id']
    result = clct_cmsMessage.find({'to':{'$in':['',uid]},'readed':{'$exists':False},'mark':{'$exists':True}}).sort([('_id',-1)])
    result = list(result)
    for one in result:one['id'] = str(one['_id'])
    count = len(result)

    return render_to_response('message.htm',locals(),context_instance=RequestContext(request,processors=[getMessageNum]))
