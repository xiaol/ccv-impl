from pymongo import Connection


con = Connection('60.28.29.37:20010')

clct_userChannel = con.tiercel.userChannel
clct_user = con.tiercel.user

userMap = {}

for userChannel in clct_userChannel.find({},timeout=False):
    if 'uuid' not in userChannel:
        continue
    if userChannel['uuid'] not in userMap:
        userMap['uuid'] = []
    userMap['uuid'].append(userChannel['channelId'])


for key in userMap:
    print userMap[key]