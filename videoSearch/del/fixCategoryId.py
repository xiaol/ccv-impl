from setting import clct_channel,clct_resource

for resource in clct_resource.find():
    try:
        categoryId = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
        print categoryId
        clct_resource.update({'_id':resource['_id']},{'$set':{'categoryId':categoryId}})
    except:
        pass
    #