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
        updateMap['subtitle'] = str(resouceList[0]['number'])
    clct_channel.update({'channelId':channelId},{'$set':updateMap})
    
    '''入库'''
    t = getCurTime()
    for resource in resouceList:
        resource['createTime'] = t
        print("insert ",resource['videoType'],resource['videoId'])
        try:
            ret = clct_resource.insert(resource , safe=True)
        except:
            print("insert Error!")
        else:
            print("insert Ok!")

            '''新增 截图任务'''
            if snapShot:
                mp4box = True if resource['videoType'] == 'sohu_url' else False
                addVideoInfoTask(resource['channelId'],str(ret),resource['videoId'],resource['videoType'],mp4box,force=True)
    

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
        one['type'] = 'video'
        
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

    snapShot = True if 'snapShot' in channel and channel['snapShot'] else False
    '''==================电视剧================'''
    if handleName == 'youkuTv':
        startSearch('handles.handle_youku_tv', url, channelId,snapShot = snapShot, updateTvNumber=True)
    elif handleName == 'funshionTv':
        startSearch('handles.handle_funshion_tv', url,channelId,snapShot = snapShot, updateTvNumber=True)
    elif handleName == 'letvTv':
        startSearch("handles.handle_letv_tv", url,channelId,snapShot = snapShot, updateTvNumber=True)
    elif handleName == 'iqiyiTv':
        startSearch("handles.handle_iqiyi_tv", url,channelId,snapShot = snapShot, updateTvNumber=True)
    elif handleName == 'sohuTv':
        startSearch("handles.handle_sohu_dongman", url,channelId,snapShot = snapShot, updateTvNumber=True)
    elif handleName == 'pptvTv':
        startSearch("handles.handle_pptv_tv", url,channelId,snapShot = snapShot, updateTvNumber=True)
    elif handleName == 'qqTv':
        startSearch("handles.handle_qq_tv", url, channelId,snapShot = snapShot, updateTvNumber=True)
    elif handleName == 'ppsTv':
        startSearch("handles.handle_pps_tv", url, channelId,snapShot = snapShot, updateTvNumber=True)
        '''===============综艺=============='''
    elif handleName == 'youkuZongyi':
        startSearch('handles.handle_youku_zongyi', url, channelId ,snapShot = snapShot, updateTvNumber=True)
    elif handleName == 'iqiyiZongyi':
        startSearch('handles.handle_iqiyi_zongyi', url, channelId,snapShot = snapShot, updateTvNumber=True)
    elif handleName == 'sohuZongyi':
        startSearch('handles.handle_sohu_zongyi', url, channelId ,snapShot = snapShot, updateTvNumber=True)
    elif handleName == 'funshionZongyi':
        startSearch('handles.handle_funshion_zongyi', url, channelId ,snapShot = snapShot, updateTvNumber=True)
    elif handleName == 'pptvZongyi':
        startSearch('handles.handle_pptv_zongyi', url, channelId ,snapShot = snapShot, updateTvNumber=True)
    elif handleName == 'qqZongyi':
        startSearch('handles.handle_qq_zongyi', url, channelId ,snapShot = snapShot, updateTvNumber=True)
        '''==============动漫==============='''
    elif handleName == 'youkuDongman':
        startSearch('handles.handle_youku_dongman', url, channelId,snapShot = snapShot, updateTvNumber=True)
    elif handleName == 'tudouDongman':
        startSearch('handles.handle_tudou', url,channelId,snapShot = snapShot, updateTvNumber=True)
    elif handleName == 'sohuDongman':
        startSearch("handles.handle_sohu_dongman", url,channelId,snapShot = snapShot, updateTvNumber=True)
    elif handleName == 'iqiyiDongman':
        startSearch("handles.handle_iqiyi_dongman", url,channelId,snapShot = snapShot, updateTvNumber=True)
    elif handleName == 'funshionDongman':
        startSearch('handles.handle_funshion_tv', url,channelId,snapShot = snapShot, updateTvNumber=True)
    elif handleName == 'letvDongman':
        startSearch('handles.handle_letv_tv', url,channelId,snapShot = snapShot, updateTvNumber=True)
        '''============ HOT ===================='''
    elif handleName == 'mtimeTrailer':
        startSearch('handles.handle_mtime', url, channelId,snapShot = snapShot)
    elif handleName == 'jimu':
        startSearch('handles.handle_jimu', url, channelId,snapShot = snapShot)
    elif handleName == 'weibo':
        startSearch('handles.handle_weibo', url, channelId,snapShot = snapShot)#url 其实就是微博UID
    elif handleName == 'youkuNews':
        startSearch('handles.handle_youku_template1', url, channelId,snapShot = snapShot)
        '''============ 纪录片 ===================='''
    elif handleName == 'youkuJilupian':
        startSearch('handles.handle_youku_jilupian', url, channelId,snapShot = snapShot)
    elif handleName == 'sohuJilupian':
        startSearch('handles.handle_sohu_dongman', url, channelId,snapShot = snapShot)
    elif handleName == 'iqiyiJilupian':
        startSearch('handles.handle_iqiyi_jilupian', url, channelId,snapShot = snapShot)
        '''============== 福利 ======================='''
    elif handleName =='welfareBaomihua':
        startSearch('handles.handle_baomihua_specialEdition',url ,channelId,snapShot = snapShot)
    elif handleName =='weipaiSquare':
        startSearch('handles.handle_weipai_square',url ,channelId,snapShot = snapShot)
    elif handleName =='chaoku4List':
        startSearch('handles.handle_chaoku4_list', url, channelId,snapShot = snapShot)
        '''==============  体育游戏 ======================='''
    elif handleName =='iqiyiSport':
        startSearch('handles.handle_iqiyi_list',url ,channelId,snapShot = snapShot)
    elif handleName =='sinaSport':
        startSearch('handles.handle_sina_sports', url, channelId,snapShot = snapShot, updateTvNumber=False)
    elif handleName =='aipai':
        startSearch('handles.handle_aipai', url, channelId,snapShot = snapShot, updateTvNumber=False)
        '''=================  其他 ======================'''
    elif handleName == 'youkuPlayList':
        startSearch('handles.handle_youku_playlist',url ,channelId,snapShot = snapShot)
    elif handleName == 'youkuSoku':
        startSearch('handles.handle_youku_soku',url ,channelId,snapShot = snapShot)
    elif handleName == '56Album':
        startSearch('handles.handle_56_album',url ,channelId,snapShot = snapShot)
    elif handleName == 'tudouAlbum':
        startSearch('handles.handle_tudou', url,channelId,snapShot = snapShot)
    elif handleName == 'youkuIndex':
        startSearch('handles.handle_youku_index', url,channelId,snapShot = snapShot)
    elif handleName == 'tudouNewsIndex':
        startSearch('handles.handle_tudou_index', url,channelId,snapShot = snapShot)
    elif handleName == '56fun':
        startSearch('handles.handle_56_fun', url,channelId ,snapShot = snapShot)
    elif handleName == '56list':
        startSearch('handles.handle_56_list', url,channelId ,snapShot = snapShot)
    elif handleName == 'youkuIyouku':
        startSearch('handles.handle_youku_iyouku', url,channelId ,snapShot = snapShot)

    elif handleName == 'youkuTravel':
        startSearch('handles.handle_youku_travel', url, channelId,snapShot = snapShot)
    elif handleName == 'youkuLife':
        startSearch('handles.handle_youku_life', url, channelId,snapShot = snapShot)
    elif handleName == 'tudouCate':
        startSearch('handles.handle_tudou_cate', url, channelId,snapShot = snapShot)
    elif handleName == 'tudouLife':
        startSearch('handles.handle_tudou_life', url, channelId,snapShot = snapShot)
    elif handleName == 'ku6Playlist':
        startSearch('handles.handle_ku6_playlist', url, channelId,snapShot = snapShot)
    elif handleName == 'iqiyiSo':
        startSearch('handles.handle_iqiyi_so', url, channelId,snapShot = snapShot)
    elif handleName == 'iqiyiList':
        startSearch('handles.handle_iqiyi_list', url, channelId,snapShot = snapShot)
    elif handleName == '56So':
        startSearch('handles.handle_56_so', url, channelId,snapShot = snapShot)
    elif handleName == 'weiboHot':
        startSearch('handles.handle_weibo_hot', url, channelId,snapShot = snapShot)
    elif handleName == 'boosjList':
        startSearch('handles.handle_boosj_list', url, channelId,snapShot = snapShot)
    elif handleName == 'boosjSubject':
        startSearch('handles.handle_boosj_subject', url, channelId,snapShot = snapShot)
    elif handleName == 'ifengList':
        startSearch('handles.handle_ifeng_list', url, channelId,snapShot = snapShot)
    elif handleName == 'kankanews':
        startSearch('handles.handle_kankanews', url, channelId,snapShot = snapShot)
    elif handleName == 'asmouList':
        startSearch('handles.handle_asmou_list', url, channelId,snapShot = snapShot)
    elif handleName == 'acfunTag':
        startSearch('handles.handle_acfun_tag', url, channelId,snapShot = snapShot)
    elif handleName == '56I':
        startSearch('handles.handle_56_i', url, channelId,snapShot = snapShot)
    elif handleName == '56Opera':
        startSearch('handles.handle_56_opera', url, channelId,snapShot = snapShot)
    elif handleName == '56Town':
        startSearch('handles.handle_56_town', url, channelId,snapShot = snapShot)
    elif handleName == 'ppsIpd':
        startSearch('handles.handle_pps_ipd', url, channelId,snapShot = snapShot)
    elif handleName == 'pptvList':
        startSearch('handles.handle_pptv_list', url, channelId,snapShot = snapShot)
    elif handleName == 'embed':
        startSearch('handles.handle_embed', url, channelId,snapShot = snapShot)
    elif handleName == 'petweiboList':
        startSearch('handles.handle_petweibo_list', url, channelId,snapShot = snapShot)
    elif handleName == 'everyshare':
        startSearch('handles.handle_everyshare', url, channelId,snapShot = snapShot)
    elif handleName == 'kengdie':
        startSearch('handles.handle_kengdie', url, channelId,snapShot = snapShot)
    elif handleName == 'o2gzs':
        startSearch('handles.handle_o2gzs', url, channelId,snapShot = snapShot)

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
