__author__ = 'ding'

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
    videoId = r1(r'''["']{0,1}video[Ii]d["']{0,1}[:=]["']([^"']+)["']''', html)
    tvId = r1(r'''tv[iI]d[:=]["']{0,1}(\d+)''',html)
    return tvId+'__'+videoId


def changeNewVideoId():
    result = clct_resource.find({'videoType':'iqiyi'},{'videoId':1,'resourceUrl':1})
    for resource in result:
        if not resource['videoId'] :continue
        if resource['videoId'].find('__') == -1:
            continue
        tvid,videoIdOld = resource['videoId'].split('__')
        if clct_resource.find_one({'videoType':'iqiyi','videoId':videoIdOld}):
            print videoIdOld,'=>',resource['videoId']
            clct_resource.remove({'videoType':'iqiyi','videoId':resource['videoId']})
            clct_resource.update({'videoType':'iqiyi','videoId':videoIdOld},{'$set':{
                'videoId':resource['videoId']
            }})



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
    clct_resource.update({'videoType':'iqiyi','videoId':resource['videoId']},{'$set':{
             'videoId':videoId
         }})
    return True

def changeOldVideoId():
    result = clct_resource.find({'videoType':'iqiyi'},{'videoId':1,'resourceUrl':1})
    result = list(result)
    print len(result)
    pool = Pool(10)
    print pool.map(changeOldVideoId_proc,result)


changeOldVideoId()