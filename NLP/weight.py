#-*- coding: utf-8 -*-

import sys
sys.path.append('..')
from SnakeFlow import header as hd
import csv
import re

def compliancejin(m,_):
    try:
        if _[_.index(m) + len(m)] == u'斤':
            return True
        else:
            int('a')
    except:
        try:
            if _[_.rindex(m) + len(m)] == u'斤':
                return True
        except:
            return False

def compliancekg(m,_):
    try:
        if _[_.index(m) + len(m)] == u'k' and _[_.index(m) + len(m) + 1] == u'g':
            return True
        else:
            int('a')
    except:
        try:
            if _[_.rindex(m) + len(m)] == u'k' and _[_.rindex(m) + len(m) + 1] == u'g':
                return True
        except:
            return False


def themax(alist):
    max = '0'
    if alist != []:
        for x in alist:
            if float(x) > float(max):
                max = x
        return max

def list1function(list1):
    onetoten = False
    overhundred = False
    for x in list1:
        if float(x) >= 100:
            overhundred = True
        if float(x) >= 1 and float(x) <= 10:
            onetoten = True
    return onetoten and overhundred

def guess(_,minvalue = 0,maxvalue = 20,returnnum = 'jin'):
    #Result is in "Jin"
    _ = _.decode('utf-8').lower()
    list1 = re.findall(r"\d+\.?\d*",_)
    list2 = []
    for x in list1:
        if float(x) <= maxvalue and float(x) >= minvalue:# and float(x) >= 1:
            list2.append(x)

    if '000' in list2:
        list2.remove('000')

    while list2 != []:
        m = str(themax(list2))
        if _.index(m) + len(m) + 1 < len(_) or _.rindex(m) + len(m) + 1 < len(_):
            if compliancekg(m,_):
                return str(float(m)*2)
            else:
                if _.index(m)+len(m)<len(_) or _.rindex(m)+len(m)<len(_):
                    if compliancejin(m,_):
                        return m
                    else:
                        list2.remove(m)
                else:
                    list2.remove(m)
        elif _.index(m)+len(m)<len(_) or _.rindex(m)+len(m)<len(_):
            if compliancejin(m,_):
                return m
            else:
                list2.remove(m)
        else:
            list2.remove(m)

    if list2 == [] and not list1function(list1):
        return 0
    else:
        return None

def lastpoint(path,filename):
    try:
        with open(path+filename,'rb') as r:
            d = csv.reader(r)
            for row in d:
                pass
            try:
                return row[0]
            except:
                return None
    except:
        return None