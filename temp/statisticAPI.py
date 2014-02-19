__author__ = 'ding'

import os,json,re
import collections


def getResource():
    labels = ['%02d'%one for one in xrange(24)]
    print json.dumps(labels)
    result = {}
    data = os.popen('cat |grep getResource"|awk -F "," "{print $1;}"').readlines()

    for line in data:
        line = line.strip()
        hour = line.split()[1].split(':')[0]
        if hour not in result:
            result[hour] = 0
        result[hour] += 1
    s = []
    for hour in labels:
        s.append(result.get(hour,0))
    print json.dumps(s)


def getResourceDeep():
    data = os.popen('''cat  /usr/local/resin-3.1.12/log/jvm-default.log.20140218.*|grep 'getResource"' ''').readlines()
    p = re.compile('"start":"(.*?)".*?"uuid":"(.*?)"')
    s = collections.defaultdict(int)
    for line in data:
        try:
            start,uuid = p.search(line).groups()
        except:
            continue
        page = int(start)/10 + 1
        #print uuid,page
        s[uuid] = max(s[uuid],page)
    ss = collections.defaultdict(int)
    for uuid in s:
        ss[s[uuid]] += 1

    _sum = 0
    for i in xrange(1,20):
        _sum += ss[i]

    for i in xrange(1,20):
        print ss[i], "%.2f%%" %(100.0 *ss[i] /_sum)

getResourceDeep()