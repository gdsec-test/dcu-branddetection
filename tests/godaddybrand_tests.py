from mock import patch
from nose.tools import (assert_equal, assert_false, assert_is_none,
                        assert_is_not_none, assert_true)

from branddetection.asnhelper import ASNPrefixes
from branddetection.brands.godaddybrand import GoDaddyBrand


class TestGodaddyBrand:
    _gd_ip = '208.109.192.70'
    _gd_llc = 'GoDaddy.com, LLC'
    _webfusion = 'UK-WEBFUSION-LEEDS'
    _KEY_IP = 'ip'

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def __init__(self, _ripe_get_prefixes_per_asn):
        self._gdb = GoDaddyBrand()

    def test_hostname_is_hosted(self):
        test_value = {'hosting_company_name': self._gd_llc}
        result = self._gdb.is_hosted(test_value)
        assert_true(result)

    def test_rdns_is_hosted(self):
        test_value = {'hosting_company_name': self._webfusion, self._KEY_IP: self._gd_ip}
        result = self._gdb.is_hosted(test_value)
        assert_true(result)

    def test_false_is_hosted(self):
        test_value = {'hosting_company_name': self._webfusion, self._KEY_IP: '212.48.64.1'}
        result = self._gdb.is_hosted(test_value)
        assert_false(result)

    def test_godaddy_is_registered(self):
        test_value = {'registrar_name': self._gd_llc}
        result = self._gdb.is_registered(test_value)
        assert_is_not_none(result)

    def test_notgodaddy_is_registered(self):
        test_value = {'registrar_name': 'CSC CORPORATE DOMAINS, INC.'}
        result = self._gdb.is_registered(test_value)
        assert_is_none(result)

    @patch.object(ASNPrefixes, 'get_network_for_ip')
    def test_is_ip_in_range(self, get_network_for_ip):
        get_network_for_ip.return_value = [self._gd_ip]
        test_value = self._gd_ip
        result = self._gdb.is_ip_in_range(test_value)
        assert_equal(result, [self._gd_ip])

    def test_is_hosted_parked(self):
        test_value = {'hosting_company_name': self._webfusion, self._KEY_IP: '34.102.136.180'}
        assert_true(self._gdb.is_hosted(test_value))
        test_value = {'hosting_company_name': self._webfusion, self._KEY_IP: '34.98.99.30'}
        assert_true(self._gdb.is_hosted(test_value))
