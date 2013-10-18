#code=utf-8

from setting import clct_userWeibo, clct_userRecommend

def meanOfVideosPerWeiboUser():
    users = clct_userWeibo.distinct('sinaId')
    count = len(users)
    total = clct_userWeibo.count()
    mean = total/count
    print mean


def displayRate():
    pass

if __name__ == '__main__':
    meanOfVideosPerWeiboUser()