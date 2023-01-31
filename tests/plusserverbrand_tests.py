from unittest import TestCase

from mock import patch

from branddetection.asnhelper import ASNPrefixes
from branddetection.brands.plusserverbrand import PlusServerBrand


class TestPlusServerBrand(TestCase):
    _emea_ip = '87.119.203.59'
    _gd_llc = 'GoDaddy.com, LLC'

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def setUp(self, _ripe_get_prefixes_per_asn):
        self._plusserver = PlusServerBrand()

    def test_is_plusserver_registered(self):
        plusserver_test = {'registrar_name': 'MESHDE'}

        results = self._plusserver.is_registered(plusserver_test)
        self.assertIsNotNone(results)

    def test_is_not_plusserver_registered(self):
        not_plusserver_test = {'registrar_name': self._gd_llc}

        results = self._plusserver.is_registered(not_plusserver_test)
        self.assertIsNone(results)

    @patch.object(ASNPrefixes, 'get_network_for_ip')
    def test_is_ip_in_range(self, get_network_for_ip):
        get_network_for_ip.return_value = [self._emea_ip]
        plusserver_test_ip = self._emea_ip

        results = self._plusserver.is_ip_in_range(plusserver_test_ip)
        self.assertEqual(results, [self._emea_ip])
        # IP found under ASN 25074
