import json

from mock import patch
from nose.tools import assert_equal, assert_is_none

from branddetection.asnhelper import ASNPrefixes
from branddetection.branddetector import BrandDetector, BrandDetectorDecorator
from branddetection.brands.emeabrand import EMEABrand
from branddetection.domainhelper import DomainHelper
from branddetection.rediscache import RedisCache
from settings import TestAppConfig


class TestBrandDetectorDecorator:
    _gd_ip = '208.109.192.70'
    _gd_abuse_email = 'abuse@godaddy.com'
    _gd_brand = 'GODADDY'
    _gd_llc = 'GoDaddy.com LLC'

    def __init__(self):
        self._tbd = BrandDetectorDecorator(BrandDetector, RedisCache(None))

    @patch.object(DomainHelper, 'convert_domain_to_ip', return_value=None)
    def test_none_get_hosting_info(self, convert_domain_to_ip):
        test_value = {'brand': None, 'hosting_company_name': None, 'hosting_abuse_email': None, 'ip': None}
        result = self._tbd.get_hosting_info(self._gd_ip)
        assert_equal(result, test_value)

    @patch.object(BrandDetectorDecorator, '_add_whois_info_to_cache', return_value=None)
    @patch.object(BrandDetectorDecorator, '_get_whois_info_from_cache', return_value=None)
    @patch.object(BrandDetector, 'get_hosting_info')
    @patch.object(DomainHelper, 'convert_domain_to_ip')
    def test_whoislookup_get_hosting_info(self, convert_domain_to_ip, get_hosting_info, _get_whos_info_from_cache,
                                          _add_whois_info_to_cache):
        convert_domain_to_ip.return_value = self._gd_ip
        get_hosting_info.return_value = {'brand': self._gd_brand, 'hosting_company_name': self._gd_llc,
                                         'ip': self._gd_ip, 'hosting_abuse_email': [self._gd_abuse_email]}

        test_value = {'brand': self._gd_brand, 'hosting_company_name': self._gd_llc,
                      'ip': self._gd_ip, 'hosting_abuse_email': [self._gd_abuse_email]}

        result = self._tbd.get_hosting_info(self._gd_ip)
        assert_equal(result, test_value)

    @patch.object(BrandDetectorDecorator, '_add_whois_info_to_cache', return_value=None)
    @patch.object(BrandDetectorDecorator, '_get_whois_info_from_cache', return_value=None)
    @patch.object(BrandDetector, 'get_registrar_info')
    def test_get_registrar_info(self, get_registrar_info, _get_whos_info_from_cache, _add_whois_info_to_cache):
        get_registrar_info.return_value = {'brand': self._gd_brand, 'domain_create_date': '1999-03-02',
                                           'registrar_abuse_email': [self._gd_abuse_email, 'companynames@godaddy.com'],
                                           'registrar_name': self._gd_llc}

        test_value = {'brand': self._gd_brand, 'domain_create_date': '1999-03-02',
                      'registrar_abuse_email': [self._gd_abuse_email, 'companynames@godaddy.com'],
                      'registrar_name': self._gd_llc}

        result = self._tbd.get_registrar_info('godaddy.com')
        assert_equal(result, test_value)

    @patch.object(RedisCache, 'get_value', return_value=json.dumps({'result': 'test'}))
    def test_result_get_whois_info_from_cache(self, get_value):
        result = self._tbd._get_whois_info_from_cache('godaddy.com-registrar_whois_info')
        assert_equal(result, 'test')

    @patch.object(RedisCache, 'get_value', return_value=None)
    def test_none_get_whos_info_from_cache(self, get_value):
        result = self._tbd._get_whois_info_from_cache('godaddy.com-registrar_whois_info')
        assert_is_none(result)


class TestBrandDetector:
    _gd_ip = '208.109.192.70'
    _gd_abuse_email = 'abuse@godaddy.com'
    _gd_brand = 'GODADDY'
    _emea_ip = '212.48.64.1'
    _emea_brand = 'EMEA'
    _gd_llc = 'GoDaddy.com LLC'

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def __init__(self, _ripe_get_prefixes_per_asn):
        self._bd = BrandDetector(TestAppConfig())

    @patch.object(BrandDetector, '_get_hosting_in_known_ip_range')
    def test_ip_range_get_hosting_info(self, _get_hosting_in_known_ip_range):
        _get_hosting_in_known_ip_range.return_value = {'brand': self._gd_brand, 'hosting_company_name': self._gd_llc,
                                                       'ip': self._gd_ip,
                                                       'hosting_abuse_email': [self._gd_abuse_email]}
        test_value = _get_hosting_in_known_ip_range.return_value

        result = self._bd.get_hosting_info(self._gd_ip)
        assert_equal(result, test_value)

    @patch.object(BrandDetector, '_get_hosting_in_known_ip_range', return_value=None)
    @patch.object(BrandDetector, '_get_hosting_by_fallback')
    def test_fallback_get_hosting_info(self, _get_hosting_by_fallback, _get_hosting_in_known_ip_range):
        _get_hosting_by_fallback.return_value = {'brand': self._gd_brand, 'hosting_company_name': 'GO-DADDY-COM-LLC',
                                                 'ip': self._gd_ip,
                                                 'hosting_abuse_email': [self._gd_abuse_email, 'noc@godaddy.com']}
        test_value = _get_hosting_by_fallback.return_value

        result = self._bd.get_hosting_info(self._gd_ip)
        assert_equal(result, test_value)

    @patch.object(DomainHelper, 'get_registrar_information_via_whois')
    def test_godaddy_get_registrar_info(self, get_registrar_information_via_whois):
        get_registrar_information_via_whois.return_value = {'domain_create_date': '1999-03-02',
                                                            'registrar_abuse_email': [self._gd_abuse_email,
                                                                                      'companynames@godaddy.com'],
                                                            'registrar_name': 'GoDaddy.com, LLC'}

        test_value = {'brand': self._gd_brand, 'domain_create_date': '1999-03-02',
                      'registrar_abuse_email': [self._gd_abuse_email, 'companynames@godaddy.com'],
                      'registrar_name': 'GoDaddy.com, LLC', 'domain_id': None}

        result = self._bd.get_registrar_info('godaddy.com')
        assert_equal(result, test_value)

    @patch.object(ASNPrefixes, '_query_ripe')
    @patch.object(DomainHelper, 'get_registrar_information_via_whois')
    def test_emea_get_registrar_info(self, get_registrar_information_via_whois, _query_ripe):
        get_registrar_information_via_whois.return_value = {'domain_create_date': '2011-08-22',
                                                            'registrar_abuse_email': None,
                                                            'registrar_name': '123-reg.co.uk'}
        bd = BrandDetector(TestAppConfig())
        bd._brands = [EMEABrand()]  # overwrite with removed GoDaddyBrand() to test EMEABrand

        test_value = {'brand': self._emea_brand, 'domain_create_date': '2011-08-22', 'registrar_abuse_email': None,
                      'registrar_name': '123-reg.co.uk', 'domain_id': None}

        result = self._bd.get_registrar_info('jenisawesome.co.uk')
        assert_equal(result, test_value)

    @patch.object(DomainHelper, 'get_registrar_information_via_whois')
    def test_none_get_registrar_info(self, get_registrar_information_via_whois):
        get_registrar_information_via_whois.return_value = {'domain_create_date': '1995-06-02',
                                                            'registrar_abuse_email': ['domainabuse@cscglobal.com',
                                                                                      'vshostmaster@verisign.com'],
                                                            'registrar_name': 'CSC CORPORATE DOMAINS, INC.'}
        self._bd._brands = []  # overwrite to test FOREIGN

        test_value = {'domain_create_date': '1995-06-02', 'registrar_abuse_email': ['domainabuse@cscglobal.com',
                                                                                    'vshostmaster@verisign.com'],
                      'brand': 'FOREIGN', 'registrar_name': 'CSC CORPORATE DOMAINS, INC.', 'domain_id': None}

        result = self._bd.get_registrar_info('verisign.com')
        assert_equal(result, test_value)

    @patch.object(ASNPrefixes, '_query_ripe')
    def test_godaddy_get_hosting_in_known_ip_range(self, _query_ripe):
        _query_ripe.return_value = {'data': {'prefixes': [{'prefix': self._gd_ip}]}}

        test_value = {'brand': self._gd_brand, 'hosting_company_name': self._gd_llc, 'ip': self._gd_ip,
                      'hosting_abuse_email': [self._gd_abuse_email]}

        result = self._bd._get_hosting_in_known_ip_range(self._gd_ip)
        assert_equal(result, test_value)

    @patch.object(ASNPrefixes, '_query_ripe')
    def test_emea_get_hosting_in_known_ip_range(self, _query_ripe):
        _query_ripe.return_value = {'data': {'prefixes': [{'prefix': self._emea_ip}]}}
        bd = BrandDetector(TestAppConfig())
        bd._brands = [EMEABrand()]  # overwrite with removed GoDaddyBrand() to test EMEABrand

        test_value = {'brand': self._emea_brand, 'hosting_company_name': 'Host Europe GmbH', 'ip': self._emea_ip,
                      'hosting_abuse_email': ['abuse-input@heg.com']}

        result = bd._get_hosting_in_known_ip_range(self._emea_ip)
        assert_equal(result, test_value)

    def test_none_get_hosting_in_known_ip_range(self):
        self._bd._brands = []  # overwrite with empty for testing return of None
        test_value = None
        result = self._bd._get_hosting_in_known_ip_range('127.0.0.0')
        assert_equal(result, test_value)

    def test_godaddy_get_hosting_by_fallback(self):
        test_value = {'brand': self._gd_brand, 'hosting_company_name': 'GO-DADDY-COM-LLC', 'ip': self._gd_ip,
                      'hosting_abuse_email': [self._gd_abuse_email, 'noc@godaddy.com']}
        result = self._bd._get_hosting_by_fallback(self._gd_ip)
        assert_equal(result, test_value)

    @patch.object(ASNPrefixes, '_query_ripe')
    def test_emea_get_hosting_by_fallback(self, _query_ripe):
        _query_ripe.return_value = {'data': {'prefixes': [{'prefix': self._emea_ip}]}}
        bd = BrandDetector(TestAppConfig())
        bd._brands = [EMEABrand()]  # overwrite with removed GoDaddyBrand() to test EMEABrand

        test_value = {'hosting_company_name': 'UK-WEBFUSION-LEEDS', 'ip': self._emea_ip, 'brand': self._emea_brand,
                      'hosting_abuse_email': ['abuse@123-reg.co.uk']}

        result = bd._get_hosting_by_fallback(self._emea_ip)
        assert_equal(result, test_value)

    def test_foreign_get_hosting_by_fallback(self):
        test_value = {'hosting_company_name': None, 'ip': None, 'brand': 'FOREIGN', 'hosting_abuse_email': None}
        result = self._bd._get_hosting_by_fallback('127.0.0.0')
        assert_equal(result, test_value)
