#coding=utf-8
__author__ = 'ding'

from pymongo import Connection
import pprint,json,urllib2,time

con = Connection('h37:20010')
clct_user = con.tiercel.user
APP_KEY = '2603329849'



userList =  clct_user.find({'sinaToken':{'$ne':''}})

print '微博用户',userList.count()

for user in userList:
    URL = 'https://api.weibo.com/2/users/show.json?source=%s&access_token=%s&uid=%s'%(APP_KEY,user['sinaToken'],user['sinaId'])
    try:
        data = json.loads(urllib2.urlopen(URL).read())
    except:
        import  traceback
        #print traceback.format_exc()
        continue
    if not data['verified']:
        time.sleep(0.5)
        continue
    print data['idstr'], data['name'],',认证理由:',data['verified_reason'],',认证类型:',data['verified_type'],\
        ',描述信息:',data['description']

    time.sleep(0.2)
