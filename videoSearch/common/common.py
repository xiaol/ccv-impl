from pymongo import Connection
import time,os


db_connection = Connection('60.28.29.49:20010')
clct_downList = db_connection.iDown.downList


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
    return time.struct_time(tl)

def getCurTime():
    return time.strftime("%Y%m%d%H%M%S",myLocaltime())

def formatHumanTime(s):
    try:
        return time.strftime("%Y-%m-%d %H:%M:%S",time.strptime(s,"%Y%m%d%H%M%S"))
    except:
        return '00000-00-00 00:00:00'

def r_mkdir(dir):
    print '---- mkdir ',dir,'----'
    dirs = dir.split('/')
    root = ''
    for dir in dirs[1:]:
        root += '/'+dir
        print root
        if not os.path.exists(root):
            os.mkdir(root)