import os
import socket
from ipaddress import IPv4Network
from typing import Dict, List, Optional, Type


class AppConfig(object):
    REDIS_TTL = 24 * 60 * 60  # Seconds in a day
    CUSTOM_NS = None
    GODADDY_BRAND_NETWORK_OVERRIDES: Optional[List[IPv4Network]] = None

    def __init__(self):
        self.REDIS = os.getenv('REDIS') or 'localhost'
        self.DOMAIN_SERVICE_URL = os.getenv('DOMAIN_SERVICE_URL') or 'localhost:9000'


class ProductionAppConfig(AppConfig):
    SSO_URL = 'sso.gdcorp.tools'
    CN_WHITELIST = ['cmapservice.client.cset.int.gdcorp.tools', 'kelvinservice.client.cset.int.gdcorp.tools', 'testapi.threat.dev-godaddy.com']

    def __init__(self):
        super(ProductionAppConfig, self).__init__()


class OTEAppConfig(AppConfig):
    SSO_URL = 'sso.ote-gdcorp.tools'
    CN_WHITELIST = ['cmapservice.client.cset.int.ote-gdcorp.tools', 'kelvinservice.client.cset.int.ote-gdcorp.tools', 'testapi.threat.dev-godaddy.com']

    def __init__(self):
        super(OTEAppConfig, self).__init__()


class DevelopmentAppConfig(AppConfig):
    SSO_URL = 'sso.dev-gdcorp.tools'
    CN_WHITELIST = ['cmapservice.client.cset.int.dev-gdcorp.tools', 'kelvinservice.client.cset.int.dev-gdcorp.tools', 'testapi.threat.dev-godaddy.com']

    def __init__(self):
        super(DevelopmentAppConfig, self).__init__()


class TestEnvironmentAppConfig(AppConfig):
    SSO_URL = 'sso.test-gdcorp.tools'
    CN_WHITELIST = ['cmapservice.client.cset.int.test-gdcorp.tools', 'kelvinservice.client.cset.int.test-gdcorp.tools', 'testapi.threat.test-godaddy.com']

    def __init__(self):
        super(TestEnvironmentAppConfig, self).__init__()
        self.CUSTOM_NS = [
            socket.gethostbyname('ns03.test-dc.gdns.godaddy.com'),
            socket.gethostbyname('ns05.test-dc.gdns.godaddy.com')
        ]
        self.GODADDY_BRAND_NETWORK_OVERRIDES = [IPv4Network('10.0.0.0/8')]


class TestAppConfig:

    DOMAIN_SERVICE_URL = 'localhost:9000'
    REDIS = 'localhost'
    SSO_URL = ''
    CN_WHITELIST = []


config_by_name: Dict[str, Type[AppConfig]] = {
    'dev': DevelopmentAppConfig,
    'ote': OTEAppConfig,
    'prod': ProductionAppConfig,
    'testenv': TestEnvironmentAppConfig
}
