import os

from dcustructuredloggingflask.flasklogger import add_request_logging
from flask import Flask, jsonify, request

from branddetection.branddetector import BrandDetector, BrandDetectorDecorator
from branddetection.rediscache import RedisCache
from branddetection.utils.auth_tools import authenticate_jwt
from settings import config_by_name

env = os.getenv('sysenv', 'dev')
app_settings = config_by_name[env]()
redis = RedisCache(app_settings)

app = Flask(__name__)

brand_detector = BrandDetector(app_settings)
decorator = BrandDetectorDecorator(brand_detector, redis)


@app.before_request
def before_request():
    return authenticate_jwt()


@app.route('/hosting', methods=['GET'])
def get_hosting_info():
    domain = request.args.get('domain')
    hosting_information = decorator.get_hosting_info(domain)
    return jsonify(hosting_information)


@app.route('/registrar', methods=['GET'])
def get_registrar_info():
    domain = request.args.get('domain')
    registrar_information = decorator.get_registrar_info(domain)
    return jsonify(registrar_information)


add_request_logging(app, 'brand-detection', sso=app_settings.SSO_URL)

if __name__ == '__main__':
    app.run()
