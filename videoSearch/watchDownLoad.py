#coding=utf-8
from setting import clct_preresource,clct_resource,clct_channel,MLDONKEY_DIR,STORE_DIR
import time,os,shutil
from common.common import r_mkdir,getCurTime



def flagDownloadDone(pretask):
    print 'task done'
    filename = pretask['videoId']
    pretask['videoId'] = str(pretask['channelId']) +'/'+ pretask['videoId']
    print pretask
    #移动文件
    oldfilename = os.path.join(MLDONKEY_DIR,filename)
    newfilename = os.path.join(STORE_DIR,str(pretask['channelId']),filename)
    #os.rename(oldfilename, newfilename)
    r_mkdir(newfilename[:newfilename.rfind('/')])
    shutil.copy(oldfilename, newfilename)
    #文件尺寸
    pretask['resourceSize'] = os.path.getsize(oldfilename)
    
    #更新剧集
    channel = clct_channel.find_one({'channelId':pretask['channelId']},{'tvNumber':1})
    tvNumber = channel['tvNumber']
    if pretask['number'] > tvNumber:
        clct_channel.update({'channelId':pretask['channelId']},{'$set':{'tvNumber':pretask['number'],'subtitle':'已更新至：'+str(pretask['number']),'updateTime':getCurTime()}})
    
    #移动数据库
    clct_resource.insert(pretask)
    clct_preresource.remove({'_id':pretask['_id']})
    

def main():
    while True:
        downing  = clct_preresource.find()
        #print downing
        for task in downing:
            filename = os.path.join(MLDONKEY_DIR,task['videoId'])
            #print filename
            if not  os.path.exists(filename):
                continue
            print task['videoId'],'download done!'
            flagDownloadDone(task)
        time.sleep(60)
        


if __name__ == '__main__':
    main()