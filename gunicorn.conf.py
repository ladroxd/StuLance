import multiprocessing

# Gevent async workers — handle thousands of concurrent SSE/long-lived connections
worker_class = "gevent"
workers = multiprocessing.cpu_count() * 2 + 1
worker_connections = 1000

bind = "0.0.0.0:8000"
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
