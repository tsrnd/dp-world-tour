import magic, datetime

def detect_content_of_file(file):
    return magic.from_buffer(file.open().read(1024), mime=False)

def gen_file_name(filename):
    if filename == '':
        return None
    now = datetime.datetime.now()
    return '{:%Y%m%d%H%M%S}'.format(now) + '_' + filename

def get_storage_file_url(filename, bucket):
    return 'http://localhost:9000/' + bucket + '/' + filename
