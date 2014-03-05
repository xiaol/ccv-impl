#coding=utf-8
import redis
from setting import clct_channel,clct_resource,clct_userWeibo,clct_playLog, clct_user, clct_userRecommend, debug
import imp,sys
from pprint import pprint
import json ,time, re, traceback, os, random
from common.HttpUtil import get_html,HttpUtil
from bson import ObjectId
import distance
import urllib2
from common.common import getCurTime,strB2Q,strQ2B
from common.Domain import Resource
from common.videoInfoTask import addVideoInfoTask
from py4j.java_gateway import JavaGateway
import suffixArrayApplications as saApp


redisUrl = '60.28.29.37'
contentUrl = 'http://60.28.29.46:8080/solr/collection1/select?q=%s&rows=1&wt=json&indent=true'
segmentUrl = 'http://60.28.29.46:8080/solr/collection1/analysis/field?wt=json&q=%s&analysis.fieldtype=text_cn&indent=true'
if not debug:
    contentUrl = 'http://h46:8080/solr/collection1/select?q=%s&rows=1&wt=json&indent=true'
    segmentUrl = 'http://h46:8080/solr/collection1/analysis/field?wt=json&q=%s&analysis.fieldtype=text_cn&indent=true'
    redisUrl = 'h7'

youkuSearchUrl = "https://openapi.youku.com/v2/searches/video/by_keyword.json?client_id=1f6d9cfc3c9723fd&keyword=%s&paid=0&orderby=%s&page=1&count=1"
baiduSearchUrl = "http://v.baidu.com/v?word=%s&rn=60&ct=905969664&fid=1606&db=0&s=0&fr=videoMultiNeed&ty=0&nf=0&cl=0&du=0&pd=0&sc=0&order=0&pn=0"

blacklist = ['视频','在线','详情','点击','其他','电影', '最新', '视频在线观看',
             '高清', '高清影视剧', '高清版', '在线观看', '', '新浪视频', '优酷娱乐', '全部', '酷6','国内']
def retrieveUserTag(sinaToken,sinaId):
    page,count = 1,20
    userTagUrl = 'https://api.weibo.com/2/tags.json?' \
                 'access_token=%s&uid=%s&page=%s&count=%s'%(sinaToken,sinaId,page,count)
    friendsUrl = 'https://api.weibo.com/2/friendships/friends/ids.json?' \
                 'access_token=%s&uid=%s&cursor=%s'%(sinaToken, sinaId, 0)

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

    try:
        html = get_html(friendsUrl)
        friends = json.loads(html)
    except Exception,e:
        print e
        return result

    count = 0
    friendsList = []
    friendsTag = []
    tagsAll = []
    for friend in friends['ids']:
        friendsList.append(friend)
        if count%19 == 0:
            tagBatchUrl = 'https://api.weibo.com/2/tags/tags_batch.json?' \
                      'access_token=%s&uids=%s'%(sinaToken, urllib2.quote(','.join(map(str,friendsList))))
            try:
                html = get_html(tagBatchUrl)
                tagBatch = json.loads(html)
                tagsAll.extend(tagBatch)
            except Exception,e:
                print e
            friendsList = []
        count = count + 1

    for friendTag in tagsAll:
        for oneTag in friendTag['tags']:
            for (k, v) in oneTag.items():
                if k != u'weight':
                    friendsTag.append(v)

    for friendTag in tagsAll:
        sinaFriendTag = []
        hit = False
        for oneTag in friendTag['tags']:
            for (k, v) in oneTag.items():
                if k != u'weight':
                    sinaFriendTag.append(v)
                    friendsTag.remove(v)
                    if v in friendsTag:
                        result.append(v)

        #if hit:
        #    result.extend(sinaFriendTag)

    return set(result)

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
    rets = clct_playLog.find({'uuid': userId, 'playTime': { '$gte': "600000" }}).sort("operationTime", -1)
    records = []
    for ret in rets:
        records.append(ret['resourceId'])
    reSet = set(records)
    records = []
    finalList = list(reSet)
    random.shuffle(finalList, random.random)
    finalList = finalList[0:2]

    for record in finalList:
        records.append(clct_resource.find_one({'_id': ObjectId(record)}))
    for entity in records:
        retC = clct_channel.find_one({'channelId':entity['channelId']})
        entity['resourceName'] = entity['resourceName']+' ' + retC.get('channelName','')+' '+retC.get('detailDescription','')
        entity['resourceName'] = re.sub('http://[\w\./]*','',entity['resourceName'])
    return records

def retrieveUserLike(userId):
    ret = clct_user.find_one({'uuid': userId})
    items = []
    for resourceId in ret.get('likeList', []):
        items.append(clct_resource.find_one({'_id': ObjectId(resourceId)}))
    return items

def retrieveUserSearchHistory(userId):
    pass

def similarWords(words,total=False,isSegment=False):
    if not isinstance(words, list):
        words = [words]
    result = {}
    for word in words:
        if not isSegment:
            rebuiltTags = word.split(' ')
            rebuiltNTags = []
            for rebuiltTag in rebuiltTags:
                if re.match("^[A-Za-z]*$", rebuiltTag):
                    rebuiltNTags.append(strB2Q(rebuiltTag))
                else: rebuiltNTags.append(rebuiltTag)
            tags_str = ' '.join(rebuiltNTags)
        else:
            segmentTags = segment(word, isSegment)
            segmentNTags = []
            for segmentTag in segmentTags:
                if re.match("^[A-Za-z]*$", segmentTag):
                    segmentNTags.append(strB2Q(segmentTag))
                else:
                    segmentNTags.append(segmentTag)
            tags_str = " ".join(segmentNTags)
        temp = distance.similar('',tags_str.encode('utf8'))
        if temp[0] == '':
            result[tags_str] = [word.encode('utf8')]
            continue
        if not total:
            random.shuffle(temp, random.random)
            tempA = temp[:5]#;tempB = temp[-2:];tempA.extend(tempB)
            result[tags_str] = tempA
        else:
            result[tags_str] = temp
    return result

def segment(sentences,isSegment=False):
    if len(sentences) <= 2:
        return [sentences]
    try:
        return segmentByNLP(sentences)
    except Exception,e:
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

def segmentByNLP(sentences): #WARNING THROW EXCEPTIONS HERE.
    gateway = JavaGateway()
    num = len(sentences)/12
    if num == 0:
        num = 1
    keywords = gateway.entry_point.extractKeywords(sentences, num,True)
    keywordsList = keywords.split(' ')
    for black in blacklist:
        try:
            keywordsList.remove(black)
        except ValueError:
            pass
    return keywordsList

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
        videos = buildVideo(ret, ' '.join(words), source)
    except Exception,e:
        print 'not found in ours', ' ',e
    if not videos:
        videos.extend(recommendByBaidu(words,' '.join(words), source, 101641))
    #videos.extend(recommendByYouku(words,' '.join(words), source))
    return videos

def recommendByYouku(words,reason, source,channelId=101641, orderBy='view-count',viewCount=7000):
    subCon = ' '.join(words)
    #subCon = strQ2B(subCon)
    url = youkuSearchUrl%(subCon, orderBy)
    videos = []
    try:
        html = get_html(url)
        ret = json.loads(html)['videos'][0:2] #TODO 限制个数
        videos = buildVideoFromYouku(ret,reason, source,True,channelId, viewCount)
    except Exception,e:
        print e
        return videos
    return videos

def recommendByBaidu(words, reason, source, channelId=101758, encode='gb2312', tagReason = False):
    subCon = ' '.join(words)
    videos = []
    #subCon = strQ2B(subCon)
    try:
        subCon = subCon.decode('utf-8').encode(encode)
        subCon = urllib2.quote(subCon)
        url = baiduSearchUrl%subCon
        html = get_html(url, 'gbk')[10:-1]
        lines = html.split('\n')
        resultLines = []
        for line in lines:
            line = re.sub(r'\\\'','\'',line)
            line = re.sub(r'([A-za-z]+):(?!//)', r'"\1":', line, 1)
            line = re.sub(r'([A-za-z]+):(?!//)\s*"', r'"\1":"', line)
            resultLines.append(line)
        html = '\n'.join(resultLines)
        #html = re.sub(r'"(\w)"(?!,|)',r'\1',html)
        result = json.loads(html)['data']
        result = filterVideo(result)
        random.shuffle(result, random.random)
        ret = result[0:1]
        #ret = json.loads(html)['data'][0:1]
        videos.extend(buildVideoFromBaidu(ret,reason, source,True,channelId, 7000, tagReason ))
    except Exception,e:
        print e
        #import traceback
        #print traceback.format_exc()
        return videos
    return videos

def filterVideo(entities):
    result = []
    for entity in entities:
        if re.search('aipai.com', entity['url']) is not None:
            continue
        if len(entity['ti'].encode('utf8')) < 20:
            continue
        if re.search('\d{9,}', entity['ti']) is not None:
            continue
        if re.search(u'\d+集',entity['ti']):
            continue
        if re.search(u'[\u4e00-\u9fa5]+\d+$', entity['ti']) and len(entity['ti'].encode('utf8')) < 27:
            continue
        titleSegs =  re.split(u'[^\u4e00-\u9fa5]+', entity['ti'])
        titleSum = 0
        for titleSeg in titleSegs:
            titleSum = titleSum + len(titleSeg.encode('utf8'))
            #print titleSeg

        if sum < 20 and len(titleSegs) == 1:
            continue

        if re.search('\d{6,}', entity['ti']) is not None:
            tempTitle = re.sub('\d{6,}', '', entity['ti'])
            if len(tempTitle.encode('utf8')) < 20:
                continue
            else:
                entity['ti'] = tempTitle
            continue

        lCommonResult =  saApp.longest(entity['ti'])
        resultLen = len(lCommonResult)
        if lCommonResult != '' and resultLen > 2:
            templCommonResult = re.sub(u'[^\u4e00-\u9fa5]+','', lCommonResult)
            tempResultLen = len(templCommonResult)
            if tempResultLen > 10 and re.search(u'[\u4e00-\u9fa5]+', lCommonResult):
                continue
            titleLen = len(entity['ti'])
            if resultLen >= 3 and re.search(u'[\u4e00-\u9fa5]+', lCommonResult):
                occurrences = saApp.search2(lCommonResult, entity['ti'])
                occurrencesCount =  len(occurrences)
                if occurrencesCount > 2 or resultLen > 3:
                    ratio = float(titleLen)/(len(lCommonResult)*len(occurrences))
                    if resultLen > 4 and ratio < 2.8:
                        continue
                    elif ratio < 3.0:
                        continue
        result.append(entity)
    return result

def buildVideoFromBaidu(entities, reason, source, snapShot = False,channelId=101758, viewCount=7000, tagReason = False):
    updateMap = {'updateTime':getCurTime()}
    clct_channel.update({'channelId':101641},{'$set':updateMap})

    '''入库'''
    t = getCurTime()
    result = []
    for entity in entities:
        item = decodeVideo(entity.get('url',''))  #TODO 百度返回的搜索会不会还有额外信息
        if not item:
            continue
        resource = buildResource(entity['url'],entity['ti'],channelId,item['videoType'],item['videoId'],'video')
        resource['createTime'] = t
        resource['categoryId'] = 0
        resource['isOnline'] = False
        resource['source'] = 'recommend'
        resource['updateTime'] = getCurTime()
        resource['tagList'] = []
        for videoTag in entity['tag']:
            if not videoTag:
                continue
            videoTagName = re.sub('<[^<]+?>', '', videoTag['name'])
            videoTagName = videoTagName.split(' ')
            videoTagName = '|'.join(videoTagName)
            resource['tagList'].append(videoTagName)
        if not entity['tag']:
            if resource['resourceName']:
                try:
                    tags = segmentByNLP(resource['resourceName'])
                    if not tags:
                        tags = [resource['resourceName']]
                    resource['tagList'].extend(tags)
                except Exception,e:
                    print e
                    continue
            tempReason = reason.split(' ')
            tempReason = '|'.join(tempReason)
        if tagReason:
            resource['tagList'].insert(0,tempReason)
        else:
            resource['tagList'].append(tempReason)
        for black in blacklist:
            try:
                resource['tagList'].remove(black)
            except ValueError:
                pass
        print("insert ",resource['videoType'],resource['videoId'], resource['resourceUrl'])
        resource['weight'] = -1

        try:
            ret = clct_resource.insert(resource , safe=True)
            resource['resourceId'] = str(ret)
            resource['snapshot'] = 'inQueue'
        except Exception,e:
            print("insert Error!",e)
            try:
                retR  = clct_resource.find_one({'videoType':resource['videoType'], 'videoId':resource['videoId']})
                resource['resourceId'] = str(retR['_id'])
                if retR['isOnline']:
                    resource['snapshot'] = 'done'
                else: continue
            except Exception,x:
                print x

        else:
            '''新增 截图任务'''
            if snapShot:
                mp4box = True if resource['videoType'] == 'sohu_url' else False
                addVideoInfoTask(resource['channelId'],str(ret),resource['videoId'],resource['videoType'],mp4box,force=True,goOnline=True)

        resource['recommendSource'] = source
        resource['recommendReason'] = reason
        resource['isViewed'] = -1
        resource['isPlayed'] = -1
        resource['playTime'] = 0
        resource['createTime'] = t
        result.append(resource)

    return result

getVideoIdUrl = 'http://60.28.29.38:9090/api/getVideoId'

if not debug:
    getVideoIdUrl = 'http://h38:9090/api/getVideoId'

p_1 = re.compile('http://(.*?)/')
p_url = re.compile('http://[\w\./]*')
p_sina = re.compile('http://video.sina.com.cn/v/b/(.*?)\.html')
p_youku = re.compile('http://v.youku.com/v_show/id_(.*?).html')
p_videos = [('sina',p_sina), ('youku',p_youku)]
httpUtil = HttpUtil()

def decodeVideo(videoUrl):
    item = {}
    try:
        for p_video in p_videos:
            if p_video[1].search(videoUrl):
                item['videoType'] = p_video[0]
                item['videoId'] = p_video[1].search(videoUrl).groups()[0]
                break
        else:
            response = httpUtil.Post(getVideoIdUrl, json.dumps({"url":'%s'%videoUrl}))
            if response:
                content = response.decode()
                result = json.loads(content)
                if result.get('videoId',None) is None:
                    return {}
                item['videoType'] = result['videoType']
                item['videoId'] = result['videoId']
                if item['videoType'] == '' or item['videoId'] == '':
                    return {}
    except Exception,e:
        print e
    return item

def buildVideoFromYouku(entities, reason, source, snapShot = False,channelId=101641, viewCount=7000):
    updateMap = {'updateTime':getCurTime()}
    clct_channel.update({'channelId':101641},{'$set':updateMap})

    '''入库'''
    t = getCurTime()
    result = []
    for entity in entities:
        if entity['view_count'] < viewCount or len(entity['title']) < 6:
            continue
        resource = buildResource(entity['link'],entity['title'],channelId,'youku',entity['id'],'video')
        resource['createTime'] = t
        resource['categoryId'] = 0
        resource['isOnline'] = False
        resource['source'] = 'recommend'
        resource['updateTime'] = getCurTime()
        resource['tagList'] = entity['tags'].split(',')
        resource['tagList'].append(entity['category'])
        resource['tagList'].append(reason)
        for black in blacklist:
            try:
                resource['tagList'].remove(black)
            except ValueError:
                pass
        print("insert ",resource['videoType'],resource['videoId'], resource['resourceUrl'])
        resource['weight'] = -1

        try:
            ret = clct_resource.insert(resource , safe=True)
            entity['resourceId'] = str(ret)
            entity['snapshot'] = 'inQueue'
        except Exception,e:
            print("insert Error!",e)
            try:
                retR  = clct_resource.find_one({'videoType':resource['videoType'], 'videoId':resource['videoId']})
                entity['resourceId'] = str(retR['_id'])
                if retR['isOnline']:
                    entity['snapshot'] = 'done'
                else: continue
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
        entity['tags'] = entity['tags'].split(',')
        entity['tags'].append(entity['category'])
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
        entity['snapshot'] = 'done'
    return entities

def retrieveVideo(keywords):
    pass

def upload(videos, uuid):
    insertErrorCount = 0
    for video in videos:
        try:
            retR = clct_resource.find_one({'_id':ObjectId(video['resourceId'])})
            if retR is not None:
                if retR.get('snapshot','') == 'done':
                    video['snapshot'] = retR['snapshot']
            try:
                if not retR['tagList']:
                    newTags = segmentByNLP(retR['resourceName'])
                    clct_resource.update({'_id':retR['_id']},{'$set':{'tagList':newTags}})
                    videos['tagList'] = newTags
            except Exception,e:
                print e
            video['uuid'] = uuid
            video['updateTime']
            ret = clct_userRecommend.insert(video , safe=True)
        except Exception,e:
            print("Insert Error!",e)
            insertErrorCount = insertErrorCount +1
            #Different reason to same recommendation
            '''ret = clct_userRecommend.find_one({'uuid':video['uuid'], 'resourceId':video['resourceId']})
            if cmp(ret['recommendReason'].encode('utf8'), video['recommendReason']) != 0:
                ret['recommendReason'] = ret['recommendReason'].encode('utf8')+' '+video['recommendReason']
                clct_userRecommend.update({'uuid':video['uuid'], 'resourceId':video['resourceId']},{'$set':{'recommendReason':ret['recommendReason']}})'''
        else:
            pass
    return insertErrorCount

def walk(reason, source):
    videos = []
    if reason == '':
        return videos
    try:
        rets = clct_userRecommend.find({'recommendReason':' '.join(reason), 'isPlayed': 1})
        if rets.count() != 0:
            for ret in rets:
                reasonDic = similarWords([ret['recommendReason']])
                for (k, v) in reasonDic.items():
                    for word in v:
                        if word == '' or cmp(word,ret['recommendReason'].encode('utf8')) == 0:
                            continue
                        videos.extend(walk([word, k.encode('utf8')],'%s %s'%(source, k)))
                return videos
        else:
            rets = clct_userRecommend.find({'recommendReason':' '.join(reason)}).sort("createTime", -1)
            if rets.count() == 0:
                return recommend(reason, source)
            else:
                for oldRecommend in rets:
                    cooling = time.mktime(time.localtime()) - time.mktime(time.strptime(oldRecommend['createTime'],'%Y%m%d%H%M%S'))  > 3600*48
                    if cooling:
                        return recommend(reason,source)
                    break
                return videos
    except Exception,e:
        print e,' ',traceback.format_exc()
        return videos

def renewOldRecommend(userId):
    rets = clct_userRecommend.find({'uuid':userId,'isViewed':-1,'snapshot':{'$in':['done','gifDone']}}).limit(100)
    for ret in rets:
        ret['createTime'] = getCurTime()
        clct_userRecommend.update({'_id':ret['_id']}, {'$set':{'createTime':ret['createTime']}})

from dataRecovery import  top_tags,initial_tags
def process(uuid):
    ret = clct_user.find_one({'uuid':uuid})
    if ret is None:
        return False
    similarDic = {}
    similarKeywordsDic = []
    videos = []
    renewOldRecommend(ret['uuid'])

    remainRecommendations = clct_userRecommend.find({'uuid':ret['uuid'],'isViewed':-1,'snapshot':{'$in':['done','gifDone']}})
    if remainRecommendations.count() > 17:
        return

    likeItems = retrieveUserLike(ret['uuid'])
    random.shuffle(likeItems, random.random)
    likeItems = likeItems[0:7]
    for likeItem in likeItems:
        itemTags = likeItem.get('tagList', []) #TODO 人工标签超过6个字 分词
        try:
            if itemTags:
                encodedTags = [x.encode('utf-8') for x in itemTags]
                source = ' '.join(encodedTags[0:3])
                likeItemVideos = recommendByBaidu(encodedTags[0:3], source, source, 101641)
                if not likeItemVideos:
                    continue
                videos.extend(likeItemVideos)
                shortTagDic = similarWords(source)
                if len(shortTagDic.itervalues().next()) == 1: continue
                for (k,v) in shortTagDic.items():
                    for tag in v:
                        tempTags = []
                        tempTags.extend(encodedTags[0:3])
                        tempTags.append(tag)
                        videos.extend(recommendByBaidu(tempTags, tag, k, 101641))
        except Exception,e:
            print e

    records = retrieveUserHistory(ret['uuid'])
    if  ret['sinaId'] == "":
        total = False
    else: total = False
    for record in records:
        similarKeywordsDic = similarWords(record['resourceName'],total,True)
        titleTags = segment(record['resourceName'], True)
        for (k,v) in similarKeywordsDic.items():
            for tag in v:
                tempTags = []
                titleTags = [x.encode('utf-8') for x in titleTags[0:3]]
                tempTags.extend(titleTags)
                tempTags.append(tag)
                video = walk(tempTags, k)
                if video: videos.extend(video)

    try:
        if ret['sinaId'] != "":
            userTags = retrieveUserTag(ret['sinaToken'],ret['sinaId'])
            userTags = list(userTags)
            if userTags:
                random.shuffle(userTags, random.random)
                userTags = userTags[0:7]
                try:
                    encodedUserTags = [x.encode('utf-8') for x in userTags]
                    for encodedTag in encodedUserTags:
                        videos.extend(recommendByBaidu([encodedTag], encodedTag, encodedTag, 101641, 'gb2312', True))
                except Exception,e:
                    print e
                if len(videos) < 5:
                    for userTag in userTags:
                        similarDic = similarWords(userTag)
                        for (k,v) in similarDic.items():
                            for tag in v:
                                tempTags = []
                                tempTags.append(userTag.encode('utf-8'))
                                tempTags.append(tag)
                                video = walk(tempTags, k)
                                if video: videos.extend(video)
    except Exception,e:
        print e

    print uuid,'count: ',len(videos)
    if len(videos) == 0:
        retR = clct_userRecommend.find_one({'uuid':ret['uuid'],'isViewed':-1,'snapshot':{'$regex':'done|gifDone'}})
        try:
            if  retR is None and ret['sinaId'] != "":
                suggestionTags = retrieveSuggestion(ret['sinaToken'])
                if suggestionTags is not None:
                    for suggestionTag in suggestionTags:
                        similarSuggestionDic = similarWords(suggestionTag)
                        for (k,v) in similarSuggestionDic.items():
                            for tag in v:
                                tempTags = []
                                tempTags.append(suggestionTag.encode('utf-8'))
                                tempTags.append(tag)
                                video = walk(tempTags, k)
                                if video: videos.extend(video)
                print uuid,'Sina suggestion count: ',len(videos)
        except Exception,e:
            print e

    if len(videos) == 0:
        retR = clct_userRecommend.find_one({'uuid':ret['uuid'],'isViewed':-1,'snapshot':{'$regex':'done|gifDone'}})
        try:
            if retR is None:
                random.shuffle(top_tags, random.random)
                for topTag in top_tags:
                    topRecommendVideo = clct_resource.find_one({'tagList':topTag}, sort=[("createTime", -1)])
                    videos.extend(buildVideo([topRecommendVideo],topTag,topTag))
        except Exception,e:
            print e

    print uuid, 'total count: ',len(videos)
    insertErrorCount = upload(videos, ret['uuid'])
    if insertErrorCount == len(videos):
        videos = []
        retR = clct_userRecommend.find_one({'uuid':ret['uuid'],'isViewed':-1,'snapshot':{'$regex':'done|gifDone'}})
        try:
            if retR is None:
                random.shuffle(initial_tags, random.random)
                randomCount = 0
                for initialTag in initial_tags:
                    topRecommendVideo = clct_resource.find_one({'tagList':initialTag}, sort=[("createTime", -1)])
                    videos.extend(buildVideo([topRecommendVideo],topTag,topTag))
                    randomCount = randomCount + 1
                    if randomCount > 10:
                        break
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
    #print(process('sina_1837408945'))#352900057858214'))#'))#99000310639035'))#'))#))#)) #huohua_sina_524922ad0cf25568d165cbdd'352900057858214 355882057756233
    main()
    #segmentByNLP("台豪华灵位聘名设计师配“样板房”")
    #recommendByYouku(["ＩＴ","ＮＢＡ"],"","")

