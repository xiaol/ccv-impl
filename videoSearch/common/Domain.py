#coding=utf-8

class DomainBase():
    def __init__(self):
        self.data = {}
        
    def __setitem__(self,key,value):
        if key not in self.__class__.__dict__:
            raise AttributeError('%s not found'%key)
        self.data[key] = value
    
    def __getitem__(self,key):
        if key in self.data:
            return self.data[key]
        if key not in self.__class__.__dict__:
            raise AttributeError('%s not found'%key)
        return self.__class__.__dict__[key]
    
    
    def getInsertDict(self):
        ret = {}
        for key in self.__class__.__dict__:
            if key.startswith('__'):continue
            if key not in self.data:
                ret[key] = self.__class__.__dict__[key]
            else:
                ret[key] = self.data[key]
        return ret
    
    def getUpdateDict(self):
        return self.data





class Resource(DomainBase):
    resourceSize = -1
    resourceUrl = ''
    resourceName = ''
    resourceImageUrl = ''
    resourceImageUrl2 = ''
    duration = -1
    channelId = -1
    categoryId = -1
    source = ''
    videoId = ''
    videoType = ''
    oldExt = ''
    ext = ''
    createTime = '00000000000000'
    modifyTime = '00000000000000'
    updateTime = '00000000000000'
    type = ''
    hot = -1
    number = -1
    isOnline = True
    tagList = []
    videoFileName = ''
    snapshot = ''
    downloadType = ''
    v_br = -1
    v_size = [0,0]
    weight = -1
    playNumber = 0
    downloadNumber = 0
    gameName = ''
    gameUrl = ''
    scheduleGoOnline = ''
    gifUrl = ''
    subtitle = ''
    isLD = False
    resolution = -1
    '''resolution:
    0:流畅， 1:标清， 2:高清 3:超清 4:原画
    '''
    isRecommend = False
    recReason = ''
    likeNum = 0
    shareNum = 0
    dislikeNum = 0
    editor = -1
    review = 0 #0 待审核，-1 审核不通过, 1 审核通过


class Category(DomainBase):
    categoryName = ''
    categoryId = 0
    description = '' 
    imageUrl = ''
    createTime = '00000000000000'
    modifyTime = '00000000000000'
    weight = 0
    categoryType = 0
    subtitle = ''
    
    '''0 电影, 1 电视剧,2 短视频'''
    videoClass = 0
    logoUrl = ''
    isOnline = True
    isFirst = False
    
    
    
class Channel(DomainBase):
    channelDescription = ''
    channelId  =  0
    channelImageUrl = ''
    resourceImageUrl = ''
    channelName = ''
    channelType  = 0
    createTime = '00000000000000'
    modifyTime = '00000000000000'
    updateTime = '00000000000000'
    nextSearchTime = '00000000000000'
    searchTime = '00000000000000'
    
    onlineStatus = 0
    description = ''
    sourceList  = []
    searchHandleList = []
    tagList = []
    starLevel = 0
    subscribeNum = 0
    tvNumber = 0
    oriUrl = ''
    isNewest = False
    identifer = 0
    sourceWebsite = ''
    processed = False
    weight = 0
    categoryType = 0
    handleName = ''
    handleArgs = ''
    handleFrequents = ''
    autoOnline = True
    subtitle = ''
    duration = -1
    daysAhead = 2
    autoSub = False
    
    yyetsSeason = ''
    yyetsEncode = ''
    yyetsDownMode = ''
    
    onSquare = False
    poster = ''

    videoClass = -1
    
    detailDirecter = ''
    detailLeadingRole = []
    detailMovieCategory = []
    detailDistrict = ''
    detailLanguage = ''
    detailReleaseDate = ''
    detailDoubanUrl = ''
    detailDuration = ''
    detaildoubanScore = -1
    detailDescription = ''
    detailTrailerUrl = ''
    detailTrailerVideoType = ''
    detailTrailerVideoId = ''
    detailTotalTvNumber = -1
    
    detailTrailerList = []
    '''
        [
         {
             "url":"",
             "videoType":"",
             "videoId","",
             "title"
         },
         ...
        ]
    '''
    isRecommend = False
    type = ''
    snapShot = False
    snapShotGoOnline = False
    recReason = ''


class Tag(DomainBase):
    name = ''
    refNum = 0
    createTime = '00000000000000'
    modifyTime = '00000000000000'

class VideoInfoTask(DomainBase):
    channelId = -1
    mp4box = False
    resourceId = ''
    videoId = ''
    videoType = ''
    force = False
    goOnline = False
    type = ''
    priority = 0


class CDNSyncTask(DomainBase):
    channelId = -1
    resourceId = ''
    videoId = ''
    videoType = ''

class UserWeibo(DomainBase):
    weiboId = -1
    sinaId = ''
    sinaName =''
    title = ''
    comment = ''
    friendId = -1
    friendScreenName = ''
    friendName = ''
    friendProfileImageUrl = ''
    friendCoverImageUrl = ''
    friendGender = ''
    retweetedFriendId = -1
    retweetedFriendScreenName = ''
    retweetedFriendName = ''
    retweetedFriendProfileImageUrl = ''
    retweetedFriendCoverImageUrl = ''
    retweetedFriendGender = ''
    repostsCount = 0
    commentsCount = 0
    attitudesCount = 0
    videoScreenshotUrl = ''
    videoUrl = ''
    resourceId = ''
    createTime = '00000000000000'
    modifyTime = '00000000000000'
    updateTime = '00000000000000'



class Topic(DomainBase):
    title = ''
    description = ''
    isOnline = False
    picture = ''
    weight = -1
    content = []
    createTime = '00000000000000'
    modifyTime = '00000000000000'
    updateTime = '00000000000000'



class TopicListPage(DomainBase):
    skip = 0
    page = 0
    limit = 0
    id = ''
    name = ''
    mongo = ''
    isOnline = False
    sort = ''


class Editor(DomainBase):
    id = -1
    role = ''
    name = ''
    password = ''
    lastLoginTime = ''
    lastLoginIp = ''
    avatar = ''
    email = ''
