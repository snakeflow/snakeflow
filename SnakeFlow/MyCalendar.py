#-*- coding: utf-8 -*-


import time
import datetime


def monday_ts_of_yearweek(yearweek):
    #year = yearweek[:4]
    #week = yearweek[4:]
    return time.mktime(time.strptime(yearweek + '-1','%Y%W-%w'))

class MyCalendar(object):
    def __init__(self, date = '', format = ''):
        self.inittype = type(date)
        if isinstance(date, str) and date != '':
            try:
                self.date = time.mktime(time.strptime(date,format))
            except:
                raise ValueError('Initial problem - date/format does not match.')
        elif isinstance(date, time.struct_time):
            self.date = time.mktime(date)
        elif isinstance(date, datetime.datetime):
            self.date = time.mktime(date.timetuple())
        elif isinstance(date, float) or isinstance(date, int):
            self.date = float(date)
        elif isinstance(date, MyCalendar):
            self.date = date.date
        else:
            self.date = 0

    def __str__(self):
        strr = ''
        strr += 'Initial type: %s\nTime stamp: %f' %(self.inittype,self.date)
        return strr

    def __get_month_days(self, months=1):
        dt = datetime.datetime.fromtimestamp(self.date)
        cm = dt.month
        cy = dt.year
        ts1 = time.mktime(time.strptime('/'.join(['1',str(cm),str(cy)]),'%d/%m/%Y'))
        cm += months
        while cm > 12:
            cm -= 12
            cy += 1
        return (time.mktime(time.strptime('/'.join(['1',str(cm),str(cy)]),'%d/%m/%Y')) - ts1)/86400

    def __get_year_days(self, years=1):
        dt = datetime.datetime.fromtimestamp(self.date)
        ts1 = time.mktime(time.strptime('/'.join([str(dt.day),str(dt.month),str(dt.year)]),'%d/%m/%Y'))
        ts2 = time.mktime(time.strptime('/'.join([str(dt.day),str(dt.month),str(dt.year + years)]),'%d/%m/%Y'))
        return (ts2 - ts1)/86400

    def delta_ts(self, days=0, weeks=0, months=0, years=0, replace = False):
        total_days = days + weeks * 7 + self.__get_month_days(months = months) + self.__get_year_days(years = years)
        if replace:
            self.date += total_days * 86400
            return self.date
        else:
            return self.date + total_days * 86400

    def next_day_ts(self):
        return self.delta_ts(days = 1)

    def next_week_ts(self):
        return self.delta_ts(weeks=1)

    def next_month_ts(self):
        return self.delta_ts(months=1)

    def next_year_ts(self):
        return self.delta_ts(years=1)

    def first_day_of_month(self):
        dt = datetime.datetime.fromtimestamp(self.date)
        return time.mktime(datetime.date(dt.year,dt.month,1).timetuple())

    def year(self):
        return datetime.datetime.fromtimestamp(self.date).year

    def month(self):
        return datetime.datetime.fromtimestamp(self.date).month

    def week(self):
        return datetime.datetime.fromtimestamp(self.date).isocalendar()[1]

    def yearweek(self):
        a = datetime.datetime.fromtimestamp(self.date).isocalendar()
        if len(str(a[1])) == 1:
            return '%s%d%s' %(str(a[0]),0,str(a[1]))
        else:
            return '%s%s' %(str(a[0]),str(a[1]))

    def day(self):
        return datetime.datetime.fromtimestamp(self.date).day

    def weekday(self, Monday = 1, Sunday = 7):
        return datetime.datetime.fromtimestamp(self.date).isocalendar()[2]

    def to_datetime(self):
        return datetime.datetime.fromtimestamp(self.date)

    def to_timetuple(self):
        return time.localtime(self.date)

    def to_timestamp(self):
        return self.date

    def to_str(self, format = '%d/%m/%Y'):
        return time.strftime(format, time.localtime(self.date))