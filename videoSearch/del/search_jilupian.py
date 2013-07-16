#coding=utf-8
from setting import clct_channel,clct_resource
import imp,sys
from pprint import pprint
from common.common import getCurTime
from common.videoInfoTask import addVideoInfoTask

def insertResouce(resouceList,channelId):
    #更新时间 频道updateTime
    resouceList.sort(key = lambda a:a['number'],reverse= True)
    clct_channel.update({'channelId':channelId},{'$set':{'tvNumber':resouceList[0]['number'],\
                                                         'subtitle':'已更新至：'+str(resouceList[0]['number']),'updateTime':getCurTime()}})
    #入库
    t = getCurTime()
    for resource in resouceList:
        resource['createTime'] = t
    ret = clct_resource.insert(resouceList)
    '''新增 截图任务'''
    '''for id,resource in zip(ret,resouceList):
        mp4box = True if resource['videoType'] == 'sohu_url' else False
        addVideoInfoTask(resource['channelId'],str(id),resource['videoId'],resource['videoType'],mp4box)
    '''

def startSearch(handleName,url,channelId):
    #获取模块
    __import__(handleName)
    module = sys.modules[handleName]
    channel = clct_channel.find_one({'channelId':channelId})
    tvNumber = channel['tvNumber']
    resourceImageUrl = channel['resourceImageUrl']
    #抽取
    result = module.handle(url,channelId,tvNumber)
    pprint(result)
    for one in result:
        if channel['autoOnline'] == False:
            one['isOnline'] = False
        one['resourceImageUrl'] = resourceImageUrl
        one['duration'] = channel['duration']
        
    #入库
    if len(result) != 0:
        pass
        insertResouce(result,channelId)


def main_youku():
    #克里斯·安吉尔的街头魔术
    startSearch('handles.handle_youku_jilupian','http://www.youku.com/show_page/id_z210ebcc4b50311e0a046.html',100274)
    #世界格斗术揭秘系列
    startSearch('handles.handle_youku_jilupian','http://www.youku.com/show_page/id_za50f5be4b50011e0a046.html',100273)
    #二战失落的档案
    startSearch('handles.handle_youku_jilupian','http://www.youku.com/show_page/id_z7b21c364b50311e0a046.html',100272)
    #人类消失后的世界
    startSearch('handles.handle_youku_jilupian','http://www.youku.com/show_page/id_z97a3b8f2b4ff11e0a046.html',100271)
    #科学幻想
    startSearch('handles.handle_youku_jilupian','http://www.youku.com/show_page/id_zd8902e2eb50211e0a046.html',100270)
    #空中搏斗
    startSearch('handles.handle_youku_jilupian','http://www.youku.com/show_page/id_z73f092ceb50211e0a046.html',100269)
    #神话传说
    startSearch('handles.handle_youku_jilupian','http://www.youku.com/show_page/id_z1434ee6cb50111e0a046.html',100268)
    #超级巨星
    startSearch('handles.handle_youku_jilupian','http://www.youku.com/show_page/id_zc0aac7e8b50111e0a046.html',100267)
    #PBS自然系列
    startSearch('handles.handle_youku_jilupian','http://www.youku.com/show_page/id_z926ee294020b11e2b52a.html',100266)
    #士兵突击2
    startSearch('handles.handle_youku_jilupian','http://www.youku.com/show_page/id_z3f07c51a951f11e2b16f.html',100265)
    #军情解码
    startSearch('handles.handle_youku_jilupian','http://www.youku.com/show_page/id_z47c8257c48bd11e29013.html',100264)
    #新电影传奇
    startSearch('handles.handle_youku_jilupian','http://www.youku.com/show_page/id_zd041063ab41711e0a046.html',100263)
    #真实第25小时
    startSearch('handles.handle_youku_jilupian','http://www.youku.com/show_page/id_zd304955c48f511e296ac.html',100262)
    #光阴
    startSearch('handles.handle_youku_jilupian','http://www.youku.com/show_page/id_zc09338b0958611e1b52a.html',100261)


def main_sohu():
    #新纪录
    startSearch('handles.handle_sohu_dongman', 'http://tv.sohu.com/s2012/xjl/',100260)
    #我的中国梦
    startSearch('handles.handle_sohu_dongman', 'http://tv.sohu.com/s2013/dream/',100259)
    #搜狐视频大视野
    startSearch('handles.handle_sohu_dongman', 'http://tv.sohu.com/s2011/9240/s328641340/',100258)


def main_iqiyi():
    #军情观察室
    #startSearch('handles.handle_iqiyi_jilupian', 'http://www.iqiyi.com/jilupian/jqgc.html',100160)
    #经典传奇
    startSearch('handles.handle_iqiyi_jilupian', 'http://www.iqiyi.com/jilupian/djcq.html',100256)
    
    
    
    
    

if __name__ == '__main__':
    #main()
    #main_youku()
    main_sohu()
    #main_iqiyi()
