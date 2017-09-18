from nose.tools import assert_true
from mock import patch
from branddetection.asnhelper import ASNPrefixes
from branddetection.brands.godaddybrand import GoDaddyBrand


class TestGoaddyBrand:
    def __init__(self):
        pass

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def test_hostname_is_hosted(self, _ripe_get_prefixes_per_asn):
        _ripe_get_prefixes_per_asn.return_value = []
        gdb = GoDaddyBrand()

        test_value = {'hosting_company_name': 'GoDaddy.com, LLC'}

        result = gdb.is_hosted(test_value)
        assert_true(result is True)

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def test_rdns_is_hosted(self, _ripe_get_prefixes_per_asn):
        _ripe_get_prefixes_per_asn.return_value = []
        gdb = GoDaddyBrand()

        test_value = {'hosting_company_name': 'UK-WEBFUSION-LEEDS', 'ip': '208.109.192.70'}

        result = gdb.is_hosted(test_value)
        assert_true(result is True)

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def test_false_is_hosted(self, _ripe_get_prefixes_per_asn):
        _ripe_get_prefixes_per_asn.return_value = []
        gdb = GoDaddyBrand()

        test_value = {'hosting_company_name': 'UK-WEBFUSION-LEEDS', 'ip': '212.48.64.1'}

        result = gdb.is_hosted(test_value)
        assert_true(result is False)

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def test_godaddy_is_registered(self, _ripe_get_prefixes_per_asn):
        _ripe_get_prefixes_per_asn.return_value = []
        gdb = GoDaddyBrand()

        test_value = {'registrar_name': 'GoDaddy.com, LLC'}

        result = gdb.is_registered(test_value)
        assert_true(result is not None)

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def test_notgodaddy_is_registered(self, _ripe_get_prefixes_per_asn):
        _ripe_get_prefixes_per_asn.return_value = []
        gdb = GoDaddyBrand()

        test_value = {'registrar_name': 'CSC CORPORATE DOMAINS, INC.'}

        result = gdb.is_registered(test_value)
        assert_true(result is None)

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    @patch.object(ASNPrefixes, 'get_network_for_ip')
    def test_is_ip_in_range(self, get_network_for_ip, _ripe_get_prefixes_per_asn):
        get_network_for_ip.return_value = ['208.109.192.70']
        _ripe_get_prefixes_per_asn.return_value = []
        gdb = GoDaddyBrand()

        test_value = '208.109.192.70'

        result = gdb.is_ip_in_range(test_value)
        assert_true(result == ['208.109.192.70'])
