import os, datetime
import logging

logging.basicConfig()
log = logging.getLogger("queue")
log.setLevel(logging.DEBUG)

def get_object_age(date_value):
    delta = datetime.datetime.now() - date_value
    return delta.days * 86400 + delta.seconds            
 
def remove_outdated_files(path, min_age):
    log.debug("Removing outdated files from %s" % path)
    generator = os.walk(path)
    for dirpath, dirnames, filenames in generator:
        for f in filenames:
            resource = os.path.join(dirpath, f)
            resource_date = datetime.datetime.fromtimestamp(os.stat(resource).st_mtime)
            resource_age = get_object_age(resource_date)
            age = get_object_age(resource_date)
            if age > min_age:
                log.debug("%s age is %s. Applying filesystem remove." % (resource, age))
                os.remove(resource)
            
            
            