__author__ = 'ding'

from pymongo import Connection
import time,json

con = Connection('h39:20010')
clct_operationLog = con.tiercel.operationLog

def main():
    logs = clct_operationLog.find({'operationCode':{'$in':[30001,30005]}},{'operationCode':1,'msg':1})
    num_30001 = 0
    num_30005 = 0
    for log in logs:
        if log['operationCode'] == 30001:
            num_30001 +=1
            msg = json.loads(log['msg'])
            try:
                print msg['errCode'],',',msg['errorMsg']
            except:
                print msg
        elif log['operationCode'] == 30005:
            num_30005 +=1

if __name__ == '__main__':
    main()