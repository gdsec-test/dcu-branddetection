import logging.config
import os

import yaml
from flask import Flask, jsonify, request

from branddetection.branddetector import BrandDetector, BrandDetectorDecorator
from branddetection.rediscache import RedisCache
from settings import config_by_name

path = 'logging.yaml'
value = os.getenv('LOG_CFG', None)
if value:
    path = value
if os.path.exists(path):
    with open(path, 'rt') as f:
        lconfig = yaml.safe_load(f.read())
    logging.config.dictConfig(lconfig)
else:
    logging.basicConfig(level=logging.INFO)

env = os.getenv('sysenv') or 'dev'
app_settings = config_by_name[env]()
redis = RedisCache(app_settings)

app = Flask(__name__)

brand_detector = BrandDetector(app_settings)
decorator = BrandDetectorDecorator(brand_detector, redis)


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


if __name__ == '__main__':
    app.run()
