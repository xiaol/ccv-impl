#coding=utf-8
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

def strB2Q(ustring):
    """把字符串半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
            rstring += uchar
            continue
        if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
            inside_code=0x3000
        else:
            inside_code+=0xfee0
        rstring += unichr(inside_code)
    return rstring

def strQ2B(ustring):
    """把字符串全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code==0x3000:
            inside_code=0x0020
        else:
            inside_code-=0xfee0
        if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
            rstring += uchar
            continue
        rstring += unichr(inside_code)
    return rstring
