#coding=utf-8
__author__ = 'ding'

from pymongo import Connection
import pprint,json,urllib2,time

con = Connection('h37:20010')
clct_channel = con.tiercel.channel




for channel in clct_channel.find():
    try:
        _ = int(channel['subtitle'])
        clct_channel.update({'_id':channel['_id']},{'$set':{'subtitle':''}})
    except:
        print channel['subtitle']