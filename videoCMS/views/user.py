from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from videoCMS.conf import *
from login import NeedLogin



@NeedLogin
def index(request):
    DICT = {}
    DICT['info'] = ''

    uid = int(request.GET.get('id',-1))
    if uid == -1: uid = request.session['id']
    editor = clct_cmsEditor.find_one({'id':uid})
    DICT.update(editor)

    resourceList = clct_resource.find({'editor':uid})

    DICT['resourceNum'] = resourceList.count()
    DICT['resourceList'] = []
    DICT['uid'] = uid
    for one in clct_resource.find({'editor':uid}).sort([('_id',-1)]).limit(10):
        one['id'] =str(one['_id'])
        DICT['resourceList'].append(one)



    return render_to_response('userIndex.htm',DICT,context_instance=RequestContext(request))


@NeedLogin
def edit(request):
    DICT = {}
    DICT['info'] = ''

    uid = int(request.GET.get('id',-1))
    if uid == -1: uid = request.session['id']
    editor = clct_cmsEditor.find_one({'id':uid})
    DICT.update(editor)

    print DICT

    return render_to_response('userEdit.htm',DICT,context_instance=RequestContext(request))


@NeedLogin
def add(request):
    DICT = {}
    DICT['info'] = ''

    if request.method == 'GET':
        return render_to_response('userIndex.htm',DICT,context_instance=RequestContext(request))


    return HttpResponseRedirect('/user/index?id=')



@NeedLogin
def list(request):
    DICT = {}
    DICT['info'] = ''
    userList = clct_cmsEditor.find()
    DICT['userList'] = userList

    return render_to_response('userList.htm',DICT,context_instance=RequestContext(request))