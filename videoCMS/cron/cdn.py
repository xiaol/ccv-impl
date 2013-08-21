import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.dirname(__file__)))]


from videoCMS.conf import clct_resource
from videoCMS.common.anquanbao import PrefetchCache,GetProgress

def main():
    
    GetProgress()



if __name__ == '__main__':
    main()