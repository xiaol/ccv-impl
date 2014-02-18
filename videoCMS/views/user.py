from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from videoCMS.conf import userList,clct_cmsEditor
from login import NeedLogin



@NeedLogin
def index(request):
    DICT = {}
    DICT['info'] = ''

    uid = int(request.GET.get('id',None))
    if uid == None: uid = request.session['id']
    editor = clct_cmsEditor.find_one({'id':uid})
    DICT.update(editor)

    return render_to_response('userIndex.htm',DICT,context_instance=RequestContext(request))


@NeedLogin
def add(request):
    DICT = {}
    DICT['info'] = ''

    if request.method == 'GET':
        return render_to_response('userIndex.htm',DICT,context_instance=RequestContext(request))


    return HttpResponseRedirect('/user/index?id=')

@NeedLogin
def list(reqyest):
    pass