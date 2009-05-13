from lineup import registry
from lineup import _debug

def do_something(queue_id, queue):
    _debug('Doing something')

def do_something_callback(queue_id, queue):
    _debug('Running callback')
    
def dummy(queue_id, queue):
    _debug('Dummy says hello')
    
def say_yo(queue_id, queue):
    _debug('Dummy callback says ouch')

registry.register_job('doso', do_something, callback = do_something_callback)
registry.register_job('dummy', dummy, callback = say_yo)