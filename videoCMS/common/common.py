#coding=utf-8
import time
import md5
import os
'''
def myLocaltime(sec=None):
    if sec != None:
        ret = time.gmtime(sec)
    else:
        ret = time.gmtime()
    days = [31,28,31,30,31,30,31,31,30,31,30,31]
    if (ret.tm_year%4==0 and ret.tm_year%100!=0) or ret.tm_year%400 == 0:
        days[1] = 29
    tl = list(ret)
    tl[3] += 8
    if tl[3] > 23:
        tl[2] += 1
        tl[3] -= 24
        if tl[2]>days[tl[1]-1]:
            tl[1] += 1
            tl[2] = 1
            if tl[1] > 12:
                tl[0] += 1
                tl[1] = 1
    print 'myLocaltime:',time.struct_time(tl)
    return time.struct_time(tl)
'''

def getCurTime(offset=0):
    return time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()+offset))



def getCurDate(offset=0):
    return time.strftime("%Y%m%d",time.localtime(time.time()+offset))

def Obj2Str(dic):
    dic['id'] = str(dic['_id'])
    dic.pop('_id')
    return dic

def formatHumanTime(s):
    try:
        return time.strftime("%Y/%m/%d %H:%M:%S",time.strptime(s,"%Y%m%d%H%M%S"))
    except:
        return s

def antiFormatHumanTime(s):
    return s.replace('/','').replace(':','').replace(' ','')
    

def validateTimeStr(s):
    try:
        time.strptime(s,"%Y%m%d%H%M%S")
        return True
    except:
        return False