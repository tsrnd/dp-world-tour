from datetime import datetime
import magic


def currentTimestamp():
    """
    Get timeStamp at now
    """
    return datetime.now().timestamp()


def datePickerFormat():
    """
    '%Y-%m-%d %H:%M+00'
    """
    return '%Y-%m-%d %H:%M+00'


def convertStringToTimestamp(timeString, dateFormat=datePickerFormat()):
    return datetime.strptime(timeString, dateFormat).timestamp()


def convertTimestampToString(timestamp, dateFormat=datePickerFormat()):
    value = datetime.fromtimestamp(timestamp)
    return datetime.strftime(value, dateFormat)


def detect_content_of_file(file):
    return magic.from_buffer(file.open().read(1024), mime=False)


def gen_file_name(filename):
    if filename == '':
        return None
    now = datetime.now()
    return '{:%Y%m%d%H%M%S}'.format(now) + '_' + filename
