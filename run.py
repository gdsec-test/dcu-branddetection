import os
import logging.config
import yaml
import time

from branddetection.branddetector import BrandDetector
from flask import Flask, request, jsonify
from settings import config_by_name

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

app = Flask(__name__)

t = time.time()
brand_detector = BrandDetector(config)
logging.info("Initialization took: {} seconds".format(time.time() - t))


@app.route('/hosting', methods=['GET'])
def get_hosting_info():
    domain = request.args.get('domain')

    t = time.time()
    hosting_information = brand_detector.get_hosting_info(domain)
    logging.info("Found hosting for {} in {} seconds".format(domain, time.time() - t))

    return jsonify({'data': hosting_information})


@app.route('/registrar', methods=['GET'])
def get_registrar_info():
    domain = request.args.get('domain')

    t = time.time()
    registrar_information = brand_detector.get_registrar_info(domain)
    logging.info("Found registrar for {} in {} seconds".format(domain, time.time() - t))

    return jsonify({'data': registrar_information})


@app.route('/health', methods=['GET'])
def health():
    return '', 200

if __name__ == '__main__':
    app.run()
