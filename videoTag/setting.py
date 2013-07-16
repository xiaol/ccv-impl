#coding=utf-8
from pymongo import Connection

TokenList = ['2.004t5RdCdMPZjD7c15db547dISSRHC']

con = Connection('60.28.29.37:20010')
clct_user = con.weibo.user
clct_tag = con.weibo.tag
clct_status = con.weibo.status
clct_relationConcern = con.weibo.relationConcern