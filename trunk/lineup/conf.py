class Status(object):
    """Stores Queue status definitions"""
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
# --------------------------------------------------------------
# Loop/Queue interval values are expressed in number of seconds.
# --------------------------------------------------------------

# Memcached server used (mostly) for debug log messages
MEMCACHED_SERVER = '127.0.0.1:11211'

# PP server, see: http://www.parallelpython.com
JOB_SERVER = '127.0.0.1:9400'

# Define queue capacity here. Capacity means maximum number of slots for jobs to be processed at once.
MAX_QUEUE_CAPACITY  = 2

# Default retry age for Queue objects. Could be overwritten for instances via Queue.retry_min_age.
# Make sure it covers your Job execution ETA, to avoid accidental retrying.
RETRY_MIN_AGE   = 60 * 30

# Reactor loop retry interval.
# The retry loop checks if Queue object has exceeded the Queue.retry_min_age value.
RETRY_PERIOD    = 60 * 5 

# Main reactor loop interval.
PROCESS_PERIOD  = 15

# Cleanup process interval.
CLEANUP_PERIOD  = 60 * 60 * 8

# Queue object with status == Status.done will be _deleted_ when its age exceeds the value below. 
CLEANUP_MIN_AGE = 60 * 60
