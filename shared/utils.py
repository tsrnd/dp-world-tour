from datetime import datetime


class Constant(object):
    datebaseDateFormat = '%Y-%m-%d %H:%M:%S+00'


class Utils(object):

    @staticmethod
    def convertTime(time, dateFormat=Constant.datebaseDateFormat):
        return datetime.strptime(time, dateFormat).timestamp()
