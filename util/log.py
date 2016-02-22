import sys
import datetime

def log(*args):
    #print('[LOG]', datetime.datetime.now(), ':\n', *args, file=sys.stderr)
    print(*args, file=sys.stderr)
    sys.stderr.flush()

