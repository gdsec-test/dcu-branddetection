import os
import logging.config
import yaml
import time

from flask import Flask, request, jsonify
from settings import config_by_name

from branddetection.rediscache import RedisCache
from branddetection.branddetector import BrandDetector, BrandDetectorDecorator

path = 'logging.yml'
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
config = config_by_name[env]()
redis = RedisCache(config)

app = Flask(__name__)

t = time.time()
brand_detector = BrandDetector()
decorator = BrandDetectorDecorator(brand_detector, redis)
logging.info("Initialization took: {} seconds".format(time.time() - t))


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


@app.route('/health', methods=['GET'])
def health():
    return '', 200

if __name__ == '__main__':
    app.run()
