from mock import patch
from nose.tools import assert_equal, assert_is_none, assert_is_not_none

from branddetection.asnhelper import ASNPrefixes
from branddetection.brands.reg123brand import Reg123Brand


class TestReg123:
    _emea_ip = '80.90.194.0'
    _123reg = '123-REG'
    _gd_llc = 'GoDaddy.com, LLC'

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def __init__(self, _ripe_get_prefixes_per_asn):
        self._reg123 = Reg123Brand()

    def test_is_reg123_registered(self):
        reg123_test = {'registrar_name': self._123reg}

        results = self._reg123.is_registered(reg123_test)
        assert_is_not_none(results)

    def test_is_not_reg123_registered(self):
        not_reg123_test = {'registrar_name': self._gd_llc}

        results = self._reg123.is_registered(not_reg123_test)
        assert_is_none(results)

    @patch.object(ASNPrefixes, 'get_network_for_ip')
    def test_is_ip_in_range(self, get_network_for_ip):
        get_network_for_ip.return_value = [self._emea_ip]
        reg123_test_ip = self._emea_ip

        results = self._reg123.is_ip_in_range(reg123_test_ip)
        assert_equal(results, [self._emea_ip])
