# FIXIT

Quick-dirty-start
=================

Dependencies:
-------------
 
	twisted, pp, memcache, hashlib

Usage after syncdb & dependencies.
----------------------------------

1. Edit lineup.conf depending on your needs
2. Have your memcached server running
3. Define job and register it with optional callback (see exampleapp/jobs.py)

	from lineup import registry
	from lineup import _debug

	def do_something(queue_id, queue):
	    _debug('Doing something')

	def do_something_callback(queue_id, queue):
	    _debug('Running callback')

	registry.register_job('doso', do_something, callback = do_something_callback)

4. Import jobs in your app models module (see exampleapp/models.py)
5. ./manage.py run_queue to start the queue reactor. 
6. Create job instances either via admin or lineup.factory interface

Contact
-------
adam@mtod.org




