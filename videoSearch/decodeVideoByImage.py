#coding=utf-8
__author__ = 'Ivan liu'
from common.HttpUtil import get_html,HttpUtil
import re, time
from setting import clct_user, clct_resource
from bson import ObjectId

snapshotUrl = 'http://47.weiweimeishi.com/huohua_v2/imageinterfacev2/api/interface/image/disk/get/430/234/%s'
headers = [('User-agent','Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166')]
p_1 = re.compile('>(.*)</a>')
def searchImage(imageUrl):
    httpUtil = HttpUtil({'http': 'http://127.0.0.1:8087'})
    httpUtil.opener.addheaders = headers

    content = httpUtil.Get('http://images.google.com/searchbyimage?image_url=%s'%imageUrl)
    if content:
        result = content.decode('utf-8','ignore')
    else:
        result = ''
    start = result.find('這個圖片最有可能的推測結果')#'对该图片的最佳猜测')
    if start == -1:
        print '找不到最佳匹配'
        return []
    end = result.find('搜尋結果', start)
    bestGuess = result[start:end]
    match = p_1.findall(bestGuess)
    print match[0]
    return match

def retrieveUserLike(userId):
    ret = clct_user.find_one({'uuid': userId})
    items = []
    for resourceId in ret.get('likeList', []):
        items.append(clct_resource.find_one({'_id': ObjectId(resourceId)}))
    return items

from reByKeyword import recommendByBaidu, upload
from collections import defaultdict
def recommendBySnapshot():
    rets = clct_user.find({'likeList':{'$exists':True}})
    lmm = defaultdict(list)
    for ret in rets:
        for like in ret['likeList']:
            lmm[like].append(ret['uuid'])

    for k, v in lmm.items():
        retR = clct_resource.find_one({'_id': ObjectId(k)})
        resourceImageUrl = retR.get('resourceImageUrl','')
        videos = []
        if resourceImageUrl != '':
            imageUrl = snapshotUrl%resourceImageUrl
            tags = searchImage(imageUrl)
            for tag in tags:
                videos.extend(recommendByBaidu([tag], 'image', tag, 101641, 'gbk'))
            print len(videos)
            if len(videos) != 0:
                for userId in v:
                    upload(videos, userId)



if __name__ == '__main__':
    recommendBySnapshot()
    #tags = searchImage('http://47.weiweimeishi.com/huohua_v2/imageinterfacev2/api/interface/image/disk/get/96/*/videoCMS_channel_52ca130dd6a1e228f473dcf720140106102101.jpg')
    #recommendByBaidu(tags, 'image', ' '.join(tags), 101641)
