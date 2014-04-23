#coding=utf-8
import redis
from setting import clct_channel,clct_resource,clct_userWeibo,clct_playLog, clct_user, clct_userRecommend, debug, clct_tag, clct_userDiscard
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

from PIL import Image
import urllib2 as urllib
import io

def updateSnapshot():
    rets = clct_resource.find({'v_size':{'$exists': False}, 'isOnline':True, 'channelId':{'$in': [101641, 101758]}})

    for ret in rets:
        try:
            fd = urllib.urlopen('http://h47/huohua_v2/imageinterfacev2/api/interface/image/disk/get/*/*/'+ret['resourceImageUrl'])
            image_file = io.BytesIO(fd.read())
        except Exception, e:
            print e
            continue
        im = Image.open(image_file)
        (w,h) = im.size
        if w < 480:
            clct_resource.update({'_id':ret['_id']},{'$set':{'isOnline':False, 'snapshot':'small', 'v_size': [w, h]}})
        else:
            clct_resource.update({'_id':ret['_id']},{'$set':{'snapshot':'done', 'v_size': [w, h]}})


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
            if entity == '':
                continue
            recommendByBaidu([entity], entity, 'Tags', 101758, 'gbk', True)

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
                if ret['channelId'] == 1 :
                    tags = []
                    hashtag = re.findall(r"#(\S+)#",title)
                    if not hashtag:
                        tags = segmentByNLP(title)
                    else:
                        tags = hashtag
                else:
                    tags = segmentByNLP(title)
                if not tags:
                    tags = [title]
                clct_resource.update({'_id':ret['_id']},{'$set':{'tagList':tags}})
            except Exception,e:
                print e
                continue

def setWeiboTag():
    rets = clct_resource.find({'channelId':1})
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
    rets = clct_resource.find({'channelId':1})
    for ret in rets:
        clct_resource.update({'_id':ret['_id']},{'$set':{'updateTime':ret['createTime']}})

from reByKeyword import blacklist
def stripTag():
    rets = clct_resource.find({'tagList':{'$exists':True}})
    for ret in rets:
        if ret['tagList']:
            stripTagList = []
            hit = False
            for tag in ret['tagList']:
                if not tag:
                    continue
                if re.search('<[^<]+?>',tag) is not None:
                    print tag
                    videoTag = re.sub('<[^<]+?>', '', tag)
                    print videoTag
                    hit = True
                else:
                    videoTag = tag
                if len(videoTag) < 6:
                    stripTagList.append(videoTag)
            if hit:
                if not stripTagList:
                    stripTagList = segmentByNLP(ret['resourceName'])
                clct_resource.update({'_id':ret['_id']},{'$set':{'tagList': stripTagList}})

def updateTag():
    rets = clct_resource.find({'tagList':{'$exists':True}})
    for ret in rets:
        if not ret['tagList']:
            title = ret.get('resourceName','')
            if title:
                try:
                    if ret['channelId'] == 1 :
                        tags = []
                        hashtag = re.findall(r"#(\S+)#",title)
                        if not hashtag:
                            tags = segmentByNLP(title)
                        else:
                            tags = hashtag
                    else:
                        tags = segmentByNLP(title)
                    if not tags:
                        tags = [title]
                except Exception,e:
                    print e
                    continue
            else:
                continue
            clct_resource.update({'_id':ret['_id']},{'$set':{'tagList':tags}})
            continue

from py4j.java_gateway import JavaGateway
def updateExistTag():
    rets = clct_resource.find({'tagList':{'$exists':True}})
    gateway = JavaGateway()
    for ret in rets:
        if ret['tagList']:
            for tag in ret['tagList']:
                if tag == u'':
                    continue
                if re.match('\d+', tag):
                    print tag
                gateway.entry_point.POS(tag)
            resultTags = list(set(ret['tagList']) - set(blacklist))
            if set(resultTags) == set(ret['tagList']):
                continue
            clct_resource.update({'_id':ret['_id']},{'$set':{'tagList':ret['tagList']}})

from collections import defaultdict
def updateUserTag():
    rets = clct_userDiscard.find({})
    resourceMM = defaultdict(list)
    for ret in rets:
        try:
            userTags = clct_user.find_one({'uuid':ret['uuid']}).get('tagList',[])
            mm = defaultdict(list)
            for dislike in ret['discardList']:
                if not resourceMM[dislike]:
                    resourceR = clct_resource.find_one({'_id':ObjectId(dislike)})
                    resourceMM[dislike].append(resourceR['tagList'])
                    tags = resourceR['tagList']
                else:
                    tags = resourceMM[dislike][0]
                for tag in tags:
                    mm[tag].append(dislike)
            dislikeTags = []
            for k, v in mm.items():
                if len(v) >= 2:
                    dislikeTags.append(k)
            resultTags = set(userTags) - set(dislikeTags)
            if resultTags != set(userTags):
                clct_user.update({'uuid':ret['uuid']}, {'$set':{'tagList':list(resultTags)}})
        except Exception,e:
            import traceback
            print traceback.format_exc()
            print e
'''def transferVideoInfoTask():
    rets = clct_videoInfoTask_bak.find({})
    for ret in rets:
        try:
            clct_videoInfoTask.insert(ret, safe=True)
        except Exception,e:
            print e'''

def updateResourceWithoutChannel():
    rets = clct_resource.find({})
    for ret in rets:
        retC = clct_channel.find_one({'channelId':ret['channelId']})
        if retC is None:
            clct_resource.update({'_id':ret['_id']},{'$set':{'channelId': 101641}})

def updateChannelSnapshot(channelId):
    rets = clct_resource.find({'channelId':channelId})
    for ret in rets:
        url = 'http://47.weiweimeishi.com:8013/resource/refreshSnapshot?id=%s'%str(ret['_id'])
        httpUtil = HttpUtil()
        encoding = 'utf-8'
        httpUtil.opener.addheaders.append(('Cookie','sessionid=33b88480a48a5490c8eb2a9c41541049'))
        content = httpUtil.Get(url)

import suffixArrayApplications as saApp
from py4j.java_gateway import JavaGateway
def filterRecommendations():
    #rets = clct_userRecommend.find({'isViewed':-1,'snapshot':{'$regex':'done|gifDone'}})
    rets = clct_resource.find({'$or':[{'channelId':101641, 'isOnline':True},{'channelId':101758, 'isOnline':True}]})
    gateway = JavaGateway()

    from reByKeyword import filterVideo

    for ret in rets:
        title = ret.get('resourceName',None)
        if title is None:
            title = ret.get('title', None)

        #nerMap = gateway.entry_point.NERTag(title)
        #print nerMap
        ret['ti'] = title
        ret['url'] = ret['resourceUrl']
        resultR = filterVideo([ret])
        if resultR:
            if resultR[0]['ti'] != title:
                clct_resource.update({'_id':ret['_id']},{'$set':{'resourceName': resultR[0]['ti']}})
                print resultR[0]['ti']
        else:
            print title
            clct_resource.update({'_id':ret['_id']},{'$set':{'isOnline':False}})


def offlineRecommendations():
    rets = clct_userRecommend.find({})
    for ret in rets:
        resource = clct_resource.find_one({'_id':ObjectId(ret['resourceId'])})
        if resource and not resource.get('isOnline', None):
            clct_userRecommend.remove({'_id':ret['_id']})

def offlineRecommendationsByTime():
    rets = clct_userRecommend.remove({'createTime':{'$lte':'20140301000000'}, 'isViewed':-1})

def predictDefinition():
    rets = clct_resource.find({'v_size':{'$exists':True}, 'isOnline':True})
    for ret in rets:

        definition = ret['v_size'][0]*ret['v_size'][1]/(ret['v_br']+2)
        print ret['v_size'][0], ' ', ret['v_size'][1], ' ', ret['v_br']
        print definition
        if definition > 1000:
            print 'wait'
            print ret['_id']
        '''if definition < 550:
            print 'hello'
        if ret['v_size'][0]>600 and definition < 550 and definition > 450:
            print ret['_id']'''

from reByKeyword import similarWords
from setting import clct_tagCloud
hot_tags = ["世界杯","汽车","原声","型男","NBA","短片","科幻", "正太","微电影", "DIY","二次元", "萌", "吻戏","恋爱诀窍"]
def tagCloud():
    depth = 10

    root_tags = {"体育":[{'screenName':"NBA十佳", 'name':['nba']},{'screenName':"NBA巨星",'name':['nba','科比']},{'screenName':"扣篮集锦",'name':['灌篮', '扣篮']},
                       {'screenName':"世界杯",'name':['世界杯']},{'screenName':"四大满贯", 'name':['温网', '法网', '澳网', '美网']},
                       {'screenName':"五大联赛", 'name':['德甲', '西甲', '意甲', '英超', '法甲']}, {'screenName':"经典足球", 'name':['足球']},
                       {'screenName':"体坛美女", 'name':['体坛', '美女']},{'screenName':"德州扑克",'name':['德州扑克']}],
                 "游戏":[{'screenName':"游戏资讯", 'name':['游戏']},{'screenName':"英雄联盟", 'name':['英雄联盟']},{'screenName':"单机攻略", 'name':['单机', '游戏']},{'screenName':"炉石传说", 'name':['炉石传说']}],
                 "美女":[{'screenName':"嫩模", 'name':['嫩模']},{'screenName':"女主播", 'name':['女主播']},{'screenName':"女星", 'name':['女星']},
                       {'screenName':"萝莉", 'name':['萝莉']}, {'screenName':"熟女", 'name':['熟女']}, {'screenName':"女同", 'name':['同性恋','女性']}],
                 "精选":[{'screenName':"科幻元素", 'name':['科学', '幻想']},{'screenName':"汽车", 'name':['汽车']},
                       {'screenName':"数码发烧友", 'name':['数码', '发烧友']} , {'screenName':"技术宅", 'name':['技术宅']},
                       {'screenName':"历史传奇", 'name':['历史','传奇']}, {'screenName':"军事观察", 'name':['军事']},
                       {'screenName':"武器装备", 'name':['武器', '装备']}, {'screenName':"中国领导人", 'name':['中国', '领导人']},
                       {'screenName':"科学揭秘", 'name':['科学', '揭秘']}, {'screenName':"新闻头条追踪", 'name':['新闻', '热点', '头条']}],
                 "男神":[{'screenName':"花美男", 'name':['花美男']}, {'screenName':"型男", 'name':['型男']}, {'screenName':"正太", 'name':['正太']}],
                 "时尚娱乐":[{'screenName':"时尚走秀", 'name':['时尚', '走秀']}, {'screenName':"美妆美发",'name':['化妆', '美发']},
                         {'screenName':"潮人搭配", 'name':['潮人', '搭配']}, {'screenName':"新片预告", 'name':['新片', '预告']},
                         {'screenName':"日韩偶像MV", 'name':['日本', '韩国', '偶像', 'MV']}, {'screenName':"影视原声", 'name':['影视', '原声']}],
                 "八卦":[{'screenName':"两性八卦", 'name':['两性', '八卦']}, {'screenName':"国内明星", 'name':['国内', '明星']},
                       {'screenName':"爆料", 'name':['爆料']}, {'screenName':"耽美BL", 'name':['耽美', 'BL']}],
                 "生活情感":[{'screenName':"音乐心情", 'name':['音乐', '心情']}, {'screenName':"DIY美食", 'name':['美食', 'DIY']},
                         {'screenName':"吃遍天下", 'name': ['吃遍天下']}, {'screenName':"减肥塑形", 'name':['减肥', '塑形']},
                         {'screenName':"恋爱诀窍", 'name':['恋爱']},
                         {'screenName':"星座运势", 'name':['星座', '运势']}, {'screenName':"养生健康", 'name':['养生', '健康']}]}
    for root, leaves in root_tags.iteritems():
        retRoot = clct_tagCloud.find_one({'name':root})
        entities =  []
        if retRoot is None:
            leafList = []
            for leaf in leaves:
                leafList.append(leaf['screenName'])
            entity = tagEntity([root], root, leafList)
            entities.append(entity)

        for leaf in leaves:
            cloudDic = similarWords([' '.join(leaf['name'])], True, False)
            if len(cloudDic.values()[0]) == 1:
                continue
            for (k, v) in cloudDic.items():
                entity = tagEntity(leaf['name'], leaf['screenName'], v[:10])
                entities.append(entity)
        uploadTagCloud(entities)


gateway = JavaGateway()
def tagCloud2():

    for hotTag in hot_tags:
        entities = []
        ret = clct_tagCloud.find_one({'screenName':hotTag})
        if ret is not None and hotTag != '汽车':
            continue
        if re.match("^[A-Za-z]*$", hotTag):
            hotTag = strB2Q(hotTag)
        entities.extend(_tagCloud(hotTag))
        uploadTagCloud(entities)

def _tagCloud(tag, depth=2):
    entities = []
    if depth <= 0:
        return entities
    cloudDic = similarWords(tag, True, False)
    if len(cloudDic.values()[0]) == 1:
        return entities
    for (k, v) in cloudDic.items():
        leafList = []
        for item in v:
            try:
                if not gateway.entry_point.POS(item):
                    continue
            except Exception,e:
                print e
                continue
            leafList.append(item)
            entities.extend(_tagCloud(item, depth -1))
        if re.match(r"^[^\uFF00-\uFFFF]*$", k):
            k = strQ2B(k)
        entity = tagEntity([k],k, leafList)
        entities.append(entity)
    return entities



def uploadTagCloud(entities):
    from setting import clct_tagCloud
    for entity in entities:
        try:
            clct_tagCloud.update({'screenName':entity['screenName']}, entity,True)
        except Exception,e:
            print e

def tagEntity(nameList, screenName, leafName):
    t = getCurTime()
    entity = {}
    entity['name'] = nameList
    entity['screenName'] = screenName
    entity['leafName'] = leafName
    entity['createTime'] = t
    entity['modifyTime'] = t

    return entity

if __name__ == '__main__':
    tagCloud2()
    #updateExistTag()
    #while True:
        #feedUserTag()
        #addTagResource()
        #updateUsrTag()
    #updateSnapshot()
    #filterRecommendations()
    #offlineRecommendationsByTime()
    #offlineRecommendations()
    #    time.sleep(12*60*60)
    #clearChannel(101758)
