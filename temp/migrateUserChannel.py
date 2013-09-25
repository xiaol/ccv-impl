from pymongo import Connection


con = Connection('h37:20010')

clct_userChannel = con.tiercel.userChannel
clct_user = con.tiercel.user

userMap = {}

for userChannel in clct_userChannel.find({},{'uuid':1,'channelId':1},timeout=False):
    if 'uuid' not in userChannel:
        continue
    if userChannel['uuid'] not in userMap:
        userMap[userChannel['uuid']] = []
    userMap[userChannel['uuid']].append(userChannel['channelId'])


for key in userMap:
    print userMap[key]