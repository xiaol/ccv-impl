#coding=utf-8
#2013-10-31
__author__ = 'ding'
import threading


class ThreadPool():
    def __init__(self,size):
        self.size = size
        self.curSize = 0
        self.curSizeLock = threading.Lock()
        self.full = threading.Semaphore(0)
        self.empty = threading.Semaphore(size)

    def _curSizeChange(self,num):
        self.curSizeLock.acquire()
        self.curSize += num
        self.curSizeLock.release()

    def _proc(self,target,params,kwargs):
        target(*params,**kwargs)
        self._curSizeChange(-1)
        self.empty.release()


    def do(self,target,*params,**kwargs):
        self.empty.acquire()
        self._curSizeChange(+1)
        t = threading.Thread(target=self._proc,args=(target,params,kwargs))
        t.start()



    def join(self):
        while self.empty.acquire():
            print 'wait all tasks done... curSize:',self.curSize
            if self.curSize == 0:
                return




def proc(i):
    import time
    print 'start',i
    time.sleep(3)
    print 'end',i

def test():

    tp = ThreadPool(5)
    for i in xrange(10):
        tp.do(proc,i)
    tp.join()


if __name__ == '__main__':
    test()