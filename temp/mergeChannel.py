__author__ = 'ding'
from pymongo import Connection

con = Connection('h37:20010')
clct_channel = con.tiercel.channel
clct_resource = con.tiercel.resource
clct_user = con.tiercel.user

CHANNEL_ID_FROM = 100078
CHANNEL_ID_TO = 100074

clct_resource.update({'channelId':CHANNEL_ID_FROM},{'$set':{'channelId':CHANNEL_ID_TO}},multi=True)

clct_user.update({'subscribedChannelList':CHANNEL_ID_FROM},\
                 {\
                     '$pull':{'subscribedChannelList':CHANNEL_ID_FROM},\
                     '$push':{'subscribedChannelList':CHANNEL_ID_TO},\
                 },multi=True)

clct_channel.remove({'channelId':CHANNEL_ID_FROM})
