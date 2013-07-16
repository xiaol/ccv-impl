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
#    startSearch('handles.handle_yyets',100001,'http://www.yyets.com/resource/10733',season='3',format="MP4",type="ed2k")
#    #圣城风云
#    startSearch('handles.handle_yyets',100003,'http://www.yyets.com/resource/10807',season='1',format="MP4",type="ed2k")
#    #斯巴达克斯
#    startSearch('handles.handle_yyets',100004,'http://www.yyets.com/resource/11176',season='3',format="MP4",type="ed2k")
#    #达芬奇的恶魔
#    startSearch('handles.handle_yyets',100005,'http://www.yyets.com/resource/28404',season='1',format="MP4",type="ed2k")
#    #格林
#    startSearch('handles.handle_yyets',100006,'http://www.yyets.com/resource/11080',season='2',format="MP4",type="ed2k")
#    #疑犯追踪 2
#    startSearch('handles.handle_yyets',100007,'http://www.yyets.com/resource/11009',season='2',format="MP4",type="ed2k")
#    #生活大爆炸 6
#    startSearch('handles.handle_yyets',100009,'http://www.yyets.com/resource/11005',season='6',format="MP4",type="ed2k")
#    #尼基塔 3
#    startSearch('handles.handle_yyets',100010,'http://www.yyets.com/resource/11012',season='3',format="MP4",type="ed2k")
#    #波吉亚家族 3
#    startSearch("handles.handle_yyets",100039,"http://www.yyets.com/resource/10818",season="3",format="MP4",type="ed2k")
#    #狗狗博客
#    startSearch("handles.handle_yyets",100212,"http://www.yyets.com/resource/28999","1","MP4","ed2k")
#    #十三号仓库
#    startSearch("handles.handle_yyets",100199,"http://www.yyets.com/resource/10899","4","MP4","ed2k")
#    #遗产游戏
#    startSearch("handles.handle_yyets",100200,"http://www.yyets.com/resource/30044","1","MP4","ed2k")
#    #汉尼拔
#    startSearch("handles.handle_yyets",100201,"http://www.yyets.com/resource/28764","1","MP4","ed2k")
#    #发展受阻
#    startSearch("handles.handle_yyets",100196 ,"http://www.yyets.com/resource/29372","4","MP4","ed2k")
#    #愤怒管理
#    startSearch("handles.handle_yyets",100193,"http://www.yyets.com/resource/26790","2","MP4","ed2k")
#    #约会规则
#    startSearch("handles.handle_yyets",100195,"http://www.yyets.com/resource/11079","7","MP4","ed2k")
#    #情何以堪
#    startSearch("handles.handle_yyets",100192,"http://www.yyets.com/resource/26190","3","MP4","ed2k")
#    #青春密语
#    startSearch("handles.handle_yyets",100043,"http://www.yyets.com/resource/10867","5","MP4","ed2k")
    #副总统
    startSearch("handles.handle_yyets",100042,"http://www.yyets.com/resource/27963","2","HDTV","ed2k")
    #护士当家
    startSearch("handles.handle_yyets",100041,"http://www.yyets.com/resource/26506","5","HDTV","ed2k")
    #军嫂
    startSearch("handles.handle_yyets",100040,"http://www.yyets.com/resource/26703","7","HDTV","ed2k")



if __name__ == '__main__':
    main()