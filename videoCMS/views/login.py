#coding=utf-8
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from videoCMS.conf import userList

def login(request):
    
    DICT = {}
    redirect = '/channel/index'
    
    
    if request.method == 'GET':
        if 'redirect' in request.GET and request.GET['redirect'] != '':
            redirect = request.GET['redirect']
        DICT['redirect'] = redirect

        return render_to_response('login.htm',DICT)

    if request.method == 'POST':
        if 'redirect' in request.POST and request.POST['redirect'] != '':
            redirect = request.POST['redirect']
        user = request.POST['username']
        passwd = request.POST['password']
        if (user,passwd) in userList:
            request.session['username'] = user
            return HttpResponseRedirect(redirect)
        else:
            DICT['username'] = user
            DICT['redirect'] = redirect
            DICT['info'] = 'wrong username or password' 
            return render_to_response('login.htm',DICT)
    
    return HttpResponse('xxx')


def logout(request):
    if 'username' in request.session:
        del request.session['username']
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def checkLogin(request):
    if 'username' not in request.session:
        print 'check fail'
        return False
    return True

def checkAdmin(request,special=[]):
    if request.session['username'] != 'admin' and request.session['username'] not in special:
        return False
    return True

'''
检查登陆装饰器
'''
def NeedLogin(func):
    def _func(request):
        if not checkLogin(request):
            return HttpResponseRedirect('/login?redirect='+request.get_full_path())
        return func(request)

    return _func





def custom_proc(request):
    DICT = {}
    DICT['USER_NAME'] = request.session.get('username','')
    DICT['MSG'] = '123123123123123'
    print 'xxxxxxxxxxxxxxxxx'
    return DICT