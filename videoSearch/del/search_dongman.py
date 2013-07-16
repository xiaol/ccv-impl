#coding=utf-8
from setting import clct_channel,clct_resource
import imp,sys
from pprint import pprint
from common.common import getCurTime
from common.videoInfoTask import addVideoInfoTask

def insertResouce(resouceList,channelId):
    #更新时间 频道updateTime
    clct_channel.update({'channelId':channelId},{'$set':{'tvNumber':resouceList[0]['number'],\
                                                         'subtitle':'已更新至：'+str(resouceList[0]['number']),'updateTime':getCurTime()}})
    #入库
    t = getCurTime()
    for resource in resouceList:
        resource['createTime'] = t
    ret = clct_resource.insert(resouceList)
    '''新增 截图任务'''
    for id,resource in zip(ret,resouceList):
        mp4box = True if resource['videoType'] == 'sohu_url' else False
        addVideoInfoTask(resource['channelId'],str(id),resource['videoId'],resource['videoType'],mp4box)
    

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


def handle(channelId,handleName,url):
    channel = clct_channel.find_one({'channelId':channelId})
    channelId = channel['channelId']
    if handleName == 'youkuDongman':
        startSearch('handles.handle_youku_dongman', url, channelId)
    elif handleName == 'tudouDongman':
        startSearch('handles.handle_tudou', url,channelId)
    elif handleName == 'sohuDongman':
        startSearch("handles.handle_sohu_dongman", url,channelId)
    elif handleName == 'iqiyiDongman':
        startSearch("handles.handle_iqiyi_dongman", url,channelId)
        
def main_tudou():
    #我叫MT第六季
    startSearch('handles.handle_tudou', 'http://www.tudou.com/albumcover/igSsjreLfok.html',100217)
    # 火影忍者
    startSearch('handles.handle_tudou', 'http://www.tudou.com/albumcover/Lqfme5hSolM.html',100223)
    

def main_sohu():
    #圣斗士星矢Ω
    startSearch('handles.handle_sohu_dongman', 'http://tv.sohu.com/s2013/sdsxsomg/',100246)
    #全职猎人重制版
    startSearch('handles.handle_sohu_dongman', 'http://tv.sohu.com/s2012/hunter/',100245)
    #海贼王
    startSearch('handles.handle_sohu_dongman', 'http://tv.sohu.com/s2013/onepiece/',100224)


    

def main_iqiyi():
    #哆啦a梦
    startSearch('handles.handle_iqiyi_dongman','http://www.iqiyi.com/dongman/dlam.html',100035)
    #进击的巨人
    startSearch('handles.handle_iqiyi_dongman','http://www.iqiyi.com/dongman/jjdjr.html',100036)
    #侠岚
    startSearch('handles.handle_iqiyi_dongman','http://www.iqiyi.com/dongman/xl.html',100242)
    #熊出没之环球大冒险
    startSearch('handles.handle_iqiyi_dongman','http://www.iqiyi.com/dongman/xcmzhqdmx.html',100241)
    #约会大作战
    startSearch('handles.handle_iqiyi_dongman','http://www.iqiyi.com/dongman/yhdzz.html',100240)
    #花牌情缘2
    startSearch('handles.handle_iqiyi_dongman','http://www.iqiyi.com/dongman/hpqy2.html',100239)
    #恶之华
    startSearch('handles.handle_iqiyi_dongman','http://www.iqiyi.com/dongman/ezh.html',100238)
    #某科学的超电磁炮S 
    startSearch('handles.handle_iqiyi_dongman','http://www.iqiyi.com/dongman/mkxdcdcps.html',100237)
    #机动战士高达SEED DESTINY HD重制
    startSearch('handles.handle_iqiyi_dongman','http://www.iqiyi.com/dongman/seeddestinyhd.html',100236)
    #打工吧 魔王大人
    startSearch('handles.handle_iqiyi_dongman','http://www.iqiyi.com/dongman/dgmw.html',100235)
    #恶魔幸存者2
    startSearch('handles.handle_iqiyi_dongman','http://www.iqiyi.com/dongman/ds2a.html',100234)
    #革命机Valvrave
    startSearch('handles.handle_iqiyi_dongman','http://www.iqiyi.com/dongman/valvrave.html',100233)
    #YUYU式
    startSearch('handles.handle_iqiyi_dongman','http://www.iqiyi.com/dongman/yuyushiki.html',100232)


def main_youku():
    #我的青春恋爱物语果然有问题
    startSearch('handles.handle_youku_dongman','http://www.youku.com/show_page/id_zb11934c66ebf11e29498.html',100252)
    #霹雳侠影之轰动武林
    startSearch('handles.handle_youku_dongman','http://www.youku.com/show_page/id_zf33e2e705bd111e2b356.html',100253)
    #RDG濒危物种少女
    startSearch('handles.handle_youku_dongman','http://www.youku.com/show_page/id_z7f0f6662322e11e2b2ac.html',100254)
    #写真女友 TV版
    startSearch('handles.handle_youku_dongman','http://www.youku.com/show_page/id_z9f1d74bc7bcb11e29013.html',100251)
    #头文字D 第5部
    startSearch('handles.handle_youku_dongman','http://www.youku.com/show_page/id_z17f586dc26ee11e2b2ac.html',100250)
    #变态王子与不笑猫
    startSearch('handles.handle_youku_dongman','http://www.youku.com/show_page/id_zac3befea6d0511e2b16f.html',100249)
    #银河机攻战队
    startSearch('handles.handle_youku_dongman','http://www.youku.com/show_page/id_z48e20788862b11e2b2ac.html',100231)
    #旋风管家 第四季
    startSearch('handles.handle_youku_dongman','http://www.youku.com/show_page/id_z1c1ac7d2862e11e296ac.html',100230)
    #虫奉行 TV版
    startSearch('handles.handle_youku_dongman','http://www.youku.com/show_page/id_z4e8d0932857a11e29498.html',100229)
    #潜行吧!奈亚子W
    startSearch('handles.handle_youku_dongman','http://www.youku.com/show_page/id_z8edd1c5a7bc711e2b16f.html',100228)
    #十万个冷笑话
    startSearch('handles.handle_youku_dongman','http://www.youku.com/show_page/id_z02baa1f0cbcf11e19013.html',100227)
    #啦啦啦德玛西亚 第3季
    startSearch('handles.handle_youku_dongman','http://www.youku.com/show_page/id_zd6189466889f11e2a19e.html',100225)


    
    
    
    

if __name__ == '__main__':
    #main()
    #main_sohu()
    #main_iqiyi()
    #main_youku()
    #main_tudou()
    startSearch('handles.handle_sohu_dongman', 'http://tv.sohu.com/s2013/sdsxsomg/',100246)
