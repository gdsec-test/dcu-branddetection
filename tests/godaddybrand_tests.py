from nose.tools import assert_true
from mock import patch
from branddetection.asnhelper import ASNPrefixes
from branddetection.brands.godaddybrand import GoDaddyBrand


class TestGodaddyBrand:

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def __init__(self, _ripe_get_prefixes_per_asn):
        self._gdb = GoDaddyBrand()
        self._gd_ip = '208.109.192.70'
        self._gd_llc = 'GoDaddy.com, LLC'
        self._webfusion = 'UK-WEBFUSION-LEEDS'

    def test_hostname_is_hosted(self):
        test_value = {'hosting_company_name': self._gd_llc}

        result = self._gdb.is_hosted(test_value)
        assert_true(result is True)

    def test_rdns_is_hosted(self):
        test_value = {'hosting_company_name': self._webfusion, 'ip': self._gd_ip}

        result = self._gdb.is_hosted(test_value)
        assert_true(result is True)

    def test_false_is_hosted(self):
        test_value = {'hosting_company_name': self._webfusion, 'ip': '212.48.64.1'}

        result = self._gdb.is_hosted(test_value)
        assert_true(result is False)

    def test_godaddy_is_registered(self):
        test_value = {'registrar_name': self._gd_llc}

        result = self._gdb.is_registered(test_value)
        assert_true(result is not None)

    def test_notgodaddy_is_registered(self):
        test_value = {'registrar_name': 'CSC CORPORATE DOMAINS, INC.'}

        result = self._gdb.is_registered(test_value)
        assert_true(result is None)

    @patch.object(ASNPrefixes, 'get_network_for_ip')
    def test_is_ip_in_range(self, get_network_for_ip):
        get_network_for_ip.return_value = [self._gd_ip]
        test_value = self._gd_ip

        result = self._gdb.is_ip_in_range(test_value)
        assert_true(result == [self._gd_ip])
