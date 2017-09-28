import json

from nose.tools import assert_true
from mock import patch

from branddetection.branddetector import BrandDetector, BrandDetectorDecorator
from branddetection.domainhelper import DomainHelper
from branddetection.asnhelper import ASNPrefixes
from branddetection.brands.emeabrand import EMEABrand
from branddetection.rediscache import RedisCache


class TestBrandDetectorDecorator:

    def __init__(self):
        self._tbd = BrandDetectorDecorator(BrandDetector, RedisCache(None))

    @patch.object(DomainHelper, 'convert_domain_to_ip')
    def test_none_get_hosting_info(self, convert_domain_to_ip):
        convert_domain_to_ip.return_value = None

        test_value = {'brand': None, 'hosting_company_name': None, 'hosting_abuse_email': None, 'ip': None}

        result = self._tbd.get_hosting_info('208.109.192.70')
        assert_true(result == test_value)

    @patch.object(BrandDetectorDecorator, '_add_whois_info_to_cache')
    @patch.object(BrandDetectorDecorator, '_get_whos_info_from_cache')
    @patch.object(BrandDetector, 'get_hosting_info')
    @patch.object(DomainHelper, 'convert_domain_to_ip')
    def test_whoislookup_get_hosting_info(self, convert_domain_to_ip, get_hosting_info, _get_whos_info_from_cache,
                                          _add_whois_info_to_cache):
        convert_domain_to_ip.return_value = '208.109.192.70'
        get_hosting_info.return_value = {'brand': 'GODADDY', 'hosting_company_name': 'GoDaddy.com LLC',
                                         'ip': '208.109.192.70', 'hosting_abuse_email': ['abuse@godaddy.com']}
        _get_whos_info_from_cache.return_value = None
        _add_whois_info_to_cache.return_value = None

        test_value = {'brand': 'GODADDY', 'hosting_company_name': 'GoDaddy.com LLC',
                      'ip': '208.109.192.70', 'hosting_abuse_email': ['abuse@godaddy.com']}

        result = self._tbd.get_hosting_info('208.109.192.70')
        assert_true(result == test_value)

    @patch.object(BrandDetectorDecorator, '_add_whois_info_to_cache')
    @patch.object(BrandDetectorDecorator, '_get_whos_info_from_cache')
    @patch.object(BrandDetector, 'get_registrar_info')
    def test_get_registrar_info(self, get_registrar_info, _get_whos_info_from_cache, _add_whois_info_to_cache):
        get_registrar_info.return_value = {'brand': 'GODADDY', 'domain_create_date': '1999-03-02',
                                           'registrar_abuse_email': ['abuse@godaddy.com', 'companynames@godaddy.com'],
                                           'registrar_name': 'GoDaddy.com, LLC'}
        _get_whos_info_from_cache.return_value = None
        _add_whois_info_to_cache.return_value = None

        test_value = {'brand': 'GODADDY', 'domain_create_date': '1999-03-02',
                      'registrar_abuse_email': ['abuse@godaddy.com', 'companynames@godaddy.com'],
                      'registrar_name': 'GoDaddy.com, LLC'}

        result = self._tbd.get_registrar_info('godaddy.com')
        assert_true(result == test_value)

    @patch.object(RedisCache, 'get_value')
    def test_result_get_whos_info_from_cache(self, get_value):
        json_string = json.dumps({'result': 'test'})
        get_value.return_value = json_string

        result = self._tbd._get_whos_info_from_cache('godaddy.com-registrar_whois_info')
        assert_true(result == 'test')

    @patch.object(RedisCache, 'get_value')
    def test_none_get_whos_info_from_cache(self, get_value):
        get_value.return_value = None

        result = self._tbd._get_whos_info_from_cache('godaddy.com-registrar_whois_info')
        assert_true(result is None)


class TestBrandDetector:

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def __init__(self, _ripe_get_prefixes_per_asn):
        self._bd = BrandDetector()

    @patch.object(BrandDetector, '_get_hosting_in_known_ip_range')
    def test_ip_range_get_hosting_info(self, _get_hosting_in_known_ip_range):
        _get_hosting_in_known_ip_range.return_value = {'brand': 'GODADDY', 'hosting_company_name': 'GoDaddy.com LLC',
                                                       'ip': '208.109.192.70',
                                                       'hosting_abuse_email': ['abuse@godaddy.com']}

        test_value = _get_hosting_in_known_ip_range.return_value

        result = self._bd.get_hosting_info('208.109.192.70')
        assert_true(result == test_value)

    @patch.object(BrandDetector, '_get_hosting_in_known_ip_range')
    @patch.object(BrandDetector, '_get_hosting_by_fallback')
    def test_fallback_get_hosting_info(self, _get_hosting_by_fallback, _get_hosting_in_known_ip_range):
        _get_hosting_by_fallback.return_value = {'brand': 'GODADDY', 'hosting_company_name': 'GO-DADDY-COM-LLC',
                                                 'ip': '208.109.192.70',
                                                 'hosting_abuse_email': ['abuse@godaddy.com', 'noc@godaddy.com']}
        _get_hosting_in_known_ip_range.return_value = None

        test_value = _get_hosting_by_fallback.return_value

        result = self._bd.get_hosting_info('208.109.192.70')
        assert_true(result == test_value)

    @patch.object(DomainHelper, 'get_registrar_information_via_whois')
    def test_godaddy_get_registrar_info(self, get_registrar_information_via_whois):
        get_registrar_information_via_whois.return_value = {'domain_create_date': '1999-03-02',
                                                            'registrar_abuse_email': ['abuse@godaddy.com',
                                                                                      'companynames@godaddy.com'],
                                                            'registrar_name': 'GoDaddy.com, LLC'}

        test_value = {'brand': 'GODADDY', 'domain_create_date': '1999-03-02',
                      'registrar_abuse_email': ['abuse@godaddy.com', 'companynames@godaddy.com'],
                      'registrar_name': 'GoDaddy.com, LLC'}

        result = self._bd.get_registrar_info('godaddy.com')
        assert_true(result == test_value)

    @patch.object(ASNPrefixes, '_query_ripe')
    @patch.object(DomainHelper, 'get_registrar_information_via_whois')
    def test_emea_get_registrar_info(self, get_registrar_information_via_whois, _query_ripe):
        get_registrar_information_via_whois.return_value = {'domain_create_date': '2011-08-22',
                                                            'registrar_abuse_email': None,
                                                            'registrar_name': '123-reg.co.uk'}
        bd = BrandDetector()
        bd._brands = [EMEABrand()]  # overwrite with removed GoDaddyBrand() to test EMEABrand

        test_value = {'brand': 'EMEA', 'domain_create_date': '2011-08-22', 'registrar_abuse_email': None,
                      'registrar_name': '123-reg.co.uk'}

        result = self._bd.get_registrar_info('jenisawesome.co.uk')
        assert_true(result == test_value)

    @patch.object(DomainHelper, 'get_registrar_information_via_whois')
    def test_none_get_registrar_info(self, get_registrar_information_via_whois):
        get_registrar_information_via_whois.return_value = {'domain_create_date': '1995-06-02',
                                                            'registrar_abuse_email': ['domainabuse@cscglobal.com',
                                                                                      'vshostmaster@verisign.com'],
                                                            'registrar_name': 'CSC CORPORATE DOMAINS, INC.'}
        self._bd._brands = []  # overwrite to test FOREIGN

        test_value = {'domain_create_date': '1995-06-02', 'registrar_abuse_email': ['domainabuse@cscglobal.com',
                                                                                    'vshostmaster@verisign.com'],
                      'brand': 'FOREIGN', 'registrar_name': 'CSC CORPORATE DOMAINS, INC.'}

        result = self._bd.get_registrar_info('verisign.com')
        assert_true(result == test_value)

    @patch.object(ASNPrefixes, '_query_ripe')
    def test_godaddy_get_hosting_in_known_ip_range(self, _query_ripe):
        _query_ripe.return_value = {'data': {'prefixes': [{'prefix': '208.109.192.70'}]}}

        test_value = {'brand': 'GODADDY', 'hosting_company_name': 'GoDaddy.com LLC', 'ip': '208.109.192.70',
                      'hosting_abuse_email': ['abuse@godaddy.com']}

        result = self._bd._get_hosting_in_known_ip_range('208.109.192.70')
        assert_true(result == test_value)

    @patch.object(ASNPrefixes, '_query_ripe')
    def test_emea_get_hosting_in_known_ip_range(self, _query_ripe):
        _query_ripe.return_value = {'data': {'prefixes': [{'prefix': '212.48.64.1'}]}}
        bd = BrandDetector()
        bd._brands = [EMEABrand()]  # overwrite with removed GoDaddyBrand() to test EMEABrand

        test_value = {'brand': 'EMEA', 'hosting_company_name': 'Host Europe GmbH', 'ip': '212.48.64.1',
                      'hosting_abuse_email': ['abuse-input@heg.com']}

        result = bd._get_hosting_in_known_ip_range('212.48.64.1')
        assert_true(result == test_value)

    def test_none_get_hosting_in_known_ip_range(self):
        self._bd._brands = []  # overwrite with empty for testing return of None

        test_value = None

        result = self._bd._get_hosting_in_known_ip_range('127.0.0.0')
        assert_true(result == test_value)

    def test_godaddy_get_hosting_by_fallback(self):
        test_value = {'brand': 'GODADDY', 'hosting_company_name': 'GO-DADDY-COM-LLC', 'ip': '208.109.192.70',
                      'hosting_abuse_email': ['abuse@godaddy.com', 'noc@godaddy.com']}

        result = self._bd._get_hosting_by_fallback('208.109.192.70')
        assert_true(result == test_value)

    @patch.object(ASNPrefixes, '_query_ripe')
    def test_emea_get_hosting_by_fallback(self, _query_ripe):
        _query_ripe.return_value = {'data': {'prefixes': [{'prefix': '212.48.64.1'}]}}
        bd = BrandDetector()
        bd._brands = [EMEABrand()]  # overwrite with removed GoDaddyBrand() to test EMEABrand

        test_value = {'hosting_company_name': 'UK-WEBFUSION-LEEDS', 'ip': '212.48.64.1', 'brand': 'EMEA',
                      'hosting_abuse_email': ['abuse@webfusion.com']}

        result = bd._get_hosting_by_fallback('212.48.64.1')
        assert_true(result == test_value)

    def test_foreign_get_hosting_by_fallback(self):
        test_value = {'hosting_company_name': None, 'ip': None, 'brand': 'FOREIGN', 'hosting_abuse_email': None}

        result = self._bd._get_hosting_by_fallback('127.0.0.0')
        assert_true(result == test_value)
