__author__ = 'ding'


def Cache(cacheKey,time):
    def _cache(func):
        def _func(request):
            return func(request)
        return _func
    return _cache
