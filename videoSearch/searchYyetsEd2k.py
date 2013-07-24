#coding=utf-8
from setting import clct_preresource,clct_resource,clct_channel
import sys,os,urllib
from ed2k.telnet import *
from common.common import getCurTime
from pprint import pprint

def checkWatchService():
    print 'checkWatchService..'
    p = os.popen('ps axu|grep "watchDownLoad"')
    result =  p.read()
    if result.find('python') == -1:
        print '[warnnig] watchDownload is not running!'
    else:
        print 'ok..'

def insertPreResouce(resource , force = False):
    #force 为True时 强制进入 preresource 列表
    if not force:
        if clct_preresource.find_one({'resourceUrl':resource['resourceUrl']}) != None:
            print 'exist in download queue...exit'
            return
        if clct_resource.find_one({'resourceUrl':resource['resourceUrl']}) != None:
            print 'downloaded...exit'
            return
    clct_preresource.insert(resource)




def startSearch(handleName,channelId,url,season=None,format="MP4",type="ed2k",force = True):
    __import__(handleName)
    module = sys.modules[handleName]
    resources = module.extractTasks(url,channelId,season,format,type)
    
    #发送到MLDonkey 然后 下载
    for resource in resources:
        pprint(resource)
        if type == 'ed2k':
            startEd2k(resource['resourceUrl'].encode('utf-8'))
            insertPreResouce(resource,force)
    checkWatchService()


def handle(channelId,handleName,url):
    channel = clct_channel.find_one({'channelId':channelId})
    channelId = channel['channelId']
    season = channel['yyetsSeason']
    yyetsEncode = channel['yyetsEncode']
    downMode = channel['yyetsDownMode']
    
    if handleName == 'yyetsTv':
        #print 'handles.handle_yyets_tv', channelId, url, season, yyetsEncode, downMode
        startSearch('handles.handle_yyets', channelId, url, season, yyetsEncode, downMode)

def main():
#    #权利的游戏
    startSearch("handles.handle_yyets",100042,"http://www.yyets.com/resource/27963","2","HDTV","ed2k")
    #护士当家
    startSearch("handles.handle_yyets",100041,"http://www.yyets.com/resource/26506","5","HDTV","ed2k")
    #军嫂
    startSearch("handles.handle_yyets",100040,"http://www.yyets.com/resource/26703","7","HDTV","ed2k")



if __name__ == '__main__':
    main()