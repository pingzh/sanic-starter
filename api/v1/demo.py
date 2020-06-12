import logging
from sanic.response import json as json_response, empty

logger = logging.getLogger(__name__)

def setup_routes(app, blueprint):

    @blueprint.route('/demo')
    async def get_demo(request):
        args = request.args
        logger.info('this is args %s', args)

        return json_response(args)

    @blueprint.route('/demo', methods={'POST', 'PUT'})
    async def update_demo(request):
        payload = request.json
        logger.info('this is payload %s', payload)
        return json_response(payload)

