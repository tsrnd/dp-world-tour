from datetime import datetime


def datebaseDateFormat():
    return '%Y-%m-%d %H:%M:%S+00'


def convertTime(time, dateFormat=datebaseDateFormat()):
    return datetime.strptime(time, dateFormat).timestamp()
