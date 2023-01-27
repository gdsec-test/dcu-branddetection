from unittest import TestCase

from branddetection.asnhelper import ASNPrefixes


class TestASNPrefixes(TestCase):
    def setUp(self):
        self._asns = [26496]
        self._asn = ASNPrefixes(self._asns)

    def test_get_network_for_ip(self):
        result = self._asn.get_network_for_ip('208.109.192.70')
        self.assertTrue(result[0] is not None)

    def test_not_get_network_for_ip(self):
        result = self._asn.get_network_for_ip('A')
        self.assertEqual(result, [])
