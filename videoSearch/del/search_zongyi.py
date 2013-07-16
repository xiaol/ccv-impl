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
    ret  = clct_resource.insert(resouceList)
    '''新增 截图任务'''
    for id,resource in zip(ret,resouceList):
        mp4box = True if resource['videoType'] == 'sohu_url' else False
        addVideoInfoTask(resource['channelId'],str(id),resource['videoId'],resource['videoType'],mp4box)

def startSearch(handleName,url,channelId):
    #获取模块
    __import__(handleName)
    module = sys.modules[handleName]
    channel = clct_channel.find_one({'channelId':channelId})
    resourceImageUrl = channel['resourceImageUrl']
    tvNumber = channel['tvNumber']
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
        insertResouce(result,channelId)

def handle(channelId,handleName,url):
    
    channel = clct_channel.find_one({'channelId':channelId})
    channelId = channel['channelId']
    if handleName == 'youkuZongyi':
        startSearch('handles.handle_youku_zongyi', url, channelId)
    elif handleName == 'iqiyiZongyi':
        startSearch('handles.handle_iqiyi_zongyi', url, channelId)


'''
def main_youku():
    #爱玩客
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z92d9eae05af211e2b16f.html',100159)
    #娱乐百分百
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z8fad81de2d6011e296ac.html',100139)
    #国光帮帮忙
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z5ca3d0742d4f11e2b356.html',100138)
    #我们约会吧
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_zde3354522d6311e2b356.html',100151)
    #超级访问
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z806d618c2d6d11e29498.html',100150)
    #转身遇到TA
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_zf904c9705df411e29498.html',100149)
    #星跳水立方
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_zc8725626907411e29498.html',100148)
    #我为歌狂
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_ze48cf80e62d211e29013.html',100147)
    #晓说
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z64feb2249b8211e296da.html',100145)
    #中国梦想秀第5季
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z0749ac7a905f11e29498.html',100144)
    #中国梦之声
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z50542a08976711e2b356.html',100143)
    #中国星跳跃
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z320ba4b27b0c11e2b16f.html',100029)
    #百变大咖秀
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z779fb5c8a25211e296da.html',100028)
    #非常完美
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_zc62716a62d5811e2b356.html',100027)
    #天天向上
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z9510781e2d4411e296ac.html',100026)
    #舞出我人生
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_zf9ddea305a2411e29013.html',100025)
    #今晚80后脱口秀
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z219ead1e31dc11e2b52a.html',100024)
    #中国最强音
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_zcb529c9c4dc211e29013.html',100023)
    #快乐大本营
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_zd18a7caa2d4311e29498.html',100022)
    #荒野求生秘技
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z7b5ce36031dd11e2b2ac.html',100181)
    #明星夫妻秀
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_zab71a2382d5111e2b16f.html',100177)
    #不朽的名曲
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_za2eb278a346b11e29013.html',100180)
    #赤脚的朋友们
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z134661e89ff611e2b2ac.html',100176)
    #两天一夜
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z7870e70c2d6211e2b52a.html',100174)
    #话神
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z69966742799911e2b2ac.html',100172)
    #人气歌谣
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z7864f1e82d5011e2b2ac.html',100171)
    #音乐银行
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z3ed1f9f22d5111e2b356.html',100142)
    #Running Man
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z1b477bfe2fba11e2b16f.html',100275)
    #Star King
    startSearch('handles.handle_youku_zongyi','http://www.youku.com/show_page/id_z3ee82ab42d5711e296ac.html',100135)
'''
    
'''
def main_iqiyi():
    #TVBS哈新闻
    startSearch('handles.handle_iqiyi_zongyi', 'http://cache.video.qiyi.com/sdvlst/6/1300002003/2013/?cb=scDtVdListC',100167)
    #全民大笑花
    startSearch('handles.handle_iqiyi_zongyi', 'http://cache.video.qiyi.com/sdvlst/6/1300002143/2013/?cb=scDtVdListC',100158)
    #大学生了没
    startSearch('handles.handle_iqiyi_zongyi', 'http://cache.video.qiyi.com/sdvlst/6/1300000225/2013/?cb=scDtVdListC',100141)
    #女人我最大
    startSearch('handles.handle_iqiyi_zongyi', 'http://cache.video.qiyi.com/sdvlst/6/1300000927/2013/?cb=scDtVdListC',100140)
    #SS小燕之夜
    startSearch('handles.handle_iqiyi_zongyi', 'http://cache.video.qiyi.com/sdvlst/6/1300000950/2013/?cb=scDtVdListC',100133)
    
    #非你莫属
    startSearch('handles.handle_iqiyi_zongyi', 'http://cache.video.qiyi.com/sdvlst/6/1300000289/2013/?cb=scDtVdListC',100154)
    #武林风
    startSearch('handles.handle_iqiyi_zongyi', 'http://cache.video.qiyi.com/sdvlst/6/1300000354/2013/?cb=scDtVdListC',100153)
    #非常静距离
    startSearch('handles.handle_iqiyi_zongyi', 'http://cache.video.qiyi.com/sdvlst/6/1300000252/2013/?cb=scDtVdListC',100152)
    #非诚勿扰
    startSearch('handles.handle_iqiyi_zongyi', 'http://cache.video.qiyi.com/sdvlst/6/1300000205/2013/?cb=scDtVdListC',100146)
    
    #无限挑战
    startSearch('handles.handle_iqiyi_zongyi', 'http://cache.video.qiyi.com/sdvlst/6/1300001919/2013/?cb=scDtVdListC',100179)
    #我们结婚了 世界版
    startSearch('handles.handle_iqiyi_zongyi', 'http://cache.video.qiyi.com/sdvlst/6/1300002020/2013/?cb=scDtVdListC',100134)
    #
    #startSearch('handles.handle_iqiyi_zongyi', '',0000)
'''

if __name__ == '__main__':
    pass
    #main_youku()
    #main_iqiyi()
#    pass
#    name = 'handles.handle_revenge2'
#    __import__('handles.handle_revenge2')
#    import sys
#    print sys.modules[name]