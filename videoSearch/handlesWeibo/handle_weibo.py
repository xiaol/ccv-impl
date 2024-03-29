#coding=utf-8
import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from setting import debug
from lxml import etree
import re,pprint,json,time, datetime
from common.common import getCurTime
from pymongo import Connection
from common.Domain import Resource,Channel,UserWeibo
from common.HttpUtil import get_html,HttpUtil, downloadGif

p_1 = re.compile('http://(.*?)/')
p_url = re.compile('http://[\w\./]*')
p_sina = re.compile('http://video.sina.com.cn/v/b/(.*?)\.html')
p_youku = re.compile('http://v.youku.com/v_show/id_(.*?).html')
#p_56 = re.compile('v_([^\.]+).html')

p_videos = [('sina',p_sina), ('youku',p_youku)]
p_2 = re.compile('\S.(?P<type>\w+)$')

getVideoIdUrl = 'http://60.28.29.38:9090/api/getVideoId'

job_server = None
if  not debug:
    import pp
    # tuple of all parallel python servers to connect with
    ppservers = ()
    #ppservers = ("10.0.0.1",)
    if len(sys.argv) > 1:
        ncpus = int(sys.argv[1])
        # Creates jobserver with ncpus workers
        job_server = pp.Server(ncpus, ppservers=ppservers)
    else:
        # Creates jobserver with automatically detected number of workers
        job_server = pp.Server(ppservers=ppservers)
    print "pp 可以用的工作核心线程数", job_server.get_ncpus(), "workers"
    getVideoIdUrl = 'http://h38:9090/api/getVideoId'


def handle(channelId, access_token, since_id, sinaId, sinaName, page=1,count=20):
    httpUtil = HttpUtil()
    # 列表页
    url = 'https://api.weibo.com/2/statuses/home_timeline.json?' \
          'access_token=%s&since_id=%s&page=%s&count=%s&feature=3'%(access_token,since_id,page,count)
    print url
    html = get_html(url)
    videos = json.loads(html)['statuses']
    print len(videos)
    videoList  = []
    jobs = []
    for video in  videos:
        if debug:
            item = decodeWeibo(video, httpUtil, sinaId, sinaName)
            if item is None:
                continue
            videoList.append({'resource':buildResource(item['videoUrl'] , item['title'], channelId, item['videoType'], item['videoId'],'video'),
                              'userWeibo':buildUserWeibo(item)})
        else:
            jobs.append(job_server.submit(pDecodeWeibo, (video, sinaId, sinaName, getVideoIdUrl ), (),
                                          ("from common.HttpUtil import HttpUtil", "import re", "import json")))
    if not debug:
        for job in jobs:
            item = job()
            if item is None:
                continue
            videoList.append({'resource':buildResource(item['videoUrl'] , item['title'], channelId, item['videoType'], item['videoId'],'video'),
                              'userWeibo':buildUserWeibo(item)})

    return videoList

def handleGif(channelId, access_token, since_id, sinaId, sinaName, page=1,count=20):
    httpUtil = HttpUtil()
    # 列表页
    url = 'https://api.weibo.com/2/statuses/home_timeline.json?' \
          'access_token=%s&since_id=%s&page=%s&count=%s&feature=2'%(access_token,since_id,page,count)
    print url
    html = get_html(url)
    images = json.loads(html)['statuses']
    print len(images)
    gifList  = []
    for image in  images:
        if 'retweeted_status' in image:
            imageUrl = image['retweeted_status']['bmiddle_pic']
        else:
            imageUrl = image['bmiddle_pic']
        m = p_2.search(imageUrl)
        type = m.group('type')
        if cmp(type,'gif') == 0:
            item = decodeImageWeibo(image, httpUtil, sinaId, sinaName)
            videoId, resourceImageUrl = downloadGif(item['videoUrl'], channelId)
            if videoId and resourceImageUrl:
                gifList.append({'resource':buildGifResource(item['videoUrl'] , item['title'], channelId, videoId, resourceImageUrl),
                             'userWeibo':buildUserWeibo(item)})
    return gifList

def pDecodeWeibo(video, sinaId, sinaName, getVideoIdUrl):
    httpUtil = HttpUtil()

    p_1 = re.compile('http://(.*?)/')
    p_url = re.compile('http://[\w\./]*')
    p_sina = re.compile('http://video.sina.com.cn/v/b/(.*?)\.html')
    p_youku = re.compile('http://v.youku.com/v_show/id_(.*?).html')
    p_56 = re.compile('v_([^\.]+).html')
    p_videos = [('sina',p_sina), ('youku',p_youku)]

    item = {}
    if 'retweeted_status' in video:
        comment = video['text']
        text = video['retweeted_status']['text']
    else:
        text = video['text']
        comment = ''
        #print video['text']
    #try:
    item['url'] = p_url.findall(text)
    hit = False
    for url in item['url']:
        realUrl = httpUtil.real_url(url)
        for p_video in p_videos:
            if p_video[1].search(realUrl):
                item['videoType'] = p_video[0]
                item['videoId'] = p_video[1].search(realUrl).groups()[0]
                hit = True
                break
            else:
                continue
        if hit:
            break
        else:
            response = httpUtil.Post(getVideoIdUrl, json.dumps({"url":'%s'%realUrl}))
            if response:
                content = response.decode()
                result = json.loads(content)
                if result.get('videoId',None) is None:
                    continue
                if result['videoId'] == '' or result['videoType'] == '':
                    continue

                item['videoType'] = result['videoType']
                item['videoId'] = result['videoId']
                hit = True
                break
    if not hit:
        return None

    item['videoUrl'] = realUrl
    item['title'] = text
    item['sinaId'] = sinaId
    item['sinaName'] = sinaName
    item['weiboId'] = video['id']
    item['comment'] = comment
    item['friendId'] = video['user']['id']
    item['friendName'] = video['user']['name']
    item['friendScreenName'] = video['user']['screen_name']
    item['friendProfileImageUrl'] = video['user']['profile_image_url']
    if 'cover_image' in video['user']:
        item['friendCoverImageUrl'] = video['user']['cover_image']
    item['friendGender'] = video['user']['gender']
    item['repostsCount'] = video['reposts_count']
    item['commentsCount'] = video['comments_count']
    item['attitudesCount'] = video['attitudes_count']
    item['created_at'] = video['created_at']
    if 'bmiddle_pic' in video:
        item['videoScreenshotUrl'] = video['bmiddle_pic']

    if 'retweeted_status' in video:
        item['retweetedFriendId'] = video['retweeted_status']['user']['id']
        item['retweetedFriendName'] = video['retweeted_status']['user']['name']
        item['retweetedFriendScreenName'] = video['retweeted_status']['user']['screen_name']
        item['retweetedFriendProfileImageUrl'] = video['retweeted_status']['user']['profile_image_url']
        if 'cover_image' in video['retweeted_status']['user']:
            item['retweetedFriendCoverImageUrl'] = video['retweeted_status']['user']['cover_image']
        item['retweetedFriendGender'] = video['retweeted_status']['user']['gender']

        #except:
        #print "Decode exception."
        #continue
        #print item
    return item

def decodeWeibo(video, httpUtil, sinaId, sinaName):
    item = {}
    if 'retweeted_status' in video:
        comment = video['text']
        text = video['retweeted_status']['text']
    else:
        text = video['text']
        comment = ''
        #print video['text']
    #try:
    item['url'] = p_url.findall(text)
    hit = False
    for url in item['url']:
        realUrl = httpUtil.real_url(url)
        for p_video in p_videos:
            if p_video[1].search(realUrl):
                item['videoType'] = p_video[0]
                item['videoId'] = p_video[1].search(realUrl).groups()[0]
                hit = True
                break
            else:
                continue
        if hit:
            break
        else:
            response = httpUtil.Post('http://60.28.29.38:9090/api/getVideoId',
                                     json.dumps({"url":'%s'%realUrl}))
            if response:
                content = response.decode()
                result = json.loads(content)
                if result.get('videoId',None) is None:
                    continue
                if result['videoId'] == '' or result['videoType'] == '':
                    continue

                item['videoType'] = result['videoType']
                item['videoId'] = result['videoId']
                hit = True
                break
    if not hit:
        return None

    item['videoUrl'] = realUrl
    item['title'] = text
    item['sinaId'] = sinaId
    item['sinaName'] = sinaName
    item['weiboId'] = video['id']
    item['comment'] = comment
    item['friendId'] = video['user']['id']
    item['friendName'] = video['user']['name']
    item['friendScreenName'] = video['user']['screen_name']
    item['friendProfileImageUrl'] = video['user']['profile_image_url']
    if 'cover_image' in video['user']:
        item['friendCoverImageUrl'] = video['user']['cover_image']
    item['friendGender'] = video['user']['gender']
    item['repostsCount'] = video['reposts_count']
    item['commentsCount'] = video['comments_count']
    item['attitudesCount'] = video['attitudes_count']
    item['created_at'] = video['created_at']
    if 'bmiddle_pic' in video:
        item['videoScreenshotUrl'] = video['bmiddle_pic']

    if 'retweeted_status' in video:
        item['retweetedFriendId'] = video['retweeted_status']['user']['id']
        item['retweetedFriendName'] = video['retweeted_status']['user']['name']
        item['retweetedFriendScreenName'] = video['retweeted_status']['user']['screen_name']
        item['retweetedFriendProfileImageUrl'] = video['retweeted_status']['user']['profile_image_url']
        if 'cover_image' in video['retweeted_status']['user']:
            item['retweetedFriendCoverImageUrl'] = video['retweeted_status']['user']['cover_image']
        item['retweetedFriendGender'] = video['retweeted_status']['user']['gender']

        #except:
        #print "Decode exception."
        #continue
        #print item
    return item

def decodeImageWeibo(image, httpUtil, sinaId, sinaName):
    item = {}
    if 'retweeted_status' in image:
        comment = image['text']
        text = image['retweeted_status']['text']
        imageUrl = image['retweeted_status']['bmiddle_pic']
    else:
        text = image['text']
        comment = ''
        imageUrl = image['bmiddle_pic']
        #print video['text']
    #try:
    item['videoUrl'] = imageUrl
    item['videoId'] = imageUrl
    item['videoType'] = 'gifUrl'
    item['title'] = text
    item['sinaId'] = sinaId
    item['sinaName'] = sinaName
    item['weiboId'] = image['id']
    item['comment'] = comment
    item['friendId'] = image['user']['id']
    item['friendName'] = image['user']['name']
    item['friendScreenName'] = image['user']['screen_name']
    item['friendProfileImageUrl'] = image['user']['profile_image_url']
    if 'cover_image' in image['user']:
        item['friendCoverImageUrl'] = image['user']['cover_image']
    item['friendGender'] = image['user']['gender']
    item['repostsCount'] = image['reposts_count']
    item['commentsCount'] = image['comments_count']
    item['attitudesCount'] = image['attitudes_count']
    item['created_at'] = image['created_at']
    if 'bmiddle_pic' in image:
        item['videoScreenshotUrl'] = image['bmiddle_pic']

    if 'retweeted_status' in image:
        item['retweetedFriendId'] = image['retweeted_status']['user']['id']
        item['retweetedFriendName'] = image['retweeted_status']['user']['name']
        item['retweetedFriendScreenName'] = image['retweeted_status']['user']['screen_name']
        item['retweetedFriendProfileImageUrl'] = image['retweeted_status']['user']['profile_image_url']
        if 'cover_image' in image['retweeted_status']['user']:
            item['retweetedFriendCoverImageUrl'] = image['retweeted_status']['user']['cover_image']
        item['retweetedFriendGender'] = image['retweeted_status']['user']['gender']

        #except:
        #print "Decode exception."
        #continue
        #print item
    return item

def buildUserWeibo(item):
    userWeibo = UserWeibo()

    userWeibo['videoUrl'] = item['videoUrl']
    userWeibo['title'] = item['title']
    userWeibo['sinaId'] = item['sinaId']
    userWeibo['sinaName'] = item['sinaName']
    userWeibo['weiboId'] = item['weiboId']
    userWeibo['comment'] = item['comment']
    userWeibo['friendId'] = item['friendId']
    userWeibo['friendName'] = item['friendName']
    userWeibo['friendScreenName'] = item['friendScreenName']
    userWeibo['friendProfileImageUrl'] = item['friendProfileImageUrl']
    if 'cover_image' in item:
        userWeibo['friendCoverImageUrl'] = item['friendCoverImageUrl']
    userWeibo['friendGender'] = item['friendGender']
    userWeibo['repostsCount'] = item['repostsCount']
    userWeibo['commentsCount'] = item['commentsCount']
    userWeibo['attitudesCount'] = item['attitudesCount']
    if 'videoScreenshotUrl' in item:
        userWeibo['videoScreenshotUrl'] = item['videoScreenshotUrl']

    if 'retweetedFriendId' in item:
        userWeibo['retweetedFriendId'] = item['retweetedFriendId']
        userWeibo['retweetedFriendName'] = item['retweetedFriendName']
        userWeibo['retweetedFriendScreenName'] = item['retweetedFriendScreenName']
        userWeibo['retweetedFriendProfileImageUrl'] = item['retweetedFriendProfileImageUrl']
        if 'cover_image' in item:
            userWeibo['retweetedFriendCoverImageUrl'] = item['retweetedFriendCoverImageUrl']
        userWeibo['retweetedFriendGender'] = item['retweetedFriendGender']

    userWeibo['createTime'] = getCurTime()
    userWeibo['modifyTime'] = getCurTime()
    timeList = item['created_at'].split(' ')
    del timeList[-2]
    strTime = ' '.join(timeList)
    weiboTime = time.strptime(strTime, "%a %b %d %H:%M:%S %Y")
    timeStamp =  time.mktime(weiboTime)
    userWeibo['updateTime'] = getCurTime()#datetime.datetime.fromtimestamp(timeStamp).strftime('%Y%m%d%H%M%S')

    return userWeibo.getInsertDict()

def buildResource(url,title,channelId,videoType,videoId,type):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = type
    resource['videoType'] = videoType
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()
    resource['modifyTime'] = getCurTime()

    return resource.getInsertDict()

def buildGifResource(url,title,channelId,videoId, resourceImageUrl):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'gif'
    resource['videoType'] =  'gif'
    resource['videoId'] =  videoId#videoUrl
    resource['createTime'] = getCurTime()
    resource['modifyTime'] = getCurTime()
    resource['resourceImageUrl'] = resourceImageUrl

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handleGif(0,'2.00JAa2ACfsSuoB59e11ed8f40Kt3ip','3625753381928262', '1837408945', '__刘潇'))

