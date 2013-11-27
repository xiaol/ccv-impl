#coding=utf-8
__author__ = 'ding'

from pymongo import Connection
import time,json

con = Connection('h39:20010')
clct_operationLog = con.tiercel.operationLog

def main():
    logs = clct_operationLog.find({'operationCode':{'$in':[30008,30009,30010]},'operationTime':{'$gte':'20131113','$lt':'20131120'}},{'operationTime':1})
    sum = logs.count()
    S = {}
    for log in logs:
        time = log['operationTime'][8:10]
        if time not in S:
            S[time] = 0
        S[time] += 1

    items = S.items()
    items.sort(key=lambda a:int(a[0].split(':')[0]))
    for item in items:
        print item[0],item[1], '%.2f%%'%(100.0*item[1]/sum)


if __name__ == '__main__':
    main()