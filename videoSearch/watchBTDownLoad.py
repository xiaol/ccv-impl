#coding=utf-8
from setting import clct_preresource,clct_resource,clct_channel,MLDONKEY_DIR,STORE_DIR,MLDONKEY_D_DIR
import time,os,shutil,re
from common.common import r_mkdir,getCurTime

p_videoFile = re.compile('\.mp4$|\.rmvb$|\.flv*|\.mkv$|\.avi$')

def flagDownloadDone(pretask):
    print pretask
    #计算新,老 文件名
    if pretask['downloadType'] == 'torrent':
        '''bt任务'''
        filename = pretask['transcodeOutputname']
        if os.path.exists( os.path.join(MLDONKEY_DIR, pretask['videoId']) ):
            #单个文件
            oldfilename  = os.path.join(MLDONKEY_DIR, pretask['videoId'])
            
        elif os.path.exists(os.path.join(MLDONKEY_D_DIR, pretask['videoId'])):
            #目录
            for root,dirs,files in os.walk(os.path.join(MLDONKEY_D_DIR, pretask['videoId'])):
                for filespath in files:
                    file =  os.path.join(root,filespath)
                    if p_videoFile.search(file):
                        oldfilename = file
                        break
    else:
        '''ed2k'''
        filename = pretask['transcodeOutputname'] if pretask['transcodeOutputname'] else pretask['videoId']
        oldfilename = os.path.join(MLDONKEY_DIR, pretask['videoId'])
    
    
    #创建目标文件夹,更新videoId
    outputFolder = os.path.join(STORE_DIR,str(pretask['channelId']))
    r_mkdir(outputFolder)
    newfilename = os.path.join(outputFolder , filename)
    pretask['videoId'] = str(pretask['channelId']) +'/'+ filename
    
    #转码 / 移动文件
    if pretask['transcodeCoderate'] and pretask['transcodeFramerate'] and pretask['transcodeDimension']:
        codeRate  = pretask['transcodeCoderate']
        frameRate = pretask['transcodeFramerate']
        dimension = pretask['transcodeDimension']
        cmd = 'ffmpeg -i %s -target mp4 -b %s -minrate %s -maxrate %S -r %s -s %s %s'%\
                        (oldfilename,codeRate,codeRate,codeRate,frameRate,dimension,newfilename)
        print cmd
        os.sys(cmd)
    else:
        shutil.copy(oldfilename, newfilename)
    #文件尺寸
    pretask['resourceSize'] = os.path.getsize(newfilename)
    
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