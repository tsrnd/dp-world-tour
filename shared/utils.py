from datetime import datetime
import magic

def datebaseDateFormat():
    return '%Y-%m-%d %H:%M:%S+00'


def convertTime(time, dateFormat=datebaseDateFormat()):
    return datetime.strptime(time, dateFormat).timestamp()

def detect_content_of_file(file):
    return magic.from_buffer(file.open().read(1024), mime=False)

def gen_file_name(filename):
    if filename == '':
        return None
    now = datetime.now()
    return '{:%Y%m%d%H%M%S}'.format(now) + '_' + filename
