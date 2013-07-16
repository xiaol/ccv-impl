# coding=utf-8
import json
from time import strftime, localtime 
from datetime import timedelta, date 
import traceback
import calendar 

from weibo import APIClient

WHERE_PLAY_KEY  = '3421733539'#'2816325460'
WHERE_PLAY_SECRET = '7d09a3ef176949de3bde27cfd4cf7c45'#'222824d0f64bacdffe606bdf050ac36f'
WHERE_PLAY_CALLBACK = 'https://api.webo.com/oauth2/default.html'#'http://www.huohua.co'



class SinaSdk():
    
    RET_CODE = 'retcode'
    SINA_CALL_COUNT = 'call_sina_api_count'
    EMPTY_CONTENT =1
    SUCCESS_CODE = 0
    FAILD_CODE = -1
    ERR_MSG = 'errmsg'
    MAX_COUNT = 40000
    LIMITED_CODE = "rate"
    RATE_LIMITED = "rate limited"

    def __init__(self, appKey, appSecret, redirectUri):
        self._client = APIClient(app_key=appKey, app_secret=appSecret, redirect_uri=redirectUri)
    
    def getFriendsBilateral(self, token, uid, page):
        self._client.set_access_token(token, 0.0)
        try:
            year = strftime("%Y",localtime()) 
            mon  = strftime("%m",localtime()) 
            day  = strftime("%d",localtime()) 
            hour = strftime("%H",localtime()) 
            key = year + mon+day+hour
            if(self.redisOfflineOperator.getCount(key)==self.MAX_COUNT):
                ret = {}
                ret[self.LIMITED_CODE]=self.RATE_LIMITED
                ret[self.RET_CODE] = self.FAILD_CODE
                ret[self.ERR_MSG] = 'the request sina is error'
                return ret
            elif(self.redisOfflineOperator.getCount(key)==None):
                self.redisOfflineOperator.updateCount(key, 0)
            ret = self._client.friendships__friends__bilateral(uid=uid, count=200, page=page)
            self.redisOfflineOperator.updateCount(key, 1)
        except:
            print traceback.format_exc()
            self.redisOfflineOperator.updateCount(key, 1)
            ret = {}
            ret[self.RET_CODE] = self.FAILD_CODE
            ret[self.ERR_MSG] = 'the request sina is error'
            return ret
        ret[self.RET_CODE] = self.SUCCESS_CODE
        ret[self.ERR_MSG] = ''
        return ret

    def statusesUpdate(self, token, text):
        self._client.set_access_token(token, 0.0)
        try:
            year = strftime("%Y",localtime()) 
            mon  = strftime("%m",localtime()) 
            day  = strftime("%d",localtime()) 
            hour = strftime("%H",localtime()) 
            key = year + mon+day+hour
            if(self.redisOfflineOperator.getCount(key)==self.MAX_COUNT):
                ret = {}
                ret[self.LIMITED_CODE]=self.RATE_LIMITED
                ret[self.RET_CODE] = self.FAILD_CODE
                ret[self.ERR_MSG] = 'the request sina is error'
                return ret
            elif(self.redisOfflineOperator.getCount(key)==None):
                self.redisOfflineOperator.updateCount(key, 0)
            ret = self._client.post.statuses__update(status=text)
            self.redisOfflineOperator.updateCount(key, 1)
        except:
            print traceback.format_exc()
            self.redisOfflineOperator.updateCount(key, 1)
            ret = {}
            ret[self.RET_CODE] = self.FAILD_CODE
            ret[self.ERR_MSG] = 'the request sina is error'
            return ret
        ret[self.RET_CODE] = self.SUCCESS_CODE
        ret[self.ERR_MSG] = ''
        return ret

    def statusesUpload(self, token, text, pic):
        self._client.set_access_token(token, 0.0)
        try:
            year = strftime("%Y",localtime()) 
            mon  = strftime("%m",localtime()) 
            day  = strftime("%d",localtime()) 
            hour = strftime("%H",localtime()) 
            key = year + mon+day+hour
            if(self.redisOfflineOperator.getCount(key)==self.MAX_COUNT):
                ret = {}
                ret[self.LIMITED_CODE]=self.RATE_LIMITED
                ret[self.RET_CODE] = self.FAILD_CODE
                ret[self.ERR_MSG] = 'the request sina is error'
                return ret
            elif(self.redisOfflineOperator.getCount(key)==None):
                self.redisOfflineOperator.updateCount(key, 0)
            ret = self._client.upload.statuses__upload(status=text, pic=pic)
            self.redisOfflineOperator.updateCount(key, 1)
        except:
            print traceback.format_exc()
            self.redisOfflineOperator.updateCount(key, 1)
            ret = {}
            ret[self.RET_CODE] = self.FAILD_CODE
            ret[self.ERR_MSG] = 'the request sina is error'
            return ret
        
        ret[self.RET_CODE] = self.SUCCESS_CODE
        ret[self.ERR_MSG] = ''
        return ret
    
    def searchStatus(self,token,keyword,pIndex,province, city):
        self._client.set_access_token(token, 0.0)
        ret = None
        try:
            year = strftime("%Y",localtime()) 
            mon  = strftime("%m",localtime()) 
            day  = strftime("%d",localtime()) 
            hour = strftime("%H",localtime()) 
            key = year + mon+day+hour
            ret = self._client.get.search__statuses(q=keyword,page=pIndex,province=province, city=city, count=50, source=WHERE_PLAY_KEY)
            self.redisOfflineOperator.updateCount(key, 1)
            ret[self.RET_CODE] = self.SUCCESS_CODE
            ret[self.ERR_MSG] = ''
            return ret
        except:
            print '======== ret ====='
            print ret
            print traceback.format_exc()
            ret = {}
            ret[self.RET_CODE] = self.FAILD_CODE
            ret[self.ERR_MSG] = 'the request sina is error'
            return ret
    
    
    def usersShow(self, token, uid):
        self._client.set_access_token(token, 0.0)

        year = strftime("%Y",localtime()) 
        mon  = strftime("%m",localtime()) 
        day  = strftime("%d",localtime()) 
        hour = strftime("%H",localtime()) 
        ret = self._client.users__show(uid=uid, source=self._client.client_id)

        return ret

    def collectStatus(self,token,userid,pagecount):
        self._client.set_access_token(token, 0.0)
        try:
            year = strftime("%Y",localtime()) 
            mon  = strftime("%m",localtime()) 
            day  = strftime("%d",localtime()) 
            hour = strftime("%H",localtime()) 
            key = year + mon+day+hour
            if(self.redisOfflineOperator.getCount(key)==self.MAX_COUNT):
                ret = {}
                ret[self.LIMITED_CODE]=self.RATE_LIMITED
                ret[self.RET_CODE] = self.FAILD_CODE
                ret[self.ERR_MSG] = 'the request sina is error'
                return ret
            elif(self.redisOfflineOperator.getCount(key)==None):
                self.redisOfflineOperator.updateCount(key, 0)
            ret = self._client.get.statuses__user_timeline(uid=userid,count=200,page=pagecount)
            self.redisOfflineOperator.updateCount(key, 1)
        except:
            print traceback.format_exc()
            self.redisOfflineOperator.updateCount(key, 1)
            ret = {}
            ret[self.RET_CODE] = self.FAILD_CODE
            ret[self.ERR_MSG] = 'the request sina is error'
            return ret
        
        if(ret == None):
            ret = {}
            ret[self.RET_CODE] = self.EMPTY_CONTENT
            ret[self.ERR_MSG] = 'No content any more'
            return ret
        else:
            ret[self.RET_CODE] = self.SUCCESS_CODE
            ret[self.ERR_MSG] = ''
            return ret
    def searchPoiList(self, token, page, name, city, category = None):
        self._client.set_access_token(token, 0.0)
        try:
            year = strftime("%Y",localtime()) 
            mon  = strftime("%m",localtime()) 
            day  = strftime("%d",localtime()) 
            hour = strftime("%H",localtime()) 
            key = year + mon+day+hour
            if(self.redisOfflineOperator.getCount(key)==self.MAX_COUNT):
                ret = {}
                ret[self.LIMITED_CODE]=self.RATE_LIMITED
                ret[self.RET_CODE] = self.FAILD_CODE
                ret[self.ERR_MSG] = 'the request sina is error'
                return ret
            elif(self.redisOfflineOperator.getCount(key)==None):
                self.redisOfflineOperator.updateCount(key, 0)
            if category is None:
                ret = self._client.place__pois__search(source=self._client.client_id, keyword=name, count='50', page=page, city=city)
            else:
                ret = self._client.place__pois__search(source=self._client.client_id, keyword=name, count='50', page=page, city=city, category=category)
            self.redisOfflineOperator.updateCount(key, 1)
            print ret
        except:
            print traceback.format_exc()
            self.redisOfflineOperator.updateCount(key, 1)
            ret = {}
            ret[self.RET_CODE] = self.FAILD_CODE
            ret[self.ERR_MSG] = 'the request sina is error'
            return ret
        ret[self.RET_CODE] = self.SUCCESS_CODE
        ret[self.ERR_MSG] = ''
        return ret

    def searchPoiPhotoList(self, token, poiid, page):
        self._client.set_access_token(token, 0.0)
        try:
            year = strftime("%Y",localtime()) 
            mon  = strftime("%m",localtime()) 
            day  = strftime("%d",localtime()) 
            hour = strftime("%H",localtime()) 
            key = year + mon+day+hour
            if(self.redisOfflineOperator.getCount(key)==self.MAX_COUNT):
                ret = {}
                ret[self.LIMITED_CODE]=self.RATE_LIMITED
                ret[self.RET_CODE] = self.FAILD_CODE
                ret[self.ERR_MSG] = 'the request sina is error'
                return ret
            elif(self.redisOfflineOperator.getCount(key)==None):
                self.redisOfflineOperator.updateCount(key, 0)
            ret = self._client.place__pois__photos(source=self._client.client_id, count="50", poiid=poiid, page=page)
            self.redisOfflineOperator.updateCount(key, 1)
        except:
            print traceback.format_exc()
            self.redisOfflineOperator.updateCount(key, 1)
            ret = {}
            ret[self.RET_CODE] = self.FAILD_CODE
            ret[self.ERR_MSG] = 'the request sina is error'
            return ret
        ret[self.RET_CODE] = self.SUCCESS_CODE
        ret[self.ERR_MSG] = ''
        return ret
    
    def searchPoiTipList(self, token, poiid, page):
        self._client.set_access_token(token, 0.0)
        try:
            year = strftime("%Y",localtime()) 
            mon  = strftime("%m",localtime()) 
            day  = strftime("%d",localtime()) 
            hour = strftime("%H",localtime()) 
            key = year + mon+day+hour
            if(self.redisOfflineOperator.getCount(key)==self.MAX_COUNT):
                ret = {}
                ret[self.LIMITED_CODE]=self.RATE_LIMITED
                ret[self.RET_CODE] = self.FAILD_CODE
                ret[self.ERR_MSG] = 'the request sina is error'
                return ret
            elif(self.redisOfflineOperator.getCount(key)==None):
                self.redisOfflineOperator.updateCount(key, 0)
            ret = self._client.place__pois__tips(source=self._client.client_id, count="50", poiid=poiid, page=page)
            self.redisOfflineOperator.updateCount(key, 1)
        except:
            print traceback.format_exc()
            self.redisOfflineOperator.updateCount(key, 1)
            ret = {}
            ret[self.RET_CODE] = self.FAILD_CODE
            ret[self.ERR_MSG] = 'the request sina is error'
            return ret
        ret[self.RET_CODE] = self.SUCCESS_CODE
        ret[self.ERR_MSG] = ''
        return ret
    
    def getRedis(self):
            year = strftime("%Y",localtime()) 
            mon  = strftime("%m",localtime()) 
            day  = strftime("%d",localtime()) 
            hour = strftime("%H",localtime()) 
            key = year + mon+day+hour
            ret = {}
            if self.redisOfflineOperator.getCount(key)==self.MAX_COUNT:
                ret[self.LIMITED_CODE]=self.RATE_LIMITED
                ret[self.RET_CODE] = self.FAILD_CODE
                ret[self.ERR_MSG] = 'the request sina is error'
            elif self.redisOfflineOperator.getCount(key)==None:
                self.redisOfflineOperator.updateCount(key, 0)
            return ret

    def putRedis(self, num):
            year = strftime("%Y",localtime()) 
            mon  = strftime("%m",localtime()) 
            day  = strftime("%d",localtime()) 
            hour = strftime("%H",localtime()) 
            key = year + mon+day+hour
            self.redisOfflineOperator.updateCount(key, num)

    def statusesMentions(self, token, page):
        ret = self.getRedis()
        if len(ret) > 0:
            return ret
        try:
            self._client.set_access_token(token, 0.0)
            ret = self._client.statuses__mentions(source=self._client.client_id, count="200", page=page, filter_by_author = '1', trim_user='1')
            ret[self.RET_CODE] = self.SUCCESS_CODE
            ret[self.ERR_MSG] = ''
        except:
            ret = {}
            ret[self.RET_CODE] = self.FAILD_CODE
            ret[self.ERR_MSG] = 'the request sina is error'
        self.putRedis(1)
        return ret

    def commentsToMe(self, token, page):
        ret = self.getRedis()
        if len(ret) > 0:
            return ret
        try:
            self._client.set_access_token(token, 0.0)
            ret = self._client.comments__to_me(source=self._client.client_id, count="200", page=page, filter_by_author = '1')
            ret[self.RET_CODE] = self.SUCCESS_CODE
            ret[self.ERR_MSG] = ''
        except:
            ret = {}
            ret[self.RET_CODE] = self.FAILD_CODE
            ret[self.ERR_MSG] = 'the request sina is error'
        self.putRedis(1)
        return ret

    def commentsByMe(self, token, page):
        ret = self.getRedis()
        if len(ret) > 0:
            return ret
        try:
            self._client.set_access_token(token, 0.0)
            ret = self._client.comments__by_me(source=self._client.client_id, count="200", page=page)
            ret[self.RET_CODE] = self.SUCCESS_CODE
            ret[self.ERR_MSG] = ''
        except:
            ret = {}
            ret[self.RET_CODE] = self.FAILD_CODE
            ret[self.ERR_MSG] = 'the request sina is error'
        self.putRedis(1)
        return ret

    def getAttentionIds(self, token, uid):
        ret = self.getRedis()
        if len(ret) > 0:
            return ret
        try:
            self._client.set_access_token(token, 0.0)
            ret = self._client.friendships__friends__ids(source = self._client.client_id, uid = uid, count = 5000)
            ret[self.RET_CODE] = self.SUCCESS_CODE
            ret[self.ERR_MSG] = ''
        except:
            ret = {}
            ret[self.RET_CODE] = self.FAILD_CODE
            ret[self.ERR_MSG] = 'the request sina is error'
        self.putRedis(1)
        return ret
    
class WherePlaySdk(SinaSdk):
    def __init__(self):
        SinaSdk.__init__(self, WHERE_PLAY_KEY, WHERE_PLAY_SECRET, WHERE_PLAY_CALLBACK)
#        self._client = APIClient(app_key=WHERE_PLAY_KEY, app_secret=WHERE_PLAY_SECRET, redirect_uri=WHERE_PLAY_CALLBACK)
#        self.redisOfflineOperator = RedisOfflineOperator()

if __name__ == '__main__':
    test = WherePlaySdk()
#    print test.statusesMentions('2.002Zb74BdMPZjDf09ca74e42RwEUpB',1)
#    print test.searchPoiList('2.00XdogmBdMPZjDcc78da407eTDjUQD', '1', '史家13号', '0010', '64')
#    print test.searchPoiTipList('2.002Zb74BdMPZjDf09ca74e42RwEUpB', 'B2094654D56EA5F5419C', '1')
#    print test.collectStatus('2.002Zb74BdMPZjDf09ca74e42RwEUpB', '2026808670', '1')
    import json
    print json.dumps(test.usersShow('2.004t5RdCMuAbED17969f330diAZbaC', '1733276337'))

#    print test.usersShow('2.00he1aDDMuAbED80d402b42dZMwW2D', 2026808670)

