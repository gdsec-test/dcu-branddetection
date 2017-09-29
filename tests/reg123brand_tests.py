from nose.tools import assert_true
from branddetection.asnhelper import ASNPrefixes
from mock import patch
from branddetection.brands.reg123brand import Reg123Brand


class TestReg123:

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def __init__(self, _ripe_get_prefixes_per_asn):
        self._reg123 = Reg123Brand()

    def test_is_reg123_hosted(self):
        reg123_test = {'hosting_company_name': '123-REG'}

        results = self._reg123.is_hosted(reg123_test)
        assert_true(results is not None)

    def test_is_not_reg123_hosted(self):
        not_reg123_test = {'hosting_company_name': 'GoDaddy.com, LLC'}

        results = self._reg123.is_hosted(not_reg123_test)
        assert_true(results is None)

    def test_is_reg123_registered(self):
        reg123_test = {'registrar_name': '123-REG'}

        results = self._reg123.is_registered(reg123_test)
        assert_true(results is not None)

    def test_is_not_reg123_registered(self):
        not_reg123_test = {'registrar_name': 'GoDaddy.com, LLC'}

        results = self._reg123.is_registered(not_reg123_test)
        assert_true(results is None)

    @patch.object(ASNPrefixes, 'get_network_for_ip')
    def test_is_ip_in_range(self, get_network_for_ip):
        get_network_for_ip.return_value = ['80.90.194.0']
        reg123_test_ip = '80.90.194.0'

        results = self._reg123.is_ip_in_range(reg123_test_ip)
        assert_true(results == ['80.90.194.0'])
