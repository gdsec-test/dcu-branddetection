import os


class AppConfig(object):
    REDIS_TTL = 24 * 60 * 60  # Seconds in a day

    def __init__(self):
        self.REDIS = os.getenv('REDIS') or 'localhost'
        self.DOMAIN_SERVICE_URL = os.getenv('DOMAIN_SERVICE_URL') or 'localhost:9000'


class ProductionAppConfig(AppConfig):
    SSO_URL = 'sso.godaddy.com'
    CN_WHITELIST = ['cmapservice.int.godaddy.com', 'kelvinservice.int.godaddy.com', 'testapi.threat.dev-godaddy.com']

    def __init__(self):
        super(ProductionAppConfig, self).__init__()


class OTEAppConfig(AppConfig):
    SSO_URL = 'sso.ote-godaddy.com'
    CN_WHITELIST = ['cmapservice.int.ote-godaddy.com', 'kelvinservice.int.ote-godaddy.com', 'testapi.threat.dev-godaddy.com']

    def __init__(self):
        super(OTEAppConfig, self).__init__()


class DevelopmentAppConfig(AppConfig):
    SSO_URL = 'sso.dev-godaddy.com'
    CN_WHITELIST = ['cmapservice.int.dev-godaddy.com', 'kelvinservice.int.dev-godaddy.com', 'testapi.threat.dev-godaddy.com']

    def __init__(self):
        super(DevelopmentAppConfig, self).__init__()


class TestAppConfig:

    DOMAIN_SERVICE_URL = 'localhost:9000'
    REDIS = 'localhost'
    SSO_URL = ''
    CN_WHITELIST = []


config_by_name = {'dev': DevelopmentAppConfig,
                  'ote': OTEAppConfig,
                  'prod': ProductionAppConfig}
