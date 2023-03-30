import os

from csetutils.flask import instrument
from flask import Flask, jsonify, request

from branddetection.branddetector import BrandDetector, BrandDetectorDecorator
from branddetection.rediscache import RedisCache
from branddetection.utils.auth_tools import authenticate_jwt
from settings import config_by_name
from html import escape

env = os.getenv('sysenv', 'dev')
app_settings = config_by_name[env]()
redis = RedisCache(app_settings)

app = Flask(__name__)


brand_detector = BrandDetector(app_settings)
decorator = BrandDetectorDecorator(brand_detector, redis)

instrument(app, service_name='brand-detection', sso=app_settings.SSO_URL, env=env)


@app.before_request
def before_request():
    return authenticate_jwt()


@app.route('/hosting', methods=['GET'])
def get_hosting_info():
    domain = escape(request.args.get('domain'))
    hosting_information = decorator.get_hosting_info(domain)
    return jsonify(hosting_information)


@app.route('/registrar', methods=['GET'])
def get_registrar_info():
    domain = escape(request.args.get('domain'))
    registrar_information = decorator.get_registrar_info(domain)
    return jsonify(registrar_information)


@app.route('/email', methods=['GET'])
def get_plid_email():
    plid = escape(request.args.get('plid'))
    return jsonify(brand_detector.get_plid_email(plid))


if __name__ == '__main__':
    app.run()
