__author__ = 'ding'

#coding=utf-8
__author__ = 'ding'
from pymongo import Connection
import time

con = Connection('h37:20010')
clct_resource = con.tiercel.resource
clct_channel = con.tiercel.channel

def fix0():
    for resource in clct_resource.find({'updateTime':'00000000000000'}):
        print resource['createTime']
        clct_resource.update({'_id':resource['_id']},{'$set':{'updateTime':resource['createTime']}})


def fixInt():
    for resource in clct_resource.find({'updateTime':{'$type':1}}):
        print resource['createTime']
        print resource['updateTime']
        clct_resource.update({'_id':resource['_id']},{'$set':{'updateTime':resource['createTime']}})


fixInt()