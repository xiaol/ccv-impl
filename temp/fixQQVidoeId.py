__author__ = 'ding'

from pymongo import Connection
import re

con = Connection('h37:20010')
clct_resource = con.tiercel.resource




data =clct_resource.find({'videoType':'qq','resourceUrl':{'$regex':'vid='}},{'resourceUrl':1,'videoId':1})

n = 0
p = re.compile('\?vid=([^&]+)')
for one in data:
    vid =  p.search(one['resourceUrl']).groups()[0]
    if vid != one['videoId']:
        n += 1
        print vid,one['videoId']
        #print 'find',clct_resource.find_one({'_id':one['_id']})
        try:
            print clct_resource.update({'_id':one['_id']},{'$set':{'videoId':vid}},w=1)
        except:
            clct_resource.remove({'_id':one['_id']})


print data.count()
print n