#coding=utf-8
from setting import clct_channel,clct_resource
import imp,sys
from pprint import pprint
from common.common import getCurTime
from common.videoInfoTask import addVideoInfoTask

def insertResouce(resouceList,channelId,snapShot = False, updateTvNumber = False):
    '''更新时间 频道updateTime'''
    resouceList.sort(key = lambda a:a['number'],reverse = True)
    updateMap = {'updateTime':getCurTime()}
    if updateTvNumber:
        updateMap['tvNumber'] = resouceList[0]['number']
        updateMap['subtitle'] = '已更新至：'+str(resouceList[0]['number'])
    clct_channel.update({'channelId':channelId},{'$set':updateMap})
    
    '''入库'''
    t = getCurTime()
    for resource in resouceList:
        resource['createTime'] = t
    ret = clct_resource.insert(resouceList)
    
    '''新增 截图任务'''
    if snapShot:
        for id,resource in zip(ret,resouceList):
            mp4box = True if resource['videoType'] == 'sohu_url' else False
            addVideoInfoTask(resource['channelId'],str(id),resource['videoId'],resource['videoType'],mp4box,force=True)
    

def startSearch(handleName,url,channelId,snapShot=False, updateTvNumber=False , **keyParams):
    #获取模块
    __import__(handleName)
    module = sys.modules[handleName]
    channel = clct_channel.find_one({'channelId':channelId})
    tvNumber = channel['tvNumber']
    resourceImageUrl = channel['resourceImageUrl']
    #抽取
    result = module.handle(url, channelId, tvNumber,**keyParams)
    
    isOver = False
    for one in result:
        #完结
        if one == "over":
            isOver = True
            continue
        if channel['autoOnline'] == False:
            one['isOnline'] = False
        one['resourceImageUrl'] = resourceImageUrl
        one['duration'] = channel['duration']
        one['categoryId'] = channel['channelType']
        
    pprint(result)
    result = filter(lambda a:a!="over",result)
    #入库
    if len(result) != 0:
        insertResouce(result,channelId, snapShot, updateTvNumber)
    
    #判断完结
    if isOver:
        clct_channel.update({'channelId':channelId},{'$set':{'nextSearchTime':'90000101000000'}})

def handle(channelId,handleName,url):
    
    channel = clct_channel.find_one({'channelId':channelId})
    channelId = channel['channelId']
    '''==================电视剧================'''
    if handleName == 'youkuTv':
        startSearch('handles.handle_youku_tv', url, channelId, updateTvNumber=True)
    elif handleName == 'funshionTv':
        startSearch('handles.handle_funshion_tv', url,channelId, updateTvNumber=True)
    elif handleName == 'letvTv':
        startSearch("handles.handle_letv_tv", url,channelId, updateTvNumber=True)
    elif handleName == 'iqiyiTv':
        startSearch("handles.handle_iqiyi_tv", url,channelId, updateTvNumber=True)
    elif handleName == 'sohuTv':
        startSearch("handles.handle_sohu_dongman", url,channelId, updateTvNumber=True)
    elif handleName == 'pptvTv':
        startSearch("handles.handle_pptv_tv", url,channelId, updateTvNumber=True)
        '''===============综艺=============='''
    elif handleName == 'youkuZongyi':
        startSearch('handles.handle_youku_zongyi', url, channelId ,snapShot=True, updateTvNumber=True)
    elif handleName == 'iqiyiZongyi':
        startSearch('handles.handle_iqiyi_zongyi', url, channelId ,snapShot=True, updateTvNumber=True)
    elif handleName == 'sohuZongyi':
        startSearch('handles.handle_sohu_zongyi', url, channelId ,snapShot=True, updateTvNumber=True)
    elif handleName == 'funshionZongyi':
        startSearch('handles.handle_funshion_zongyi', url, channelId ,snapShot=True, updateTvNumber=True)
    elif handleName == 'pptvZongyi':
        startSearch('handles.handle_pptv_zongyi', url, channelId ,snapShot=True, updateTvNumber=True)
        
        '''==============动漫==============='''
    elif handleName == 'youkuDongman':
        startSearch('handles.handle_youku_dongman', url, channelId, updateTvNumber=True)
    elif handleName == 'tudouDongman':
        startSearch('handles.handle_tudou', url,channelId, updateTvNumber=True)
    elif handleName == 'sohuDongman':
        startSearch("handles.handle_sohu_dongman", url,channelId, updateTvNumber=True)
    elif handleName == 'iqiyiDongman':
        startSearch("handles.handle_iqiyi_dongman", url,channelId, updateTvNumber=True)
    elif handleName == 'funshionDongman':
        startSearch('handles.handle_funshion_tv', url,channelId, updateTvNumber=True)
    elif handleName == 'letvDongman':
        startSearch('handles.handle_letv_tv', url,channelId, updateTvNumber=True)
        '''============ HOT ===================='''
    elif handleName == 'mtimeTrailer':
        startSearch('handles.handle_mtime', url, channelId,snapShot = True)
    elif handleName == 'jimu':
        startSearch('handles.handle_jimu', url, channelId, snapShot = True)
    elif handleName == 'weibo':
        startSearch('handles.handle_weibo', url, channelId, snapShot = True)#url 其实就是微博UID
    elif handleName == 'youkuNews':
        startSearch('handles.handle_youku_template1', url, channelId, snapShot = True)
        '''============ 纪录片 ===================='''
    elif handleName == 'youkuJilupian':
        startSearch('handles.handle_youku_jilupian', url, channelId)
    elif handleName == 'sohuJilupian':
        startSearch('handles.handle_sohu_dongman', url, channelId)
    elif handleName == 'iqiyiJilupian':
        startSearch('handles.handle_iqiyi_jilupian', url, channelId)
        '''============== 福利 ======================='''
    elif handleName =='welfareBaomihua':
        startSearch('handles.handle_baomihua_specialEdition',url ,channelId, snapShot = True)
        '''==============  体育游戏 ======================='''
    elif handleName =='iqiyiSport':
        startSearch('handles.handle_iqiyi_list',url ,channelId, snapShot = True)
        '''=================  其他 ======================'''
    elif handleName == 'youkuPlayList':
        startSearch('handles.handle_youku_playlist',url ,channelId)
    elif handleName == 'youkuSoku':
        startSearch('handles.handle_youku_soku',url ,channelId)
    elif handleName == '56Album':
        startSearch('handles.handle_56_alnum',url ,channelId)
    elif handleName == 'tudouAlbum':
        startSearch('handles.handle_tudou', url,channelId,needNumber = False)
        
if __name__ == '__main__':
    pass
#    pass
#    name = 'handles.handle_revenge2'
#    __import__('handles.handle_revenge2')
#    import sys
#    print sys.modules[name]
    #handle(100148,'youkuZongyi','http://www.youku.com/show_page/id_zc8725626907411e29498.html')
    #handle(100254,'youkuDongman','http://www.youku.com/show_page/id_z7f0f6662322e11e2b2ac.html')
    handle(100240,'iqiyiDongman','http://www.iqiyi.com/dongman/yhdzz.html')