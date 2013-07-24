#coding=utf-8
import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from common.HttpUtil import get_html

print get_html('http://sports.sina.com.cn/video/g/pl/#104750832','gbk')