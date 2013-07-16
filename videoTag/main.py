#coding=utf-8
from setting import TokenList,clct_user,clct_tag,clct_status,clct_relationConcern
from WeiboSdk import WeiboSdk
import random,json



def CrawlUserList(tokenList, startUid, limit, minStatusNumber= None,minFollowerNumber = None):
    _WeiboSdk = WeiboSdk()
    UserSet = set([])
    ret = [startUid]
    begin = 0
    while len(UserSet) < limit:
        token = random.choice(tokenList)
        users= set(_WeiboSdk.getAllBiFriendsId(token, ret[begin], minStatusNumber, minFollowerNumber))
        newUsers = users - UserSet
        UserSet |= users 
        print len(UserSet),len(newUsers)
        ret += list(newUsers)
        begin += 1
        
    return list(UserSet)


def GetTags(tokenList,uids):
    _WeiboSdk = WeiboSdk()
    ret = []
    while True:
        if len(uids) > 20:
            uidss = uids[:20]
            uids = uids[20:]
        else:
            uidss = uids
            uids = []
        
        #- - -- - - -
        
        token = random.choice(tokenList)
        result =  _WeiboSdk.tags_tags_batch(token, uidss)
        print json.dumps(result)
        for one in result:
            tags = []
            for tag in  one['tags']:
                for key in tag:
                    if key != 'weight':
                        tags.append(tag[key])
            one['tags'] = tags
            print one
        ret += result
        clct_tag.insert(result)
        if uids == []:
            break
    return ret


def GetStatus(tokenList,uids):
    _WeiboSdk = WeiboSdk()
    for uid in uids:
        if clct_status.find_one({'uid':uid},{'_id':1}):
            print 'continue'
            continue
        token = random.choice(tokenList)
        statuses = _WeiboSdk.statuses_user_timeline_all(token,uid,1)
        #分开多条记录
        #records = [{'uid':uid, 'status':status} for status in statuses]
        #单条记录
        record = {'uid':uid,'statuses':statuses}
        clct_status.insert(record)
    
    return



def getUsers():
    with open('UserList5w.json','wb') as f:
        userList =  CrawlUserList(TokenList,'1733276337',50000,100,100)
        f.write(json.dumps(userList))


def getTags():
    users = [one['uid'] for one in list(clct_status.find({},{'uid':1}))]
    #只要有一个不行就重试
    users = filter(lambda uid:not clct_tag.find_one({'id':uid},{'_id':1}),users)
    print len(users)
    GetTags(TokenList,users)


def getStatus():
    while True:
        try:
            with open('UserList5w.json') as f:
                users = json.loads(f.read())
                GetStatus(TokenList,users)
        except:
            import time
            time.sleep(10)
            continue
        break

def getStatus2():
    while True:
        try:
            print 'start'
            users = []
            for one in clct_relationConcern.find():
                print len(one['concern'])
                users.extend(one['concern'])
                if len(users) > 60000:
                    break
            print len(users)
            GetStatus(TokenList,users)
        except:
            import time
            time.sleep(10)
            continue
        break

if __name__ == '__main__':
    #getTags()
    #GetStatus(TokenList,[1704106354,1642857884,1589124154,1819501237,1763750687,1960368935,1700085910,1717931492])
    #GetTags(TokenList,[1704106354,1642857884,1589124154,1819501237,1763750687,1960368935,1700085910,1717931492])
    getStatus2()