#coding=utf-8
import redis
from setting import clct_channel,clct_resource,clct_userWeibo,clct_playLog, clct_user, clct_userRecommend, debug, clct_tag
import imp,sys
from pprint import pprint
import json ,time, re
from common.HttpUtil import get_html,HttpUtil
from bson import ObjectId
import urllib2
from common.common import getCurTime,strB2Q,strQ2B
from common.Domain import Resource
from common.videoInfoTask import addVideoInfoTask
from bson.objectid import ObjectId

__author__ = 'Ivan liu'

def updateSnapshot():
    rets = clct_userRecommend.find({'isViewed':-1,'snapshot':"doingGif"})

    for ret in rets:
        retR = clct_resource.find_one({'_id':ObjectId(ret['resourceId'])})
        if retR['isOnline']:
            clct_userRecommend.update({'uuid':ret['uuid'], 'resourceId':ret['resourceId']},{'$set':{'snapshot':'done'}})
        else:
            clct_userRecommend.update({'uuid':ret['uuid'], 'resourceId':ret['resourceId']},{'$set':{'snapshot':retR['snapshot']}})

def clearChannel(channelId):
    rets = clct_resource.remove({'channelId':channelId})

initial_tags = ['BBC', 'HBO', 'OVA', 'TVB', 'MV', '爱情',
                '奥斯卡', '暴力',  '传记', '迪斯尼', '谍战',  '动画短片', '动漫', '萌宠',  '动作',
                '独立电影', '恶搞', '儿童', '二战', '犯罪',  '感人',  '搞笑',  '宫崎骏',  '国产电影',
                '国产动画', '韩剧',  '黑白片' , '黑帮', '黑色幽默', '纪录片',  '僵尸',
                '惊悚',  '经典', '警匪', '剧场版',  '科幻', '恐怖片', '烂片', '浪漫',  '励志', '历史',
                '旅行',  '伦理',  '漫画改编', '冒险', '美剧',  '美食',  '好莱坞',  '梦想',  '名著改编',
                '魔幻',   '女性',  '欧美电影',  '奇幻',  '亲情', '青春', '情色',   '人性',  '日本动漫',  '日剧',
                '生活',   '史诗',  '台剧',  '泰国电影',  '同性',  '童话',  '童年回忆',  '推理',  '文艺',
                '武侠',   '吸血鬼',  '希区柯克', '喜剧' ,  '香港电影',  '校园',  '悬疑',   '血腥',  '摇滚',
                '音乐剧',  '英剧',  '友情',  '灾难',  '战争',  '治愈系',  '自由',  '宗教',
                '纯音乐',  '电影原声',  '独立音乐',  '翻唱牛人',  '摩登天空音乐节',  '同人音乐',  '演唱会',
                '明星', '写真',  '健康', '小窍门']

top_tags = ['动画短片', '黑色幽默', '惊悚', '烂片', '亲情', '同性', '童年回忆',
            '武侠', '治愈系', '写真', '摇滚', '音乐剧', '推理', '科幻', '灾难', '纪录片']

def createOrUpdateTags():
    for entity in initial_tags:
        tag = buildTag(entity,[])
        try:
            clct_tag.insert(tag,safe=True)
        except Exception,e:
            try:
                retR  = clct_tag.update({'name': tag['name']},{'$set':{'weight':tag['weight']}})
            except Exception,x:
                print x


def buildTag(name,wordVec,refNum=1):
    tag = {}
    t = getCurTime()
    tag['refNum'] = refNum
    tag['modifyTime'] = t
    tag['createTime'] = t
    tag['name'] = name
    tag['wordVec'] = wordVec
    tag['weight'] = 90
    if name in top_tags:
        tag['weight'] = 100
    return tag

from reByKeyword import recommendByYouku,recommendByBaidu, segmentByNLP

def feedTag(tags, divide=False, fromWord = ''):
    start = False
    for entity in tags:
        #recommendByYouku([entity],entity,'Tags',101758, 'relevance')
        if divide and not start and (entity == fromWord):
            start = True
        if start or not divide:
            recommendByBaidu([entity], entity, 'Tags', 101758)

def feedUserTag():
    rets = clct_user.find({'tagList':{'$exists':True}})
    tags = []
    for ret in rets:
        tags.extend(ret['tagList'])
    tagSet = set(tags)
    print "Update tags count: ", len(tagSet)
    feedTag(tagSet)

def addTag():
    rets = clct_userRecommend.find({'tags':{'$exists':False},'tagList':{'$exists':False}})
    for ret in rets:
        title = ret.get('resourceName','')
        if title:
            try:
                tags = segmentByNLP(title)
                clct_resource.update({'_id':ObjectId(ret['resourceId'])},{'$set':{'tagList':tags}})
                clct_userRecommend.update({'_id':ret['_id']},{'$set':{'tagList':tags}})
            except Exception,e:
                print e
                continue

def addTagResource():
    rets = clct_resource.find({'tagList':[]})
    for ret in rets:
        title = ret.get('resourceName','')
        if title:
            try:
                if ret['channelId'] == 0 :
                    tags = []
                    hashtag = re.findall(r"#(\S+)#",title)
                    if not hashtag:
                        tags = segmentByNLP(title)
                    else:
                        tags = hashtag
                else:
                    tags = segmentByNLP(title)
                clct_resource.update({'_id':ret['_id']},{'$set':{'tagList':tags}})
            except Exception,e:
                print e
                continue

def setWeiboTag():
    rets = clct_resource.find({'channelId':0})
    for ret in rets:
        title = ret.get('resourceName','')
        if title:
            try:
                hashtag = re.findall(r"#(\S+)#",title)
                if hashtag:
                    tags = hashtag
                    clct_resource.update({'_id':ret['_id']},{'$set':{'tagList':tags}})
            except Exception,e:
                print e
                continue

def updateWeiboUpdateTime():
    rets = clct_resource.find({'channelId':0})
    for ret in rets:
        clct_resource.update({'_id':ret['_id']},{'$set':{'updateTime':ret['createTime']}})

from reByKeyword import blacklist
def updateTag():
    rets = clct_resource.find({'tagList':{'$exists':True}})
    for ret in rets:
        count = len(blacklist)
        hitCount = 0
        for black in blacklist:
            try:
                ret['tagList'].remove(black)
            except ValueError:
                hitCount = hitCount + 1
        if hitCount != count:
            clct_resource.update({'_id':ret['_id']},{'$set':{'tagList':ret['tagList']}})


if __name__ == '__main__':
    #createOrUpdateTags()
    #addTag()
    #setWeiboTag()
    #updateWeiboUpdateTime()
    #updateTag()
    while True:
        feedUserTag()
        addTagResource()
        time.sleep(60*60)
    #feedTag(initial_tags, True, '音乐剧')
    #clearChannel(101758)
