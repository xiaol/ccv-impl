__author__ = 'ding'

from pymongo import Connection

con = Connection('h37:20010')
clct_operationLog = con.tiercel.operationLog

