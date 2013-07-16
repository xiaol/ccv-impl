#coding=utf-8
from weibo import APIClient

WHERE_PLAY_KEY  = '3421733539'#'2816325460'
WHERE_PLAY_SECRET = '7d09a3ef176949de3bde27cfd4cf7c45'#'222824d0f64bacdffe606bdf050ac36f'
WHERE_PLAY_CALLBACK = 'https://api.webo.com/oauth2/default.html'#'http://www.huohua.co'


class WeiboSdk():
    def __init__(self, appKey = WHERE_PLAY_KEY, appSecret = WHERE_PLAY_SECRET, redirectUri = WHERE_PLAY_CALLBACK):
        self._client = APIClient(app_key=appKey, app_secret=appSecret, redirect_uri=redirectUri)
        
        
    def users_show(self, token, uid):
        self._client.set_access_token(token, 0.0)
        data = self._client.users__show(uid=uid, source=self._client.client_id,access_token=token)
        return data
    
    def statuses_user_timeline(self,token,uid,feature,page,count):
        self._client.set_access_token(token, 0.0)
        data = self._client.statuses__user_timeline(uid=uid, source=self._client.client_id,access_token=token,feature=feature,trim_user=1,page=page,count=count)
        return data
    
    
    def friendships_friends_bilateral(self,token, uid, page, count):
        self._client.set_access_token(token, 0.0)
        data = self._client.friendships__friends__bilateral(uid=uid, source=self._client.client_id,access_token=token,page=page,count=count)
        return data
    
    
    def tags_tags_batch(self,token, uids):
        self._client.set_access_token(token, 0.0)
        data = self._client.tags__tags_batch(uids=','.join(map(str,uids)), source=self._client.client_id, access_token=token)
        return data
    
    #----------------------------------------------
    
    def statuses_user_timeline_all(self,token,uid,feature=0):
        '''
            feature    false    int    过滤类型ID，0：全部、1：原创、2：图片、3：视频、4：音乐，默认为0。
        '''
        ret = []
        page = 1
        while True:
            data = self.statuses_user_timeline(token,uid,feature,page,100)
            ret += [status['text'] for status in data['statuses']]
            if len(data['statuses']) == 0:
                break
            page += 1
        return ret
    
    def getAllBiFriendsId(self, token, uid, minStatusNumber= None,minFollowerNumber = None):
        ret = []
        page = 1
        while True:
            data = self.friendships_friends_bilateral(token,uid,page,100)
            if minStatusNumber:
                data['users'] = filter(lambda a:a['statuses_count'] > minStatusNumber, data['users'])
            if minFollowerNumber:
                data['users'] = filter(lambda a:a['followers_count'] > minFollowerNumber, data['users'])
            
            ret += [user['id'] for user in data['users']]
            if len(data['users']) == 0:
                break
            page += 1
        return ret
        
        
        
if __name__ == '__main__':
    sdk = WeiboSdk()
    #print sdk.users_show('2.004t5RdCdMPZjD7c15db547dISSRHC' ,'1733276337')
    #print sdk.ext_statuses_user_timeline_all('2.004t5RdCdMPZjD7c15db547dISSRHC' ,'1733276337')
    print len(sdk.getAllBiFriendsId('2.004t5RdCdMPZjD7c15db547dISSRHC' ,'1733276337' ,10,100))
    #print sdk.statuses_user_timeline('2.004t5RdCdMPZjD7c15db547dISSRHC' ,'1733276337',1,100)
    