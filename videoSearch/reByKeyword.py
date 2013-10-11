#coding=utf-8

import redis
from setting import clct_channel,clct_resource,clct_userWeibo,clct_playLog, clct_user
import imp,sys
from pprint import pprint
import json ,time
from common.HttpUtil import get_html,HttpUtil
from bson import ObjectId

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
    pass

def segment(sentences):
    pass

def retrieveVideo(keywords):
    pass

def upload(videos):
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
        similarTags = similarWords(userTags)
    
    infos = retrieveUserHistory(userId)
    keywords = segment(infos)
    
    if keywords is not None:
        similarKeywords = similarWords(keywords)

    videos = []
    videos.append(retrieveVideo(similarTags)) 
    videos.append(retrieveVideo(similarKeywords))

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
