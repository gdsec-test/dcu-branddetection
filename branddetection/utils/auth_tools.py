import os

from dcustructuredloggingflask.flasklogger import get_logging
from flask import Response, request
from gd_auth.token import AuthToken

from settings import config_by_name

logger = get_logging()
env = os.getenv('sysenv', 'dev')
app_settings = config_by_name[env]()


def authenticate_jwt():
    jwt = request.headers.get('Authorization', '').strip()
    if jwt:
        logger.debug('JWT: {}'.format(jwt))
        if jwt.startswith('sso-jwt'):
            jwt = jwt[8:].strip()
        return validate_auth(jwt)
    else:
        return Response('No JWT provided. Unauthorized. Please verify your Authorization header \n', status=401)


def validate_auth(jwt):
    try:
        payload = AuthToken.payload(jwt)
        typ = payload.get('typ')
        parsed = AuthToken.parse(jwt, app_settings.SSO_URL, app="Brand Detection", typ=typ)
        if parsed.subject.get('cn', '') not in app_settings.CN_WHITELIST:
            logger.info('CN: {} is not whitelisted'.format(parsed.subject.get('cn')))
            return Response('Forbidden. Please verify your token \n', status=403)
    except Exception as e:
        logger.error('Authentication invalid with error: {}'.format(e.message))
        return Response('Authentication invalid. Please verify your token \n', status=403)
