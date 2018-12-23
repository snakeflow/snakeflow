#-*-  coding: utf-8 -*-


import csv
import header as hd
import random
import time


def random_pick(a,b):
    x=random.uniform(0,1)
    cumulative_p = 0.0
    for item, item_p in zip(a,b):
        cumulative_p += item_p
        if x<cumulative_p:break
    return item

def _path_file_check(path,filename=''):
    import os
    if not os.path.exists(path):
        raise ValueError('Path not exists.')
    if filename != '':
        if not os.path.isfile(path + filename):
            raise ValueError('File not exists.')
    return True

def int_in_tri_count(_):
    if isinstance(_, int) or isinstance(_, float):
        thelist = str(_).split('.')
        a = list(thelist[0])
        if len(thelist) > 1:
            b = '.' + str(_).split('.')[1]
        else:
            b = ''
        for i in range((len(a) - 1) / 3):
            a.insert(-4 * i - 3, ',')
        return ''.join(a) + b
    else:
        return False


class MyText(object):
    def __init__(self, _= False):
        self.content = []
        if _:
            if isinstance(_,MyText):
                self.content = _.content
            elif isinstance(_,list):
                for row in _:
                    self.content.append(row)

    def copy(self):
        newmt = MyText()
        newmt.content = self.content
        return newmt

    def __str__(self):
        strr = ''
        tr = self.total_row()
        if tr<=20:
            for row in self.content:
                if isinstance(row,list):
                    for c in row:
                        if isinstance(c, unicode):
                            strr += str(c.encode('utf-8')) + '\t'
                        elif isinstance(c, str):
                            strr += c + '\t'
                        else:
                            strr += str(c).encode('utf-8') + '\t'
                else:
                    strr += str(row) + '\n'
            strr += '\n'
            if len(self.content) > 0:
                strr += '[Row × Column = %s × %s]' %(int_in_tri_count(tr),int_in_tri_count(len(self.content[0])))
            else:
                strr += '[Row × Column = %d × %d]' %(0,0)
        else:
            count = 0
            for i in range(8):
                if isinstance(self.content[i],list):
                    for c in self.content[i]:
                        if isinstance(c, unicode):
                            strr += str(c.encode('utf-8')) + '\t'
                        elif isinstance(c,str):
                            strr += c + '\t'
                        else:
                            strr += str(c).encode('utf-8') + '\t'
                        count = len(self.content[i])
                    strr += '\n'
                else:
                    strr += str(self.content[i]) + '\n'
            for i in range(count):
                strr += '...\t'
            strr += '\n'
            for i in range(8,0,-1):
                if isinstance(self.content[i],list):
                    for c in self.content[tr-i]:
                        if isinstance(c, unicode):
                            strr += str(c.encode('utf-8')) + '\t'
                        elif isinstance(c,str):
                            strr += c + '\t'
                        else:
                            strr += str(c).encode('utf-8') + '\t'
                    strr += '\n'
                else:
                    strr += str(self.content[i]) + '\n'
            if len(self.content) > 0:
                strr += '[Row × Column = %s × %s]' %(int_in_tri_count(tr),int_in_tri_count(len(self.content[0])))
            else:
                strr += '[Row × Column = %d × %d]' %(0,0)
        return strr

    def total_row(self):
        return len(self.content)

    def insert_row(self,position,content):
        self.content.insert(position,content)
        return self

    def add_row(self, content):
        if isinstance(content,list):
            self.content.append(content)
        else:
            self.content.append([content])
        return self

    def to_csv(self,path,filename):
        import codecs
        if filename[-4:] != '.csv':
            filename += '.csv'
        with open(path+filename,'wb') as w:
            w.write(codecs.BOM_UTF8)
            writer = csv.writer(w)
            for row in self.content:
                agent = []
                if isinstance(row, list):
                    for c in row:
                        if isinstance(c, unicode):
                            agent.append(c.encode('utf-8'))
                        else:
                            agent.append(c)
                writer.writerow(agent)
        print '"%s%s" is been saved successfully.' %(path,filename)

    def head(self,row=20):
        if len(self.content) <= row:
            for r in self.content:
                if isinstance(r,list):
                    for c in r:
                        print c,'\t'
                    print
                else:
                    print r
        else:
            for i in range(int(row)):
                if isinstance(self.content[i],list):
                    for c in self.content[i]:
                        print c,
                    print
                else:
                    print self.content[i]
        return

    def combine(self,mt2,replace = False):
        if len(self.content) < len(mt2.content):
            return False
        if replace:
            for i in range(len(mt2.content)):
                if isinstance(self.content[i],list):
                    self.content[i].extend(mt2.content[i])
                else:
                    self.content[i] = [self.content[i]]
                    self.content[i].extend(mt2.content[i])
            return self
        else:
            newmt = MyText()
            mt2length = len(mt2.content)
            for i in range(len(self.content)):
                agent = []
                if isinstance(self.content[i],list):
                    agent.extend(self.content[i])
                else:
                    agent.append(self.content[i])
                if i <= mt2length:
                    if isinstance(mt2.content[i],list):
                        agent.extend(mt2.content[i])
                    else:
                        agent.append(mt2.content[i])
                newmt.add_row(agent)
            return newmt

class SnackFlow(object):
    def __init__(self, path = '', filename = ''):
        self.path = path
        self.filename = filename
        if filename != '':
            self.column = hd.theheader(path, filename)
        return

    def __get_iter(self):
        print '__get_iter'
        return

    def read_csv(self,path,filename):
        if path[-1:] != '\\':
            path += '\\'
        if _path_file_check(path,filename):
            self.path = path
            self.filename = filename
            self.column = hd.theheader(path, filename)
            hd.printme(self.column,str(path+filename))
            print
        return self

    def head(self,row = 30):
        with open(self.path+self.filename,'rb') as r:
            d = csv.reader(r)
            i = 0
            print
            for r in d:
                i += 1
                if i <= int(row) + 1:
                    for c in r:
                        print '%s\t' %c,
                    print
                else:
                    break
            print

    def map(self, func, cols, result_name = 'result', combine = True, skip_firstrow = True):
        if not [0 for y in [column in self.column for column in cols] if y is False] == []:
            raise ValueError('Input columns do not exist.')
        theheader = hd.theheader(self.path, self.filename)
        mt = MyText()
        with open(self.path+self.filename,'rb') as r:
            d = csv.reader(r)
            i = 0
            if skip_firstrow:
                fr = next(d)
                ag = []
                i = 1
                if combine:
                    for col in cols:
                        ag.append(fr[theheader[col]])
                    ag.append(result_name)
                    mt.add_row(ag)
                else:
                    mt.add_row([result_name])
            for row in d:
                agent = []
                for col in cols:
                    agent.append(row[theheader[col]])
                result = func(agent,i)
                if combine:
                    agent.append(result)
                    mt.add_row(agent)
                else:
                    mt.add_row([result])
                i += 1
        return mt

    def columns(self):
        import header as hd
        theheader = hd.theheader(self.path,self.filename)
        hd.printme(theheader,name = 'Columns')
        return theheader

    def describe(self):
        return

    def total_row(self):
        return

    def cross_analysis(self):
        return

    def select(self, columns):
        if [0 for y in [column in self.column for column in columns] if y is False] == []:
            with open(self.path+self.filename,'rb') as r:
                d = csv.reader(r)
                mt = MyText()
                for row in d:
                    therow = []
                    for column in columns:
                        therow.append(row[self.column[column]])
                    mt = mt.add_row(therow)
        else:
            raise ValueError('Input columns do not exist.')
        return mt

    def season(self,season_dict,geo_col,date_col,format = '%d/%m/%Y',skip_firstrow = True):
        #season_dict = {country1:{startdate:'',enddate:''},country2:{startdate:'',enddate:''},...}
        theheader = hd.theheader(self.path,self.filename)
        mt = MyText()
        with open(self.path+self.filename,'rb') as r:
            d = csv.reader(r)
            if skip_firstrow:
                first_row = next(d)
                mt.add_row([first_row[theheader[geo_col]].decode('utf-8'),first_row[theheader[date_col]],'season'])
            for row in d:
                country = row[theheader[geo_col]].decode('utf-8')
                date = row[theheader[date_col]]
                result = self.__match_season_country(season_dict,country,date,format)
                if result:
                    mt.add_row([country,date,1])
                else:
                    #1
                    mt.add_row([country,date,0])
        return mt

    def __judge_season(self,starttime,endtime,datestr,dateformat,dictformat='%Y-%m-%d',try_possible = False):
        possible_format = ['%Y-%m-%d','%d-%m-%Y','%Y/%m/%d','%d/%m/%Y']
        try:
            startts = time.mktime(time.strptime(starttime,dictformat))
            endts = time.mktime(time.strptime(endtime,dictformat))
            thets = time.mktime(time.strptime(datestr,dictformat))
        except:
            if try_possible:
                x = []
                for format in possible_format:
                    try:
                        startts = time.mktime(time.strptime(starttime, dictformat))
                        endts = time.mktime(time.strptime(endtime, dictformat))
                        thets = time.mktime(time.strptime(datestr, format))
                        x.append(format)
                    except:
                        continue
                if len(x) > 1:
                    print 'Multiple formatting fits: %s, %s' %(str(x),dateformat)
                    raise ValueError()
                elif len(x) == 0:
                    print 'No formatting fits: %s' %(dateformat)
                    raise ValueError()
        if thets >= startts and thets <= endts:
            return True
        else:
            return False

    def __match_season_country(self,season_dict,country,datestr,theformat):
        try:
            x = []
            for it in season_dict[country]:
                x.append(self.__judge_season(it['startdate'],it['enddate'],datestr,theformat,try_possible=True))
            if True in x:
                return True
            else:
                return False
        except:
            print '%s, %s, %s' %(country,datestr,theformat)
            #raise ValueError()

    def __str__(self):
        str = '=======Object: [SnakeFlow]=======\nFilepath: ['
        str += self.path + self.filename + ']\n'
        str += '=======Object: [SnakeFlow]=======\n'
        return str