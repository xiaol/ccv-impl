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
        startSearch('handles.handle_yyets_tv', channelId, url, season, yyetsEncode, downMode)
'''
def main_japanKorea():
    # 幽灵女友
    startSearch('handles.handle_yyets_tv',100247, 'http://www.yyets.com/resource/29659',"","RMVB","ed2k")
    # 飞翔情报室【抢先版】
    startSearch('handles.handle_yyets_tv',60032, 'http://www.yyets.com/resource/29716',"","RMVB","ed2k")
    # 35岁的高中生【抢先版】
    startSearch('handles.handle_yyets_tv',60030, 'http://www.yyets.com/resource/29707',"","RMVB","ed2k")
    # 一吻定情【抢先版】
    startSearch('handles.handle_yyets_tv',60028, 'http://www.yyets.com/resource/29582',"","MP4","ed2k")
    # TAKE FIVE 我们能盗取爱吗【抢先版】
    startSearch('handles.handle_yyets_tv',60026, 'http://www.yyets.com/resource/29774',"","RMVB","ed2k")
    # 最后的灰姑娘【抢先版】
    startSearch('handles.handle_yyets_tv',60024, 'http://www.yyets.com/resource/29681',"","RMVB","ed2k")
    # 神探伽利略2【抢先版】
    startSearch('handles.handle_yyets_tv',60021, 'http://www.yyets.com/resource/29725',"","RMVB","ed2k")	


def main():
    # 一吻定情【抢先版】 首播
    #startSearch('handles.handle_yyets_tv',100419, 'http://www.yyets.com/resource/29582',"","MP4","ed2k",True)
    #汉尼拔首播
    startSearch("handles.handle_yyets",100407,"http://www.yyets.com/resource/28764","1","MP4","ed2k",True)

def main2():
    #复仇者集结 第一季
    #startSearch("handles.handle_yyets",100248,"http://www.yyets.com/resource/30010","1","MP4","ed2k",False)
    #日常工作 第4季
    #startSearch("handles.handle_yyets",100244,"http://www.yyets.com/resource/29975","4","720P","ed2k",False)
    #妙女神 第4季
    #startSearch("handles.handle_yyets_tv",100210,"http://www.yyets.com/resource/10588","4","HDTV","ed2k",False)
    #小律师大作为 第3季
    #startSearch("handles.handle_yyets_tv",100209,"http://www.yyets.com/resource/10857","3","MP4","ed2k",False)
    #真爱如血 第6季
    #startSearch("handles.handle_yyets_tv",100208,"http://www.yyets.com/resource/10878","6","MP4","ed2k",False)
    #黑名单 第7季
    #startSearch("handles.handle_yyets_tv",100205,"http://www.yyets.com/resource/10875","7","MP4","ed2k",False)
    #金麦侦探社 第1季
    #startSearch("handles.handle_yyets_tv",100206,"http://www.yyets.com/resource/29524","1","HDTV","ed2k",False)
    #谋杀 第3季
    #startSearch("handles.handle_yyets_tv",100203,"http://www.yyets.com/resource/11114","3","MP4","ed2k",False)
    #少男奶爸 第2季
    #startSearch("handles.handle_yyets_tv",100202,"http://www.yyets.com/resource/28547","2","MP4","ed2k",False)
    #罪案第六感 第2季
    startSearch("handles.handle_yyets_tv",100211,"http://www.yyets.com/resource/26588","2","MP4","ed2k",False)
'''
if __name__ == '__main__':
    #main_japanKorea()
    #main2()
    pass