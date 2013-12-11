__author__ = 'ding'
from pymongo import Connection

con = Connection('h37:20010')
clct_channel = con.tiercel.channel
clct_user = con.tiercel.user
clct_resource = con.tiercel.resource

def migrateChannel(fromId,toId):
    clct_resource.update({'channelId':fromId},{'$set':{'channelId':toId}}, multi=True)
    clct_user.update({'subscribedChannelList':fromId}, {'$addToSet':{'subscribedChannelList':toId}},multi=True)
    clct_user.update({'subscribedChannelList':fromId},{'$pull':{'subscribedChannelList':fromId}},multi=True)


migrateChannel(101652,101657)