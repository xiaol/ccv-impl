#coding=utf-8
__author__ = 'ding'
import sys
sys.path += ['/usr/local/apache2/djangoapp/videoCMS']
print sys.path

from pymongo import Connection
import re,urlparse
from gevent import monkey
monkey.patch_socket()
from videoCMS.common.HttpUtil import get_html
from urllib2 import HTTPError
from gevent.pool import Pool


con = Connection('h37:20010')
clct_resource= con.tiercel.resource


def r1(pattern, text):
    m = re.search(pattern, text)
    if m:
        return m.group(1)

def get_videoId(url):
    html = get_html(url)
    videoId = r1(r'''["']{0,1}video[Ii]d["']{0,1}[:=]["']([\w\d]+)["']''', html)
    tvId = r1(r'''tv[iI]d[:=]["']{0,1}(\d+)''',html)
    return tvId+'__'+videoId



'''
检查新视频，如果有存在的将重复老视频，就老视频更新为新的videoId，并删除新的
'''
def changeNewVideoId():
    result = clct_resource.find({'videoType':'iqiyi'},{'videoId':1,'resourceUrl':1})
    for resource in result:
        if not resource['videoId'] :continue
        if resource['videoId'].find('__') == -1:
            continue
        tvid,videoIdOld = resource['videoId'].split('__')
        if clct_resource.find_one({'videoType':'iqiyi','videoId':videoIdOld},{'_id':1}):
            print videoIdOld,'=>',resource['videoId']
            clct_resource.remove({'videoType':'iqiyi','videoId':resource['videoId']})
            clct_resource.update({'videoType':'iqiyi','videoId':videoIdOld},{'$set':{
                'videoId':resource['videoId']
            }})


'''
检查老视频，如果有url，更新为新视频的
'''
def changeOldVideoId_proc(resource):
    print '...'
    if not resource['videoId'] :
        return
    if resource['videoId'].find('__') != -1:
        return
    if not resource['resourceUrl']:
        return
    try:
        videoId = get_videoId(resource['resourceUrl'])
    except HTTPError,e:
        print resource['resourceUrl']
        print e
        if e.code == 404:
            print '404 delete'
            clct_resource.remove({'resourceUrl':resource['resourceUrl']})
        return
    except:
        return

    print resource['videoId'],'=>',videoId
    #如果存在新的，删除新的
    if clct_resource.find_one({'videoType':'iqiyi','videoId':videoId},{'_id':1}):
        print '删除新视频'
        clct_resource.remove({'videoType':'iqiyi','videoId':videoId})

    clct_resource.update({'videoType':'iqiyi','videoId':resource['videoId']},{'$set':{
             'videoId':videoId
         }})
    return True

'''
检查新视频
'''
def changeOldVideoId():
    result = clct_resource.find({'videoType':'iqiyi'},{'videoId':1,'resourceUrl':1})
    result = list(result)
    print len(result)
    pool = Pool(10)
    print pool.map(changeOldVideoId_proc,result)


'''
修复 videoId出错的视频
'''

def fixVideoIdJAVA():
    result = clct_resource.find({'videoType':'iqiyi','videoId':{'$regex':'Object'}},{'videoId':1,'resourceUrl':1})
    for resource in result:
        videoId = get_videoId(resource['resourceUrl'])
        print resource['videoId'],'=>',videoId


#changeOldVideoId()
#changeNewVideoId()
fixVideoIdJAVA()