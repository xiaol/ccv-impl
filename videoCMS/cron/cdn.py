import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))]

from videoCMS.conf import clct_resource, clct_channel
from videoCMS.common.anquanbao import PrefetchCache,GetProgress

def main():
    channels = [ one["channelId"] for one in clct_channel.find({"videoClass":0},{"channelId":1})]
    print(channels)
    for one  in clct_resource.find({"channelId":{"$in":channels}}):
        #print PrefetchCache('/'+one["videoId"])
        print GetProgress('/'+one["videoId"])



if __name__ == '__main__':
    main()
