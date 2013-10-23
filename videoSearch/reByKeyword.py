#coding=utf-8

import redis
from setting import clct_channel,clct_resource,clct_userWeibo,clct_playLog, clct_user, clct_userRecommend, debug
import imp,sys
from pprint import pprint
import json ,time
from common.HttpUtil import get_html,HttpUtil
from bson import ObjectId
import distance
import urllib2
from common.common import getCurTime


redisUrl = 'localhost'
contentUrl = 'http://60.28.29.46:8080/solr/collection1/select?q=%s&rows=1&wt=json&indent=true'
segmentUrl = 'http://60.28.29.46:8080/solr/collection1/analysis/field?wt=json&q=%s&analysis.fieldtype=text_cn&indent=true'
if not debug:
    contentUrl = 'http://h46:8080/solr/collection1/select?q=%s&rows=1&wt=json&indent=true'
    segmentUrl = 'http://h46:8080/solr/collection1/analysis/field?wt=json&q=%s&analysis.fieldtype=text_cn&indent=true'
    redisUrl = 'h48'

def retrieveUserTag(sinaToken,sinaId):
    page,count = 1,20
    userTagUrl = 'https://api.weibo.com/2/tags.json?' \
                 'access_token=%s&uid=%s&page=%s&count=%s'%(sinaToken,sinaId,page,count)
    result = []
    html = get_html(userTagUrl)
    tags = json.loads(html)
    for tag in tags:
        for (k,v) in tag.items():
            if isinstance(v, basestring):
                result.append(v)

    return result

def retrieveSuggestion(sinaToken):
    result = []
    userSuggestionUrl = 'https://api.weibo.com/2/tags/suggestions.json?' \
                        'access_token=%s&count=10'%(sinaToken)
    html = get_html(userSuggestionUrl)
    suggestions = json.loads(html)
    for suggest in suggestions:
        for (k,v) in suggest.items():
            if cmp(k,'value') == 0:
                result.append(v)

    return result

def retrieveUserHistory(userId):
    rets = clct_playLog.find({'uuid': userId, 'playTime': { '$ne': '0' }}).sort("operationTime", 1).limit(10)
    records = []
    for ret in rets: records.append(ret['resourceId'])
    reSet = set(records)
    records = []

    for record in reSet:
        records.append(clct_resource.find_one({'_id': ObjectId(record)}))
    return records

def retrieveUserSearchHistory(userId):
    pass

def similarWords(words):
    if not isinstance(words, list):
        words = [words]
    result = {}
    for word in words:
        tags_str = " ".join(segment(word))
        temp = distance.similar('',tags_str.encode('utf8'))
        tempA = temp[:10];tempB = temp[-10:];tempA.extend(tempB)
        result[tags_str] = tempA
    return result

def segment(sentences):
    url = segmentUrl%(urllib2.quote(sentences.encode('utf8')))
    html = get_html(url)
    result = json.loads(html)['analysis']['field_types']['text_cn']['query'][1]
    i,tags = 0,[]
    for line in result:
        tags.append(line['text'])
    return tags

def recommend(words, source):
    subCon = ' OR '.join(words)
    if len(words) > 1:
        subCon = '( %s )'%subCon
    '''query = '(channelName: %s AND processed:true) OR (resourceName: %s AND isOnline:true)' \
            ' OR (detailLeadingRole: %s AND processed:true) OR (detailMovieCategory: %s AND processed:true)'%(subCon, subCon, subCon, subCon)'''
    query = 'resourceName: %s AND isOnline:true'%subCon
    query = urllib2.quote(query)
    url = contentUrl%query
    html = get_html(url)
    ret = json.loads(html)['response']['docs']
    videos = buildVideo(ret, ' '.join(words), source)
    return videos

def buildVideo(entities, reason, source):
    t = getCurTime()
    for entity in entities:
        entity['recommendSource'] = source
        entity['recommendReason'] = reason
        entity['isViewed'] = -1
        entity['isPlayed'] = -1
        entity['playTime'] = 0
        entity['resourceId'] = entity['_id']
        del entity['_id']
        entity['createTime'] = t
    return entities

def retrieveVideo(keywords):
    pass

def upload(videos, uuid):
    for video in videos:
        try:
            video['uuid'] = uuid
            ret = clct_userRecommend.insert(video , safe=True)
        except Exception,e:
            print("Insert Error!",e)
            ret = clct_userRecommend.find_one({'uuid':video['uuid'], 'resourceId':video['resourceId']})
            ret['recommendReason'] = ret['recommendReason'].encode('utf8')+' '+video['recommendReason']
            clct_userRecommend.update({'uuid':video['uuid'], 'resourceId':video['resourceId']},{'$set':{'recommendReason':ret['recommendReason']}})
        else:
            pass

def walk(reason, source): #TODO maybe find in list can work this out
    rets = clct_userRecommend.find({'recommendReason':{'$regex':'^'+reason+'|'+' '+reason}, 'isPlayed': 1})
    videos = []
    if rets.count() != 0:
        for ret in rets:
            reasonDic = similarWords([ret['recommendReason']])
            for (k, v) in reasonDic.items():
                for word in v:
                    videos.extend(walk(word,'%s %s'%(source, k)))
            return videos
    else:
        rets = clct_userRecommend.find({'recommendReason':{'$regex':reason}})
        if rets.count() == 0:
            return recommend([reason], source)
        else: return videos

def process(uuid):
    ret = clct_user.find_one({'uuid':uuid})
    if ret is None:
        return False
    similarDic = {}
    similarKeywordsDic = []
    videos = []

    records = retrieveUserHistory(ret['uuid'])
    for record in records:
        similarKeywordsDic = similarWords(record['resourceName'])
        for (k,v) in similarKeywordsDic.items():
            for tag in v:
                video = walk(tag, k)
                if video: videos.extend(video)

    if ret['sinaId'] is not None:
        userTags = retrieveUserTag(ret['sinaToken'],ret['sinaId'])
    if userTags is not None:
        similarDic = similarWords(userTags)
        for (k,v) in similarDic.items():
            for tag in v:
                video = walk(tag, k)
                if video: videos.extend(video)

    print uuid,'count: ',len(videos)
    upload(videos, ret['uuid'])

def main():
    redisHost = redis.Redis(redisUrl, 6379)
    while True:
        try:
            originalMsg = redisHost.blpop('resys')   #timeout=3
            if originalMsg is None:
                #time.sleep(2)
                continue
            start = time.time()
            msg = json.loads(originalMsg[1])
            print("User starting: ", msg['uuid'])
            process(msg['uuid'])
            elapsed = (time.time() - start)
            print("Time used:",elapsed)

        except Exception,e:
            print e

if __name__ == '__main__':
    pprint(process('sina_1837408945')) #huohua_sina_524922ad0cf25568d165cbdd'
    #main()
