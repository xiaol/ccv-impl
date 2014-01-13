#coding=utf-8
__author__ = 'ding'
import urllib2

cities = "01|北京,02|上海,03|天津,04|重庆,05|黑龙江,06|吉林,07|辽宁,08|内蒙古,09|河北,10|山西,11|陕西,12|山东,13|新疆,14|西藏,15|青海,16|甘肃,17|宁夏,18|河南,19|江苏,20|湖北,21|浙江,22|安徽,23|福建,24|江西,25|湖南,26|贵州,27|四川,28|广东,29|云南,30|广西,31|海南,32|香港,33|澳门,34|台湾"


D = {}
for province in cities.split(','):
    code,province = province.split('|')
    print code,province

    url = 'http://www.weather.com.cn/data/list3/city%s.xml'%code
    data = urllib2.urlopen(url).read().decode()
    for city in data.split(','):
        code2,city = city.split('|')
        print '  ',code2,city
        url = 'http://www.weather.com.cn/data/list3/city%s01.xml'%code2
        _,code3 = urllib2.urlopen(url).read().decode().split('|')
        D[city] = code3

with open('city.json','w') as f:
    import json
    f.write(json.dumps(D))