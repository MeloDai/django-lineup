class Status(object):
    new = 0
    processing = 1
    done = 2
    exception = -1
    
    choices = (
        ( new, 'New' ),
        ( processing, 'Processing'),
        ( done, 'Done'),
        ( exception, 'Exception'),
    )

MEMCACHED_SERVER = '127.0.0.1:11211'
JOB_SERVER = '127.0.0.1:9400'
MAX_QUEUE_CAPACITY  = 2
RETRY_MIN_AGE   = 60 * 30
RETRY_PERIOD    = 60 * 5 
PROCESS_PERIOD  = 15
CLEANUP_PERIOD  = 60 * 60 * 8
CLEANUP_MIN_AGE = 60 * 60
REMOVE_PROJECT_MIN_AGE = 60 * 60 * 50
REMOVE_ARCHIVE_MIN_AGE = 60 * 60 * 48
REMOVE_THUMBS_MIN_AGE = 60 * 60 * 24
