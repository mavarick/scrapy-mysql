# scrapy_mysql

  Use django+mysql as url server to push and pop url request, mainly changes are:
    
    1. add request id, set settings "SCHEDULER_FUNC_REQ_ID" to custom your self funciton (request, spider)
    2. use 'SpierUrlApi.py' to connect to remote server. The remote server will record every handlerd url. Use `status` to tag url crawling status. So use this api in `errback` to change url status in remote server
    3. use mysql deduplicating funciton by unique key. 
    4. Cause url are serialized, so increasing scrawling and distributing scrawling are supported

## Castrated Functions
  
  some functions are CASTRATED:
  
    1. Queue. Only one queue now is supported with one remote server. Of cause, you could set multiple remote server for multi spiders
    2. speed. the speed maybe much slower, cause network data transfering.
     
## Future work

  1. errback.
  2. mutilple queue in one server
  3. better way, other than django+mysql, to support functions above.
