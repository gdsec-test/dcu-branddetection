from nose.tools import assert_true
from mock import patch
from branddetection.asnhelper import ASNPrefixes
from branddetection.brands.godaddybrand import GoDaddyBrand


class TestGodaddyBrand:

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def __init__(self, _ripe_get_prefixes_per_asn):
        self._gdb = GoDaddyBrand()

    def test_hostname_is_hosted(self):
        test_value = {'hosting_company_name': 'GoDaddy.com, LLC'}

        result = self._gdb.is_hosted(test_value)
        assert_true(result is True)

    def test_rdns_is_hosted(self):
        test_value = {'hosting_company_name': 'UK-WEBFUSION-LEEDS', 'ip': '208.109.192.70'}

        result = self._gdb.is_hosted(test_value)
        assert_true(result is True)

    def test_false_is_hosted(self):
        test_value = {'hosting_company_name': 'UK-WEBFUSION-LEEDS', 'ip': '212.48.64.1'}

        result = self._gdb.is_hosted(test_value)
        assert_true(result is False)

    def test_godaddy_is_registered(self):
        test_value = {'registrar_name': 'GoDaddy.com, LLC'}

        result = self._gdb.is_registered(test_value)
        assert_true(result is not None)

    def test_notgodaddy_is_registered(self):
        test_value = {'registrar_name': 'CSC CORPORATE DOMAINS, INC.'}

        result = self._gdb.is_registered(test_value)
        assert_true(result is None)

    @patch.object(ASNPrefixes, 'get_network_for_ip')
    def test_is_ip_in_range(self, get_network_for_ip):
        get_network_for_ip.return_value = ['208.109.192.70']
        test_value = '208.109.192.70'

        result = self._gdb.is_ip_in_range(test_value)
        assert_true(result == ['208.109.192.70'])
