#coding=utf-8
__author__ = 'ding'

from pymongo import Connection
import time,json

con = Connection('h39:20010')
clct_operationLog = con.tiercel.operationLog

def main():
    logs = clct_operationLog.find({'operationCode':{'$in':[30001,30005]}},{'operationCode':1,'msg':1})
    num_30001 = 0
    num_30005 = 0
    S = {}
    for log in logs:
        if log['operationCode'] == 30001:
            num_30001 +=1
            msg = json.loads(log['msg'])
            try:
                key = msg['errCode']+','+msg['errorMsg']
                print key
                if key not in S:
                    S[key] = 1
                else:
                    S[key] += 1
            except:
                print msg
        elif log['operationCode'] == 30005:
            num_30005 +=1

    print '解析错误',num_30005,'下载错误',num_30001
    print '下载错误详情：'
    for key in S:
        print key,':',S[key]

if __name__ == '__main__':
    main()