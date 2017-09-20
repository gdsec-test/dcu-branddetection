from nose.tools import assert_true
from mock import patch
from branddetection.asnhelper import ASNPrefixes
from branddetection.brands.plusserverbrand import PlusServerBrand


class TestPlusServerBrand:

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def __init__(self, _ripe_get_prefixes_per_asn):
        _ripe_get_prefixes_per_asn.return_value = []
        self._plusServer = PlusServerBrand()

    def test_is_plusServer_hosted(self):
        plusServer_test = {'hosting_company_name': 'Mainlab'}

        results = self._plusServer.is_hosted(plusServer_test)
        assert_true(results is not None)

    def test_is_notplusServer_hosted(self):
        not_plusServer_test = {'hosting_company_name': 'GoDaddy.com, LLC'}

        results = self._plusServer.is_hosted(not_plusServer_test)
        assert_true(results is None)

    def test_is_plusServer_registered(self):
        plusServer_test = {'registrar_name': 'MESHDE'}

        results = self._plusServer.is_registered(plusServer_test)
        assert_true(results is not None)

    def test_is_plusServer_registered(self):
        not_plusServer_test = {'registrar_name': 'GoDaddy.com, LLC'}

        results = self._plusServer.is_registered(not_plusServer_test)
        assert_true(results is None)

    @patch.object(ASNPrefixes, 'get_network_for_ip')
    def test_is_ip_in_range(self, get_network_for_ip):
        get_network_for_ip.return_value = ['87.119.203.59']
        plusServer_test_ip = '87.119.203.59'

        results = self._plusServer.is_ip_in_range(plusServer_test_ip)
        assert_true(results == ['87.119.203.59'])
        #IP found under ASN 25074