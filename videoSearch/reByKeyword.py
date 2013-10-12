#coding=utf-8

import redis
from setting import clct_channel,clct_resource,clct_userWeibo,clct_playLog, clct_user, clct_userRecommend
import imp,sys
from pprint import pprint
import json ,time
from common.HttpUtil import get_html,HttpUtil
from bson import ObjectId
import distance
import urllib2
from common.common import getCurTime

redisUrl = 'localhost'
if not __debug__:
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
            result.append(v)
            break

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
    pass

def retrieveUserSearchHistory(userId):
    pass

def similarWords(words):
    result = {}
    for word in words:
        tags_str = " ".join(segment(word))
        result[tags_str] = distance.similar('',tags_str.encode('utf8'))
    return result

def segment(sentences):
    url = 'http://60.28.29.46:8080/solr/collection1/analysis/field?'\
        'wt=json&q=%s&analysis.fieldtype=text_cn&indent=true'%(urllib2.quote(sentences.encode('utf8')))
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
    #query = '(channelName: %s AND processed:true) OR (resourceName: %s AND isOnline:true) OR (detailLeadingRole: %s AND processed:true) OR (detailMovieCategory: %s AND processed:true)'%(subCon, subCon, subCon, subCon)
    query = 'resourceName: %s AND isOnline:true'%subCon
    query = urllib2.quote(query)
    url = 'http://60.28.29.46:8080/solr/collection1/select?'\
          'q=%s&rows=1&wt=json&indent=true'%query
    html = get_html(url)
    ret = json.loads(html)['response']['docs']
    videos = buildVideo(ret, ' '.join(words), source)
    return videos

def buildVideo(entities, reason, source):
    for entity in entities:
        entity['recommendSource'] = source
        entity['recommendReason'] = reason
        entity['isViewed'] = -1
    return entities

def retrieveVideo(keywords):
    pass

def upload(videos):
    t = getCurTime()

    for video in videos:
        try:
            ret = clct_userRecommend.insert(video , safe=True)
        except Exception,e:
            print("Insert Error!",e)
            #ret  = clct_userWeibo.find_one({'weiboId':userWeibo['weiboId'],})
        else:
            pass

def process(userId):
    ret = clct_user.find_one({'_id':ObjectId(userId)})
    if ret is None:
        return False
    if ret['sinaId'] is not None:
        userTags = retrieveUserTag(ret['sinaToken'],ret['sinaId'])
    similarTags = []
    similarKeywords = []
    if userTags is not None:
        similarDic = similarWords(userTags)

    videos = []
    for (k,v) in similarDic.items():
        for tag in v:
            video = recommend([tag], k);videos.append(video)
    infos = retrieveUserHistory(userId)
    upload(videos)

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
            process(msg['userId'])
            elapsed = (time.time() - start)
            print("Time used:",elapsed)

        except Exception,e:
            print e

if __name__ == '__main__':
    pprint(process('51bb18b10cf2507d314b78f2'))
