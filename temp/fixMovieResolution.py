__author__ = 'ding'

#coding=utf-8
__author__ = 'ding'
from pymongo import Connection
import time

con = Connection('h37:20010')
clct_resource = con.tiercel.resource
clct_channel = con.tiercel.channel
clct_category = con.tiercel.category




def fixInt():
    channelids  =  [channel['channelId']  for channel in list(clct_channel.find({'channelType':22},{'channelId':1}))]
    for resource in clct_resource.find({'channelId':{'$in':channelids}}):
        print resource['resourceName']
        clct_resource.update({'_id':resource['_id']}, {'$set':{'resolution':2}})

fixInt()