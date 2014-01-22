#coding=utf-8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from videoCMS.conf import clct_setting
from videoCMS.common.Domain import Setting

def POST2Setting(request):
    setting = Setting()
    setting['hotSearch'] = filter(lambda a:a!='',request.POST.get('hotSearch').strip().replace('，',',').split(','))
    setting['firstTag'] = request.POST.get('firstTag')
    return setting

def update(request):
    DICT = {}
    DICT['info'] = ''

    if request.method == 'GET':
        setting = clct_setting.find_one()
        setting['hotSearch'] = ','.join(setting['hotSearch'])
        DICT.update(setting)
        return render_to_response('setting.htm',DICT,context_instance=RequestContext(request))

    setting = POST2Setting(request)
    clct_setting.update({},setting.getUpdateDict())

    return HttpResponseRedirect('update')