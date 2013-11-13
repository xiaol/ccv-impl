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

                if key.startswith('VALUE_ERROR_DWONLOADING_ERROR,Download incomplete'):
                    key = 'VALUE_ERROR_DWONLOADING_ERROR,Download incomplete'
                elif key.startswith('RESPONSE_PARSER_ERROR'):
                    key = 'RESPONSE_PARSER_ERROR'
                elif key.startswith('GET_VIDEO_SIZE_ERROR'):
                    key = 'GET_VIDEO_SIZE_ERROR'
                elif key.startswith('failed,failedTraceback'):
                    key = 'failed,failedTraceback'
                elif key.startswith('VALUE_ERROR_DWONLOADING_ERROR,Connection to'):
                    key = 'VALUE_ERROR_DWONLOADING_ERROR,Connection to'
                elif key.startswith('VALUE_ERROR_DWONLOADING_ERROR,Unable to resolve host'):
                    key = 'VALUE_ERROR_DWONLOADING_ERROR,Unable to resolve host'


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
    result = S.items()
    result.sort(key=lambda a:a[1],reverse=True)
    for one in result:
        print one[0],':',one[1],'%.1f%%'%(100.0*one[1]/(num_30005 + num_30001))


if __name__ == '__main__':
    main()