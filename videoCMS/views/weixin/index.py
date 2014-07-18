#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from videoCMS.common.xml_dict import xml2dict
from eventHandles import subscribe, unsubscribe, default
from infoHandles import text, image

handleMap = {
    'event': {
        'subscribe': subscribe,
        'unsubscribe': unsubscribe,
        'SCAN': default,
        'LOCATION': default,
        'CLICK': default,
        'VIEW': default,

    },
    'text': text,
    'image': image
}


def index(request):
    if request.method == 'GET':
        echostr = request.GET.get('echostr','wElcome to Zan\'s mothership')
        return HttpResponse(echostr)
    else:
        print request.get_full_path()
        print request.body
        msg = xml2dict(request.body)

        if msg['MsgType'] not in handleMap:
            raise Exception('MsgType %s ' % msg['MsgType'])
        if msg['MsgType'] == 'event':
            if msg['Event'] not in handleMap['event']:
                raise Exception('Event %s ' % msg['Event'])
            return HttpResponse(handleMap['event'][msg['Event']](msg))
        else:
            return HttpResponse(handleMap[msg['MsgType']](msg))
