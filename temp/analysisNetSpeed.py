#coding=utf-8
__author__ = 'ding'

from pymongo import Connection
import time,json
from collections import defaultdict

con = Connection('h39:20010')
clct_operationLog = con.tiercel.operationLog
clct_netspeed = con.tiercel.netspeed


def save():
    i = 0
    for one in clct_operationLog.find({'operationCode':30014}):
        clct_netspeed.insert(one)
        i+=1
        print i

def main():
    logs = clct_netspeed.find({"netstatus": "WIFI"},{'msg':1})

    S = defaultdict(dict)
    for log in logs:
        msg = json.loads(log['msg'])
        parsertype =  msg['parsertype'] + msg.get('videoparsertype','')

        STEP = 5
        MAX_STEPS = 20
        speed = msg['speedroad'] // STEP


        if speed > MAX_STEPS:
            speed = MAX_STEPS
        if speed not in S[parsertype]:
            S[parsertype][speed] = 0
        S[parsertype][speed] += 1
    for parsertype in S:
        print '========== %s =========='%parsertype
        sum_num = sum(S[parsertype].values())
        for speed in S[parsertype]:
            if speed == 0:
                print "0 KB/S:\t%d\t%.2f%%"%(S[parsertype][speed],S[parsertype][speed]*100.0/sum_num)
            elif speed == MAX_STEPS:
                print "> %d KB/S:\t%d\t%.2f%%"%(speed*STEP,S[parsertype][speed],S[parsertype][speed]*100.0/sum_num)
            else:
                print "%d~%d KB/S:\t%d\t%.2f%%"%(speed*STEP,speed*STEP+STEP,S[parsertype][speed],S[parsertype][speed]*100.0/sum_num)


if __name__ == '__main__':
    #save()
    main()