from unittest import TestCase

from mock import MagicMock, patch

from branddetection.asnhelper import ASNPrefixes
from branddetection.brands.emeabrand import EMEABrand
from branddetection.brands.plusserverbrand import PlusServerBrand
from branddetection.brands.reg123brand import Reg123Brand


class TestEMEA(TestCase):
    _emea_ip = '80.90.194.0'
    _gd = 'GoDaddy'
    _123reg = 'WEBFUSION'

    def setUp(self):
        ASNPrefixes._ripe_get_prefixes_per_asn = MagicMock()
        self._emea = EMEABrand()

    def test_is_hosted(self):
        self._emea._brands = [PlusServerBrand(), Reg123Brand()]
        hosted_dict = {'brand': None, 'ip': None, 'hosting_company_name': self._123reg, 'hosting_abuse_email': None}
        hosted_results = self._emea.is_hosted(hosted_dict)
        self.assertTrue(hosted_results)

    def test_is_not_hosted(self):
        test_dict = {'brand': None, 'ip': None, 'hosting_company_name': self._gd, 'hosting_abuse_email': None}
        hosted_results = self._emea.is_hosted(test_dict)
        self.assertFalse(hosted_results)

    def test_is_registered(self):
        reg_dict = {'brand': None, 'registrar_name': self._123reg, 'registrar_abuse_email': None, 'domain_create_date': None}
        reg_results = self._emea.is_registered(reg_dict)
        self.assertTrue(reg_results)

    def test_is_not_registered(self):
        reg_dict = {'brand': None, 'registrar_name': self._gd, 'registrar_abuse_email': None, 'domain_create_date': None}
        reg_results = self._emea.is_registered(reg_dict)
        self.assertFalse(reg_results)

    @patch.object(ASNPrefixes, '_query_ripe')
    def test_is_ip_in_range(self, _query_ripe):
        _query_ripe.return_value = {'data': {'prefixes': [{'prefix': self._emea_ip}]}}
        ip_emea = self._emea.is_ip_in_range(self._emea_ip)
        self.assertFalse(ip_emea)

    @patch.object(ASNPrefixes, '_query_ripe')
    def test_is_not_in_range(self, _query_ripe):
        _query_ripe.return_value = {'data': {'prefixes': [{'prefix': self._emea_ip}]}}
        ip_not_emea = self._emea.is_ip_in_range('208.109.192.70')
        self.assertFalse(ip_not_emea)

    def test_email_from_hosting_name(self):
        whois_dict = {'brand': None, 'hosting_company_name': '123REG'}
        email = self._emea.get_email_for_hosted_from_whois(whois_dict)
        self.assertEquals(email, 'abuse@123-reg.co.uk')

    @patch('branddetection.brands.emeabrand.socket.gethostbyaddr', return_value=['HEARTINTERNET'])
    def test_email_from_hosting_ip(self, mock_get_host_by_addr):
        whois_dict = {'brand': None, 'ip': 'N/A'}
        email = self._emea.get_email_for_hosted_from_whois(whois_dict)
        self.assertEqual(email, 'abuse@heartinternet.co.uk')

    def test_email_from_hosted_default(self):
        email = self._emea.get_email_for_hosted_from_whois({})
        self.assertEqual(email, 'automationfails-emea@godaddy.com')

    @patch('branddetection.brands.domainfactorybrand.DomainFactoryBrand.is_ip_in_range', return_value=True)
    def test_get_email_from_ip(self, mock_is_ip_in_range):
        email = self._emea.get_email_from_ip(self._emea_ip)
        self.assertEqual(email, 'abuse@domainfactory.de')

    def test_get_email_from_ip_default(self):
        email = self._emea.get_email_from_ip('')
        self.assertEqual(email, 'automationfails-emea@godaddy.com')

    def test_get_email_from_registrar(self):
        email = self._emea.get_email_for_registrar_from_whois({'registrar_name': 'HOSTEUROPE'})
        self.assertEqual(email, 'abuse@hosteurope.de')

    def test_get_email_from_registrar_default(self):
        email = self._emea.get_email_for_registrar_from_whois({})
        self.assertEqual(email, 'automationfails-emea@godaddy.com')
