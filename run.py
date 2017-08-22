import os
import logging.config
import yaml
import time

from branddetection.branddetector import BrandDetector
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

if __name__ == '__main__':

    t1 = time.time()
    brand_detector = BrandDetector(config)
    logging.info("time take to initialize: {}".format(time.time() - t1))

    while True:
        ip = raw_input('Please provide an domain/IP to be scanned: ')
        t2 = time.time()
        logging.info("Hosting information is: {}".format(brand_detector.find_hosting(ip)))
        logging.info("Time to find hosting: {}".format(time.time() - t2))

        t2 = time.time()
        logging.info("Registrar information is: {}".format(brand_detector.find_registrar(ip)))
        logging.info("Time to find registration: {}".format(time.time() - t2))
