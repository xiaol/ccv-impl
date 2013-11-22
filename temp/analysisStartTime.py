#coding=utf-8
__author__ = 'ding'

import csv


lines = open('/Users/ding/Downloads/口袋视频_小时_启动次数_20131113_20131119.csv','rb').readlines()

map = {}
sum = 0

for line in lines:
    date,num,_ = line.strip().split('\t')
    #print date,num
    time = date.split()[-1]
    #print num,len(num),type(num)
    if time not in map:
        map[time]= 0
    map[time] += int(num)
    sum += int(num)

items = map.items()
items.sort(key=lambda a:int(a[0].split(':')[0]))

for item in items:
    print item[0],item[1], '%.2f%%'%(100.0*item[1]/sum)