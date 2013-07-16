import os

def SingletonProcessDecoration(filename):
    def _deco(func):
        def __deco(*args, **kwargs):
            if os.path.exists(filename):
                print 'lockfile %s exists..program exit...'%filename
                return
            open(filename,'w').close()
            ret = func(*args, **kwargs)
            os.remove(filename)
            return ret
        return __deco
    return _deco


def SingletonFunction(func, filename):
    @SingletonProcessDecoration(filename)
    def _d(*args, **kwargs):
        return func(*args, **kwargs)
    return _d

@SingletonProcessDecoration('1.lock')
def main():
    import time
    time.sleep(3)
    return True

def f(a):
    import time
    for i in xrange(5):
        print a
        time.sleep(1)

def main2():
    #SingletonFunction(f,'1.lock')('aa')
    SingletonProcessDecoration('1.lock')(f)('aa')

if __name__ == '__main__':
    print main2()