"""Gunicorn *production* config file"""

import multiprocessing

# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "app.wsgi:application"
# The number of worker processes for handling requests
workers = multiprocessing.cpu_count() * 2 + 1
# The socket to bind
bind = "0.0.0.0:5000"
# Write access and error info to /var/log
accesslog = "config/gunicorn/access.log"
errorlog = "config/gunicorn/error.log"
# Redirect stdout/stderr to log file
capture_output = True
# PID file so you can easily fetch process ID
pidfile = "config/gunicorn/prod.pid"
# Daemonize the Gunicorn process (detach & enter background)
daemon = True
# The granularity of Error log outputs
loglevel = "debug"
