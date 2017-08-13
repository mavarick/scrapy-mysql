# defaults settings

# For standalone use.
PIPELINE_KEY = '%(spider)s:items'

# default queue key
DEFAULT_QUEUE_KEY = "dq"

# scheduler
SCHEDULER_QUEUE_CLASS = 'scrapy_mysql.queue.RemoteQueue'

# Sane connection defaults.
# or use `MYSQL_URL_REMOTE_PARAMS` in scrapy settings
# QUQUE: the remote url server will support multiple queue for multiple spider
MYSQL_REMOTE_PARAMS = {
    'SERVER': 'http://127.0.0.1:11011',
    'AUTH_CODE': 'auth_code',
    'QUEUE': DEFAULT_QUEUE_KEY,
}

SCHEDULER_FUNC_REQ_ID = "scrapy_mysql.utils.get_default_id"

# empty queue trying times
EMPTY_QUEUE_TRY_TIME = 1
EMPTY_QUEUE_SLEEP_TIME = 1