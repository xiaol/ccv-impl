#coding=utf-8
import redis
from setting import clct_channel,clct_resource,clct_userWeibo,clct_playLog, clct_user, clct_userRecommend, debug
import imp,sys
from pprint import pprint
import json ,time, re
from common.HttpUtil import get_html,HttpUtil
from bson import ObjectId
import distance
import urllib2
from common.common import getCurTime,strB2Q,strQ2B
from common.Domain import Resource
from common.videoInfoTask import addVideoInfoTask


redisUrl = 'localhost'
contentUrl = 'http://60.28.29.46:8080/solr/collection1/select?q=%s&rows=1&wt=json&indent=true'
segmentUrl = 'http://60.28.29.46:8080/solr/collection1/analysis/field?wt=json&q=%s&analysis.fieldtype=text_cn&indent=true'
if not debug:
    contentUrl = 'http://h46:8080/solr/collection1/select?q=%s&rows=1&wt=json&indent=true'
    segmentUrl = 'http://h46:8080/solr/collection1/analysis/field?wt=json&q=%s&analysis.fieldtype=text_cn&indent=true'
    redisUrl = 'h48'

youkuSearchUrl = "https://openapi.youku.com/v2/searches/video/by_keyword.json?client_id=1f6d9cfc3c9723fd&keyword=%s&paid=0&orderby=view-count&page=1&count=1"

def retrieveUserTag(sinaToken,sinaId):
    page,count = 1,20
    userTagUrl = 'https://api.weibo.com/2/tags.json?' \
                 'access_token=%s&uid=%s&page=%s&count=%s'%(sinaToken,sinaId,page,count)
    result = []
    try:
        html = get_html(userTagUrl)
        tags = json.loads(html)
    except Exception,e:
        print e
        return result
    for tag in tags:
        for (k,v) in tag.items():
            if isinstance(v, basestring):
                result.append(v)

    return result

def retrieveSuggestion(sinaToken):
    result = []
    userSuggestionUrl = 'https://api.weibo.com/2/tags/suggestions.json?' \
                        'access_token=%s&count=10'%(sinaToken)
    try:
        html = get_html(userSuggestionUrl)
        suggestions = json.loads(html)
    except Exception,e:
        print e
        return result
    for suggest in suggestions:
        for (k,v) in suggest.items():
            if cmp(k,'value') == 0:
                result.append(v)

    return result

def retrieveUserHistory(userId):
    rets = clct_playLog.find({'uuid': userId, 'playTime': { '$ne': "0" }}).sort("operationTime", -1).limit(10)
    records = []
    for ret in rets:
        records.append(ret['resourceId'])
    reSet = set(records)
    records = []

    for record in reSet:
        records.append(clct_resource.find_one({'_id': ObjectId(record)}))
    for entity in records:
        retC = clct_channel.find_one({'channelId':entity['channelId']})
        entity['resourceName'] = entity['resourceName']+' ' + retC.get('channelName','')+' '+retC.get('detailDescription','')
        entity['resourceName'] = re.sub('http://[\w\./]*','',entity['resourceName'])
    return records

def retrieveUserSearchHistory(userId):
    pass

def similarWords(words,total=False):
    if not isinstance(words, list):
        words = [words]
    result = {}
    for word in words:
        tags_str = " ".join(segment(word))
        temp = distance.similar('',tags_str.encode('utf8'))
        if not total:
            tempA = temp[:10];tempB = temp[-10:];tempA.extend(tempB)
            result[tags_str] = tempA
        else:
            result[tags_str] = temp
    return result

def segment(sentences):
    if len(sentences) <= 2:
        return [sentences]
    url = segmentUrl%(urllib2.quote(sentences.encode('utf8')))
    i,tags = 0,[]
    try:
        html = get_html(url)
        result = json.loads(html)['analysis']['field_types']['text_cn']['query'][1]
    except Exception,e:
        print e
        return tags
    for line in result:
        tags.append(strB2Q(line['text']))
        if len(tags) >= 100: return tags
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
    videos = []
    try:
        html = get_html(url)
        ret = json.loads(html)['response']['docs']
    except Exception,e:
        print e
        return videos
    videos = buildVideo(ret, ' '.join(words), source)
    videos.extend(recommendByYouku(words,' '.join(words), source))
    return videos

def recommendByYouku(words,reason, source):
    subCon = ' '.join(words)
    #subCon = strQ2B(subCon)
    url = youkuSearchUrl%subCon
    videos = []
    try:
        html = get_html(url)
        ret = json.loads(html)['videos']
        videos = buildVideoFromYouku(ret,reason, source,True)
    except Exception,e:
        print e
        return videos
    return videos

def buildVideoFromYouku(entities, reason, source, snapShot = False):
    updateMap = {'updateTime':getCurTime()}
    clct_channel.update({'channelId':101641},{'$set':updateMap})

    '''入库'''
    t = getCurTime()
    result = []
    for entity in entities:
        if entity['view_count'] < 7000:
            continue
        resource = buildResource(entity['link'],entity['title'],101641,'youku',entity['id'],'video')
        resource['createTime'] = t
        resource['categoryId'] = 0
        resource['isOnline'] = False
        resource['source'] = 'recommend'
        resource['updateTime'] = getCurTime()
        resource['tagList'] = entity['tags'].split(',')
        resource['tagList'].append(entity['category'])
        print("insert ",resource['videoType'],resource['videoId'], resource['resourceUrl'])
        resource['weight'] = -1

        try:
            ret = clct_resource.insert(resource , safe=True)
            entity['resourceId'] = str(ret)
        except Exception,e:
            print("insert Error!",e)
            try:
                ret  = clct_resource.find_one({'videoType':resource['videoType'], 'videoId':resource['videoId']})
                entity['resourceId'] = str(ret['_id'])
            except Exception,x:
                print x

        else:
            '''新增 截图任务'''
            if snapShot:
                mp4box = True if resource['videoType'] == 'sohu_url' else False
                addVideoInfoTask(resource['channelId'],str(ret),resource['videoId'],resource['videoType'],mp4box,force=True,goOnline=True)

        entity['recommendSource'] = source
        entity['recommendReason'] = reason
        entity['isViewed'] = -1
        entity['isPlayed'] = -1
        entity['playTime'] = 0
        entity['createTime'] = t
        result.append(entity)

    return result


def buildResource(url,title,channelId,videoType,videoId,typeType):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = typeType
    resource['videoType'] = videoType
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    resource['modifyTime'] = getCurTime()

    return resource.getInsertDict()

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
            if cmp(ret['recommendReason'].encode('utf8'), video['recommendReason']) != 0:
                ret['recommendReason'] = ret['recommendReason'].encode('utf8')+' '+video['recommendReason']
                clct_userRecommend.update({'uuid':video['uuid'], 'resourceId':video['resourceId']},{'$set':{'recommendReason':ret['recommendReason']}})
        else:
            pass

def walk(reason, source):
    videos = []
    if reason == '':
        return videos
    try:
        rets = clct_userRecommend.find({'recommendReason':{'$regex':'^'+reason+'|'+' '+reason}, 'isPlayed': 1})
        if rets.count() != 0:
            for ret in rets:
                reasonDic = similarWords([ret['recommendReason']])
                for (k, v) in reasonDic.items():
                    for word in v:
                        if cmp(word,ret['recommendReason'].encode('utf8')) == 0:
                            continue
                        videos.extend(walk(word,'%s %s'%(source, k)))
                return videos
        else:
            rets = clct_userRecommend.find({'recommendReason':{'$regex':'^'+reason+'|'+' '+reason}}).sort("createTime", -1)
            if rets.count() == 0:
                return recommend([reason], source)
            else:
                for oldRecommend in rets:
                    cooling = time.mktime(time.localtime()) - time.mktime(time.strptime(oldRecommend['createTime'],'%Y%m%d%H%M%S'))  > 3600*48
                    if cooling:
                        return recommend([reason],source)
                    break
                return videos
    except Exception,e:
        print e
        return videos

def process(uuid):
    ret = clct_user.find_one({'uuid':uuid})
    if ret is None:
        return False
    similarDic = {}
    similarKeywordsDic = []
    videos = []

    records = retrieveUserHistory(ret['uuid'])
    if  ret['sinaId'] == "":
        total = False
    else: total = False
    for record in records:
        similarKeywordsDic = similarWords(record['resourceName'],total)
        for (k,v) in similarKeywordsDic.items():
            for tag in v:
                video = walk(tag, k)
                if video: videos.extend(video)

    try:
        if ret['sinaId'] != "":
            userTags = retrieveUserTag(ret['sinaToken'],ret['sinaId'])
            if userTags:
                similarDic = similarWords(userTags)
                for (k,v) in similarDic.items():
                    for tag in v:
                        video = walk(tag, k)
                        if video: videos.extend(video)
    except Exception,e:
        print e

    print uuid,'count: ',len(videos)
    if len(videos) == 0:
        retR = clct_userRecommend.find_one({'uuid':ret['uuid'],'isViewed':-1,'snapshot':{'$regex':'done|gifDone'}})
        try:
            if  retR is None and ret['sinaId'] != "":
                suggestionTag = retrieveSuggestion(ret['sinaToken'])
                if suggestionTag is not None:
                    similarSuggestionDic = similarWords(suggestionTag)
                    for (k,v) in similarSuggestionDic.items():
                        for tag in v:
                            video = walk(tag, k)
                            if video: videos.extend(video)
                print uuid,'count: ',len(videos)
        except Exception,e:
            print e


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
            print(originalMsg[1])
            msg = json.loads(originalMsg[1])
            print("User starting: ", msg['uuid'])
            process(msg['uuid'])
            elapsed = (time.time() - start)
            print("Time used:",elapsed)

        except Exception,e:
            print e

if __name__ == '__main__':
    #pprint(process('sina_1837408945'))#'99000310639035'))#)) #huohua_sina_524922ad0cf25568d165cbdd'
    main()
    #recommendByYouku(["ＩＴ"],"","")
