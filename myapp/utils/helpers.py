# coding: utf-8
import datetime


def get_time():
    '''返回上午/下午/晚上'''
    now = datetime.datetime.now()
    hour = int(now.strftime('%H'))
    if hour >= 6 and hour < 12:
        return u'上午'
    elif hour >= 12 and hour < 19:
        return u'下午'
    else:
        return u'晚上'

if __name__ == '__main__':
    print get_time()
