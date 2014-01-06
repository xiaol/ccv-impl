#coding=utf-8
__author__ = 'ding'
import sys,os


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path += [ROOT_DIR]

from common.sendMail import send_mail,server
import time


def main():
    t = os.path.getmtime(ROOT_DIR + '/main.log')
    lastModifySpan  = (time.time() - t)/3600
    if lastModifySpan > 3:
        content = '日志%.2f小时无输出，日志上次输出时间为：%s'%(lastModifySpan,time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(t)))
        print content
        send_mail(server,server['user'],['dingyaguang117@126.com'],'视频搜索服务down了',content)

if __name__ == '__main__':
    main()