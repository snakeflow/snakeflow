#-*-  coding: utf-8 -*-

import csv

def theheader(path,filename):
    try:
        with open(path+filename, 'rb') as r:
            d = csv.reader(r)
            row = next(d)
    except:
        raise IOError('No such path/file')
    i = 0
    returndict = dict()
    for it in row:
        returndict[it.replace('\xef\xbb\xbf','')] = i
        i += 1
    return returndict

def printme(theheader,name = 'theheader'):
    print '============%s============' %name
    for it in sorted(theheader.items(), key = lambda x : x[1]):
        print '%s : %d' %(it[0],it[1])
    print '============%s============' %name