from nose.tools import assert_true
from mock import patch
from branddetection.asnhelper import ASNPrefixes
from branddetection.brands.plusserverbrand import PlusServerBrand


class TestPlusServerBrand:

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def __init__(self, _ripe_get_prefixes_per_asn):
        _ripe_get_prefixes_per_asn.return_value = []
        self._plusserver = PlusServerBrand()

    def test_is_plusserver_hosted(self):
        plusserver_test = {'hosting_company_name': 'Mainlab'}

        results = self._plusserver.is_hosted(plusserver_test)
        assert_true(results is not None)

    def test_is_not_plusserver_hosted(self):
        not_plusserver_test = {'hosting_company_name': 'GoDaddy.com, LLC'}

        results = self._plusserver.is_hosted(not_plusserver_test)
        assert_true(results is None)

    def test_is_plusserver_registered(self):
        plusserver_test = {'registrar_name': 'MESHDE'}

        results = self._plusserver.is_registered(plusserver_test)
        assert_true(results is not None)

    def test_is_not_plusserver_registered(self):
        not_plusserver_test = {'registrar_name': 'GoDaddy.com, LLC'}

        results = self._plusserver.is_registered(not_plusserver_test)
        assert_true(results is None)

    @patch.object(ASNPrefixes, 'get_network_for_ip')
    def test_is_ip_in_range(self, get_network_for_ip):
        get_network_for_ip.return_value = ['87.119.203.59']
        plusserver_test_ip = '87.119.203.59'

        results = self._plusserver.is_ip_in_range(plusserver_test_ip)
        assert_true(results == ['87.119.203.59'])
        # IP found under ASN 25074
