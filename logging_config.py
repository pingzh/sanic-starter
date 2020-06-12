import logging
import asyncio

LOG_CONTEXT_VAR = 'sanic_request_id_logging'
# REF: https://github.com/terrycain/sanic-json-logging
# AND: https://blog.sqreen.com/asyncio/
def _task_factory(loop, coro, context_var='context') -> asyncio.Task:
    """
    Task factory function
    Fuction closely mirrors the logic inside of
    asyncio.BaseEventLoop.create_task. Then if there is a current
    task and the current task has a context then share that context
    with the new task
    """
    task = asyncio.Task(coro, loop=loop)

    # Share context with new task if possible
    current_task = asyncio.Task.current_task(loop=loop)
    if current_task is not None and hasattr(current_task, context_var):
        setattr(task, context_var, getattr(current_task, context_var))

    return task

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        current_task = asyncio.Task.current_task()
        if current_task and hasattr(current_task, LOG_CONTEXT_VAR):
            record.request_id = getattr(current_task, LOG_CONTEXT_VAR).get('request_id', 'unknown')
        else:
            record.request_id = 'na'
        return True


LOG_SETTINGS = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'filters': ['requestid'],
        },
    },
    'filters': {
        'requestid': {
            '()': RequestIdFilter,
        },
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(process)d %(levelname)s %(request_id)s | %(message)s',
        },
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True
        },
    }
}
