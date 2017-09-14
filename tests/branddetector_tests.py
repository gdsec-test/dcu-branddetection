from nose.tools import assert_true
from mock import patch
from branddetection.branddetector import BrandDetector
from branddetection.domainhelper import DomainHelper
from branddetection.asnhelper import ASNPrefixes
from branddetection.brands.emeabrand import EMEABrand


class TestBrandDetectorDecorator:  # AKA: MOCK ALL THE THINGS!!1!1!!
    def __init__(self):
        pass

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    @patch.object(BrandDetector, '_get_hosting_in_known_ip_range')
    def test_ip_range_get_hosting_info(self, _get_hosting_in_known_ip_range, _ripe_get_prefixes_per_asn):
        _get_hosting_in_known_ip_range.return_value = {'brand': 'GODADDY', 'hosting_company_name': 'GoDaddy.com LLC',
                                                       'ip': '208.109.192.70',
                                                       'hosting_abuse_email': ['abuse@godaddy.com']}
        _ripe_get_prefixes_per_asn.return_value = ['208.109.192.70']
        bd = BrandDetector()

        test_value = _get_hosting_in_known_ip_range.return_value

        result = bd.get_hosting_info('208.109.192.70')
        assert_true(result == test_value)

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    @patch.object(BrandDetector, '_get_hosting_in_known_ip_range')
    @patch.object(BrandDetector, '_get_hosting_by_fallback')
    def test_fallback_get_hosting_info(self, _get_hosting_by_fallback, _get_hosting_in_known_ip_range, _ripe_get_prefixes_per_asn):
        _get_hosting_by_fallback.return_value = {'brand': 'GODADDY', 'hosting_company_name': 'GO-DADDY-COM-LLC',
                                                 'ip': '208.109.192.70',
                                                 'hosting_abuse_email': ['abuse@godaddy.com', 'noc@godaddy.com']}
        _get_hosting_in_known_ip_range.return_value = None
        _ripe_get_prefixes_per_asn.return_value = ['208.109.192.70']
        bd = BrandDetector()

        test_value = _get_hosting_by_fallback.return_value

        result = bd.get_hosting_info('208.109.192.70')
        assert_true(result == test_value)

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    @patch.object(DomainHelper, 'get_registrar_information_via_whois')
    def test_godaddy_get_registrar_info(self, get_registrar_information_via_whois, _ripe_get_prefixes_per_asn):
        get_registrar_information_via_whois.return_value = {'domain_create_date': '1999-03-02',
                                                            'registrar_abuse_email': ['abuse@godaddy.com',
                                                                                      'companynames@godaddy.com'],
                                                            'registrar_name': 'GoDaddy.com, LLC'}
        _ripe_get_prefixes_per_asn.return_value = []
        bd = BrandDetector()

        test_value = {'brand': 'GODADDY', 'domain_create_date': '1999-03-02',
                      'registrar_abuse_email': ['abuse@godaddy.com', 'companynames@godaddy.com'],
                      'registrar_name': 'GoDaddy.com, LLC'}

        result = bd.get_registrar_info('godaddy.com')
        assert_true(result == test_value)

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    @patch.object(DomainHelper, 'get_registrar_information_via_whois')
    def test_emea_get_registrar_info(self, get_registrar_information_via_whois, _ripe_get_prefixes_per_asn):
        get_registrar_information_via_whois.return_value = {'domain_create_date': '2011-08-22',
                                                            'registrar_abuse_email': None,
                                                            'registrar_name': '123-reg.co.uk'}
        _ripe_get_prefixes_per_asn.return_value = []
        bd = BrandDetector()
        bd._brands = [EMEABrand()]  # overwrite with removed GoDaddyBrand() to test EMEABrand

        test_value = {'brand': 'EMEA', 'domain_create_date': '2011-08-22', 'registrar_abuse_email': None,
                      'registrar_name': '123-reg.co.uk'}

        result = bd.get_registrar_info('jenisawesome.co.uk')
        assert_true(result == test_value)

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    @patch.object(DomainHelper, 'get_registrar_information_via_whois')
    def test_none_get_registrar_info(self, get_registrar_information_via_whois, _ripe_get_prefixes_per_asn):
        get_registrar_information_via_whois.return_value = {'domain_create_date': '1995-06-02',
                                                            'registrar_abuse_email': ['domainabuse@cscglobal.com',
                                                                                      'vshostmaster@verisign.com'],
                                                            'registrar_name': 'CSC CORPORATE DOMAINS, INC.'}
        _ripe_get_prefixes_per_asn.return_value = []
        bd = BrandDetector()
        bd._brands = []  # overwrite to test FOREIGN

        test_value = {'domain_create_date': '1995-06-02', 'registrar_abuse_email': ['domainabuse@cscglobal.com',
                                                                                    'vshostmaster@verisign.com'],
                      'brand': 'FOREIGN', 'registrar_name': 'CSC CORPORATE DOMAINS, INC.'}

        result = bd.get_registrar_info('verisign.com')
        assert_true(result == test_value)

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def test_godaddy_get_hosting_in_known_ip_range(self, _ripe_get_prefixes_per_asn):
        _ripe_get_prefixes_per_asn.return_value = ['208.109.192.70']
        bd = BrandDetector()

        test_value = {'brand': 'GODADDY', 'hosting_company_name': 'GoDaddy.com LLC', 'ip': '208.109.192.70',
                      'hosting_abuse_email': ['abuse@godaddy.com']}

        result = bd._get_hosting_in_known_ip_range('208.109.192.70')
        assert_true(result == test_value)

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def test_emea_get_hosting_in_known_ip_range(self, _ripe_get_prefixes_per_asn):
        _ripe_get_prefixes_per_asn.return_value = ['212.48.64.1']
        bd = BrandDetector()
        bd._brands = [EMEABrand()]  # overwrite with removed GoDaddyBrand() to test EMEABrand

        test_value = {'brand': 'EMEA', 'hosting_company_name': 'Host Europe GmbH', 'ip': '212.48.64.1',
                      'hosting_abuse_email': ['abuse-input@heg.com']}

        result = bd._get_hosting_in_known_ip_range('212.48.64.1')
        assert_true(result == test_value)

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def test_none_get_hosting_in_known_ip_range(self, _ripe_get_prefixes_per_asn):
        _ripe_get_prefixes_per_asn.return_value = []
        bd = BrandDetector()
        bd._brands = []  # overwrite with empty for testing return of None

        test_value = None

        result = bd._get_hosting_in_known_ip_range('127.0.0.0')
        assert_true(result == test_value)

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def test_godaddy_get_hosting_by_fallback(self, _ripe_get_prefixes_per_asn):
        _ripe_get_prefixes_per_asn.return_value = ['208.109.192.70']
        bd = BrandDetector()

        test_value = {'brand': 'GODADDY', 'hosting_company_name': 'GO-DADDY-COM-LLC', 'ip': '208.109.192.70',
                      'hosting_abuse_email': ['abuse@godaddy.com', 'noc@godaddy.com']}

        result = bd._get_hosting_by_fallback('208.109.192.70')
        assert_true(result == test_value)

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def test_emea_get_hosting_by_fallback(self, _ripe_get_prefixes_per_asn):
        _ripe_get_prefixes_per_asn.return_value = ['212.48.64.1']
        bd = BrandDetector()
        bd._brands = [EMEABrand()]  # overwrite with removed GoDaddyBrand() to test EMEABrand

        test_value = {'hosting_company_name': 'UK-WEBFUSION-LEEDS', 'ip': '212.48.64.1', 'brand': 'EMEA',
                      'hosting_abuse_email': ['abuse@webfusion.com']}

        result = bd._get_hosting_by_fallback('212.48.64.1')
        assert_true(result == test_value)

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def test_foreign_get_hosting_by_fallback(self, _ripe_get_prefixes_per_asn):
        _ripe_get_prefixes_per_asn.return_value = ['127.0.0.0']
        bd = BrandDetector()

        test_value = {'hosting_company_name': None, 'ip': None, 'brand': 'FOREIGN', 'hosting_abuse_email': None}

        result = bd._get_hosting_by_fallback('127.0.0.0')
        assert_true(result == test_value)
