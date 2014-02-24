__author__ = 'ding'

from django import template
import time
register = template.Library()


def formatHumanTime(s):
    try:
        return time.strftime("%Y/%m/%d %H:%M:%S",time.strptime(s,"%Y%m%d%H%M%S"))
    except:
        return s

register.filter('formatHumanTime',formatHumanTime)
print dir(register)
print register.filters
print 'dddddddddddddddd'