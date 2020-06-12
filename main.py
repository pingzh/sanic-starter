import os
import sys
import time
import json
import logging
import asyncio
from databases import Database
from uuid import uuid4

from sanic import Blueprint, Sanic
from sanic.response import json as json_response
from sanic.exceptions import NotFound

from api.v1.demo import setup_routes as setup_v1_resource

from logging_config import _task_factory, LOG_SETTINGS, LOG_CONTEXT_VAR

# Auto inject request id to each asyncio task so that it is available in the logging, RequestIdFilter
# defined in the log_config.py
asyncio.get_event_loop().set_task_factory(lambda loop, coro: _task_factory(loop, coro, LOG_CONTEXT_VAR))

app = Sanic('demo', log_config=LOG_SETTINGS)

blueprint = Blueprint('api-v1', url_prefix='/api/v1')

app.config.from_pyfile('./sanic_config.py')

app.db = Database(app.config.DATABASE_URL)

logger = logging.getLogger(__name__)


@app.listener('before_server_start')
async def connect_to_db(*args, **kwargs):
    logger.info('DB connecting')
    await app.db.connect()
    logger.info('DB connected')


@app.listener('after_server_stop')
async def disconnect_from_db(*args, **kwargs):
    logger.info('DB disconnecting')
    await app.db.disconnect()
    logger.info('DB disconnected')


@app.middleware('request')
async def pre_request(request):
    start_time = time.time()
    # A case-insensitive dictionary that contains the request headers.
    if request.headers.get('X-Request-ID') is None:
        request_id = uuid4()
    else:
        request_id = request.headers['X-Request-ID']

    request.ctx.start_time = start_time

    current_task = asyncio.Task.current_task()
    if current_task:
        if hasattr(current_task, LOG_CONTEXT_VAR):
            if isinstance(getattr(current_task, LOG_CONTEXT_VAR), dict):  # Guard against different non-dict context objs
                getattr(current_task, LOG_CONTEXT_VAR)['request_id'] = request_id
        else:
            setattr(current_task, LOG_CONTEXT_VAR, {
                'request_id': request_id,
            })

@app.middleware('response')
async def post_response(request, response):
    if request.path.startswith('/api/'):
        performance_ms = round((time.time() - request.ctx.start_time) * 1000, 2)
        status_code = response.status

        ip = request.headers.get('X-Remote-Host')
        log_line = {
            'ip': ip,
            'api_client': request.headers.get('X-Api-Client'),
            'method': request.method,
            'path': request.path,
            'query_string': request.query_string,
            'status_code': status_code,
            'performance_ms': performance_ms,
            'response_body': response.body.decode(),
        }
        logger.info(json.dumps(log_line))


@app.route('/health')
async def health(request):
    return json_response('ok')

async def server_error_handler(request, exception):
    logger.exception(f'server_error_handler {exception}')
    if isinstance(exception, NotFound):
        return json_response({'error': str(exception)}, 404)

    return json_response({'error': 'Internal Server Error'}, 500)
app.error_handler.add(Exception, server_error_handler)

setup_v1_resource(app, blueprint)

app.blueprint(blueprint)

if __name__ == "__main__":
    workers = app.config.WORKERS
    port = app.config.PORT
    debug = app.config.DEBUG
    app.run(host="0.0.0.0", port=port, debug=debug, workers=workers, access_log=False)
