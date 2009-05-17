import os, datetime, logging, pp, traceback
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from lineup.models import Queue
from lineup.conf import *
from lineup import registry, get_object_age
from django.conf import settings
from django.core.cache import cache
logging.basicConfig()
log = logging.getLogger("queue")
log.setLevel(logging.DEBUG)

job_server = pp.Server(1, ( JOB_SERVER ,))
# log_server = memcache.Client( [ MEMCACHED_SERVER ] )

queue_capacity = 0

def request_processed(queue_id, queue):
    """Method called when queued job has finished processing.
    Decreases the queue capacity and set either Status.done on success or
    Status.exception on failure.
    """
    global queue_capacity
    log.debug('Request processing finished: %s' % queue_id)    
    queue_capacity -= 1        

    if queue:
        log.debug(queue.job)    
        log.debug(queue)
        log.debug('Data recieved.')
        queue.set_status(Status.done)        
    else:
        err = 'Something went wrong with request %s - no data recieved from process_request!' % queue_id
        queue.set_status(Status.exception, err = err)
        log.warn(err)
    
def process_request(id, queue):
    """Executes queued job"""  
    from lineup import registry
    from lineup.conf import Status
    import traceback
         
    job = registry.get_job(queue.job)
    
    try:        
        job.execute(id, queue)
        return queue
    except:
        exc = traceback.format_exc()
        queue.set_status(Status.exception, exc)
        raise
            
def process_queued_requests():
    """Submits queued jobs to the job server if possible."""
    global queue_capacity        
    log.debug('Current queue capacity: %s/%s' % (queue_capacity, MAX_QUEUE_CAPACITY))

    if queue_capacity < MAX_QUEUE_CAPACITY:
        log.debug('Looking for new queue items to process.')
        queued_requests = Queue.objects.all().filter(status=Status.new).select_related()
        
        if queued_requests:

            queue = queued_requests[0]
            
            log.debug('-' * 50)
            log.debug('Handling request %s' % queue)        
            log.debug('-' * 50)
            
            queue_capacity += 1
            
            job = registry.get_job(queue.job)
            args = (
                queue.id,
                queue,
            )
            log.debug('Submitting request to job server (%s)' % job)
            job_server.submit( process_request, args, callback=request_processed, callbackargs=(queue.id,) )
        else:
            log.info("No queued jobs.")        

def collect_job_debug():
    """Memcached debug log reader"""
    try:
        messages = cache.get("job_debug", None)  
        if messages:
            for message in messages:
                log.info(message)
            cache.delete('job_debug')                  
    except:
        print '@ exc'
        exc = traceback.format_exc()
        log.error(exc)
                
def retry_failed_requests():
    """Retries requests that have failed or are processed too long."""
    log.debug("Looking for failed or processed too long.")
    requests = Queue.objects.all().filter(status__in=[Status.processing, Status.exception])
    if requests:
        for queue in requests:
            seconds = get_object_age(queue.date_accessed)
            if seconds > queue.retry_min_age:
                log.debug("Request %s age is %s seconds. Retrying." % (queue.id, seconds))
                queue.set_status(Status.new)
    else:
        log.debug("Nothing found. Next retry check in %s seconds." % RETRY_PERIOD)

def cleanup():
    """Deletes finished queue items."""
    log.debug("Cleanup check.")
    # find finished queue items, remove if old enough
    requests = Queue.objects.all().filter(status=Status.done)
    if requests:
        for queue in requests:
            seconds = get_object_age(queue.date_accessed)
            if seconds > CLEANUP_MIN_AGE:
                log.debug("Request %s age is %s seconds. Cleaning up." % (queue.id, seconds))
                queue.delete()
    else:        
        log.debug("Nothing found. Next cleanup check in %s seconds." % CLEANUP_PERIOD)        
            
def run():    
    reactor.run()
     
reactor.callWhenRunning(LoopingCall(process_queued_requests).start, PROCESS_PERIOD)
reactor.callWhenRunning(LoopingCall(retry_failed_requests).start, RETRY_PERIOD)
reactor.callWhenRunning(LoopingCall(cleanup).start, CLEANUP_PERIOD)
reactor.callWhenRunning(LoopingCall(collect_job_debug).start, 0.5)

if __name__ == '__main__':
    run()