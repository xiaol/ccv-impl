#coding=utf-8
from setting import clct_channel,clct_resource
import imp,sys
from pprint import pprint
from common.common import getCurTime
from common.videoInfoTask import addVideoInfoTask

def insertResouce(resouceList,channelId):
    #更新时间 频道updateTime
    resouceList.sort(key = lambda a:a['number'],reverse = True)
    clct_channel.update({'channelId':channelId},{'$set':{'tvNumber':resouceList[0]['number'],\
                                                         'subtitle':'已更新至：'+str(resouceList[0]['number']),'updateTime':getCurTime()}})
    #入库
    t = getCurTime()
    for resource in resouceList:
        resource['createTime'] = t
    ret = clct_resource.insert(resouceList)
    '''新增 截图任务'''
    '''
    for id,resource in zip(ret,resouceList):
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
    for one in result:
        if channel['autoOnline'] == False:
            one['isOnline'] = False
        one['resourceImageUrl'] = resourceImageUrl
        one['duration'] = channel['duration']
    pprint(result)
    #入库
    if len(result) != 0:
        insertResouce(result,channelId)


def handle(channelId,handleName,url):
    
    channel = clct_channel.find_one({'channelId':channelId})
    channelId = channel['channelId']
    if handleName == 'youkuTv':
        startSearch('handles.handle_youku_tv', url, channelId)
    elif handleName == 'funshionTv':
        startSearch('handles.handle_funshion_tv', url,channelId)
    elif handleName == 'letvTv':
        startSearch("handles.handle_letv_tv", url,channelId)
    elif handleName == 'iqiyiTv':
        startSearch("handles.handle_iqiyi_tv", url,channelId)
    
        
def main():
    #startSearch('handles.handle_revenge2', 'http://www.iqiyi.com/dianshiju/revenge2.html',1)
    # 马永贞
    startSearch('handles.handle_youku_showPage', 'http://www.youku.com/show_page/id_z1e2a5fe0b6b511e1b16f.html',100011)
    # 爱的创可贴 2013
    startSearch('handles.handle_youku_showPage', 'http://www.youku.com/show_page/id_z3fa08c4a094311e2b16f.html',100012)
    # 唐山大地震 2013
    startSearch('handles.handle_youku_showPage', 'http://www.youku.com/show_page/id_z18a4737aea6511e0a046.html',100013)
    # 新编辑部故事 2013
    startSearch('handles.handle_youku_showPage', 'http://www.youku.com/show_page/id_zebf36546fc1e11df97c0.html',100014)
    # 金枝欲孽Ⅱ 2013
    startSearch('handles.handle_youku_showPage', 'http://www.youku.com/show_page/id_z84933d227a4911e1b2ac.html',100015)
    # 枪花 2013
    startSearch('handles.handle_youku_showPage', 'http://www.youku.com/show_page/id_z6c798516855b11e2b16f.html',100016)
    #两个爸爸 2013
    startSearch('handles.handle_youku_showPage', 'http://www.youku.com/show_page/id_z57077d9095dd11e296da.html',100017)
    #等待绽放 2013
    startSearch('handles.handle_youku_showPage', 'http://www.youku.com/show_page/id_z3f6eb098940f11e196ac.html',100018)
    #神探高伦布 2013
    startSearch('handles.handle_youku_showPage', 'http://www.youku.com/show_page/id_ze9ac2786a3a311e19498.html',100019)
    #大宅门1912 2013
    startSearch('handles.handle_youku_showPage', 'http://www.youku.com/show_page/id_z83307696561411e2a19e.html',100020)
    #仁心解码Ⅱ 2013
    startSearch('handles.handle_youku_showPage', 'http://www.youku.com/show_page/id_z247c63b2433b11e29013.html',100021)


def main2():
    #熟男有惑
    #startSearch('handles.handle_youku_tv', 'http://www.youku.com/show_page/id_z4186475cad6711e2b16f.html',100539)
    #铁血玫瑰 
    #startSearch('handles.handle_youku_tv', 'http://www.youku.com/show_page/id_z09b99cc85ac611e296ac.html',100538)
    #神探高伦布
    #startSearch('handles.handle_youku_tv', 'http://www.youku.com/show_page/id_ze9ac2786a3a311e19498.html',100537)
    #好心作怪
    #startSearch('handles.handle_youku_tv', 'http://www.youku.com/show_page/id_z95dd9e68434511e2b356.html',100536)
    #鲨鱼
    #startSearch('handles.handle_youku_tv', 'http://www.youku.com/show_page/id_zcece6e64a5a111e2b2ac.html',100535)
    #爱在春天
    #startSearch('handles.handle_youku_tv', 'http://www.youku.com/show_page/id_z53c8401cc84411e2b356.html',100534)
    #当男人恋爱时
    #startSearch('handles.handle_youku_tv', 'http://www.youku.com/show_page/id_z0a7ac8126f6111e2b16f.html',100533)
    #听见你的声音
    #startSearch('handles.handle_youku_tv', 'http://www.youku.com/show_page/id_z494b92cab2fe11e29498.html',100531)
    
    #35岁的高中生
    startSearch('handles.handle_funshion_tv', 'http://www.funshion.com/subject/107354',100532)

def main3():
    #无情都市
    #startSearch('handles.handle_letv_tv', 'http://so.letv.com/tv/89951.html',100391)
    #新恋爱时代
    #startSearch("handles.handle_letv_tv", "http://tv.letv.com/zt/xlasd/index.shtml",100555)
    # 火线三兄弟 100540
    #startSearch("handles.handle_iqiyi_tv", "http://www.iqiyi.com/dianshiju/hxsxd.html",100540)
    
    #国土安全 第一季
    #startSearch('handles.handle_youku_tv', 'http://www.youku.com/show_page/id_zbaceffd8db7111e0a046.html',100527)
    #穹顶之下 第1季
    startSearch("handles.handle_youku_tv", "http://www.youku.com/show_page/id_ze277322e9b4d11e2be40.html",100213)

if __name__ == '__main__':
    main3()
#    pass
#    name = 'handles.handle_revenge2'
#    __import__('handles.handle_revenge2')
#    import sys
#    print sys.modules[name]