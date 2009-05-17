VERSION = (0, 1, 'pre')
__all__ = ['registry',]

from django.core.cache import cache
from lineup.conf import *
import datetime

class Job(object):
    """Basic abstraction layer for a single queue task."""
    def __init__(self, name, func, callback = False):
        super(Job, self).__init__()
        self.name = name
        self.func = func
        self.callback = callback
        
    def execute(self, id, request):
        """Executes queued job and callback function if provided."""
        _debug('*' * 50)
        _debug("Excecuting %s %s %s" % (self, id, request) )
        request.set_status(1)
        self.func(id, request)        
        if self.callback:
            _debug("Callback run.")
            self.callback(id, request)
        else:
            _debug('No callback.')
        _debug('*' * 50)
     
    def __str__(self):
        return self.name
     
    def __unicode__(self):
        return self.name

class Registry(object):
    """Provides interface for queue jobs registration (storage)/
    management across django project."""
    def __init__(self):
        super(Registry, self).__init__()
        self.registry = []
        
    def register_job(self, name, func, callback=False):
        """Stores Job object within registry."""
        job = Job(name, func, callback)
        self.registry.append(job)
        cache.set('job_registry', self.registry)
        
    def _get_registered_jobs_tuple(self):
        """Internal jobs tuple generator. Should be accessed via
        registered_jobs property."""
        _registry = cache.get('job_registry', None)
        if _registry:
            print 'Got registry from cache! yay', _registry
        else:
            _registry = self.registry
        jobs = []
        for job in _registry:
            jobs.append( (job.name, job.func) )

        for job in jobs:
            yield job    
            
    registered_jobs = property(_get_registered_jobs_tuple)
    
    def get_job(self, strid, prop = 'name'):
        """ Retrieves Job object from registry by attribute (e.g. name/func/callback) """
        for job in self.registry:
            if getattr(job, prop) == strid:
                return job
        return None

registry = Registry()        

# log_server = memcache.Client( [ MEMCACHED_SERVER ] )

def _debug(msg):  
    """Stores debugging message in the memcached log server"""
    messages = cache.get('job_debug')  
    if not messages:
        messages = []
    messages.append('[JOB] %s' % msg)    
    cache.set('job_debug', messages)
    return True

def get_object_age(date_value):
    """Generic method returning time delta for given date (in seconds)"""
    delta = datetime.datetime.now() - date_value
    return delta.days * 86400 + delta.seconds

# def remove_outdated_files(path, min_age):
#     log.debug("Removing outdated files from %s" % path)
#     generator = os.walk(path)
#     for dirpath, dirnames, filenames in generator:
#         for f in filenames:
#             resource = os.path.join(dirpath, f)
#             resource_date = datetime.datetime.fromtimestamp(os.stat(resource).st_mtime)
#             resource_age = get_object_age(resource_date)
#             age = get_object_age(resource_date)
#             if age > min_age:
#                 log.debug("%s age is %s. Applying filesystem remove." % (resource, age))
#                 os.remove(resource)