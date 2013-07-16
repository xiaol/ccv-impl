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
    channelId = ''
    source = ''
    videoId = ''
    videoType = ''
    oldExt = ''
    ext = ''
    createTime = '00000000000000'
    modifyTime = '00000000000000'
    type = ''
    hot = -1
    number = -1


class Category(DomainBase):
    categoryName = ''
    categoryId = 0
    description = '' 
    imageUrl = ''
    createTime = '00000000000000'
    modifyTime = '00000000000000'
    weight = 0
    categoryType = 0
    
    
class Channel(DomainBase):
    channelDescription = ''
    channelId  =  0
    channelImageUrl = ''
    channelName = ''
    channelType  = 0
    createTime = '00000000000000'
    modifyTime = '00000000000000'
    updateTime = '00000000000000'
    onlineStatus = 0
    description = ''
    sourceList  = []
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


class Tag(DomainBase):
    name = ''
    refNum = 0
    createTime = '00000000000000'
    modifyTime = '00000000000000'