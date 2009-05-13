from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import force_unicode
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from lineup.conf import *
from lineup import registry
import datetime

class Queue(models.Model):
    """`Queue` model stores information about queued jobs and their properties.
    
    The common case is, you would like to relate a `Queue` object to any other model object
    in your application. Use `context_object` generic value for this purpose.
    
    `err` field is automatically filled with exception(s) traceback history if any 
    occured during the job execution.
    
    `Queue` objects use `QueueParam`(s) as optional & additional, user-defined
    information for the queue object.
    
    Queues should be created either via admin interface or `lineup.factory` module.
    """
    date_created = models.DateTimeField(auto_now_add = True, blank=True)
    date_accessed = models.DateTimeField(auto_now = True, blank=True)
    status = models.IntegerField(blank=False, null=False, default=0, choices=Status.choices)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    context_object = generic.GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User)
    job = models.CharField(blank=False, max_length=255, choices=registry.registered_jobs)
    retry_min_age = models.PositiveIntegerField(blank=True, null=True, default=RETRY_MIN_AGE)
    err = models.TextField(blank=True, null=True)
    
    def __init__(self, *args, **kwargs):
        super(Queue, self).__init__(*args, **kwargs)
        self.params = self.queueparam_set.all()

    def delete(self):
        self.queueparam_set.all().delete()
        super(Queue, self).delete()
        
    def get_param(self, param_name):
        if self.params:
            for param in self.params:                
                if param.param_name == param_name:
                    return force_unicode(param)
                    
    def set_status(self, status, err = None):
        self.status = status
        if err:
            errors = "[%s] %s \n %s \n" % (datetime.datetime.today(), err, self.err)        
            self.err = errors
        self.save()
                                                        
    def __unicode__(self):
        return "[%s] %s request for %s (by %s)" % (self.status, self.job, self.context_object, self.user)

class QueueParam(models.Model):
    """QueueParam purpose is to store additional information about Queue objects.
    `param_value` has higher priority than `param_value_long`, so you should make sure 
    you use only one of them.
    
    Example usage: e-mail text content for queued e-mail sending job.
    """
    queue = models.ForeignKey(Queue)
    param_name = models.CharField(blank=False, max_length=100)
    param_value = models.CharField(blank=True, null=True, max_length=255)
    param_value_long = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return self.param_value or self.param_value_long
            

