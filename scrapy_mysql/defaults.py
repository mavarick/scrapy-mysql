import redis


# For standalone use.
PIPELINE_KEY = '%(spider)s:items'

# default queue key
DEFAULT_QUEUE_KEY = "dq"

# scheduler
SCHEDULER_QUEUE_CLASS = 'scrapy_mysql.queue.PriorityQueue'

# Sane connection defaults.
# or use `MYSQL_URL_REMOTE_PARAMS` in scrapy settings
# QUQUE: the remote url server will support multiple queue for multiple spider
MYSQL_REMOTE_PARAMS = {
    'SERVER': 'http://127.0.0.1:11011',
    'AUTH_CODE': 'auth_code',
    'QUEUE': DEFAULT_QUEUE_KEY,
}
