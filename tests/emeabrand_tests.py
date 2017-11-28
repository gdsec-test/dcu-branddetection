from nose.tools import assert_true
from branddetection.brands.emeabrand import EMEABrand
from branddetection.asnhelper import ASNPrefixes
from mock import patch
from branddetection.brands.reg123brand import Reg123Brand
from branddetection.brands.plusserverbrand import PlusServerBrand


class TestEMEA:
    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def __init__(self, _ripe_get_prefixes_per_asn):
        self._emea = EMEABrand()
        self._emea_ip = '80.90.194.0'
        self._gd = 'GoDaddy'
        self._123reg = '123REG'

    def test_is_hosted(self):
        self._emea._brands = [PlusServerBrand(), Reg123Brand()]
        hosted_dict = {'brand': None, 'ip': None, 'hosting_company_name': self._123reg, 'hosting_abuse_email': None}
        hosted_results = self._emea.is_hosted(hosted_dict)
        assert_true(hosted_results is True)

    def test_is_not_hosted(self):
        test_dict = {'brand': None, 'ip': None, 'hosting_company_name': self._gd, 'hosting_abuse_email': None}
        hosted_results = self._emea.is_hosted(test_dict)
        assert_true(hosted_results is False)

    def test_is_registered(self):
        reg_dict = {'brand': None, 'registrar_name': self._123reg, 'registrar_abuse_email': None, 'domain_create_date': None}
        reg_results = self._emea.is_registered(reg_dict)
        assert_true(reg_results is True)

    def test_is_not_registered(self):
        reg_dict = {'brand': None, 'registrar_name': self._gd, 'registrar_abuse_email': None, 'domain_create_date': None}
        reg_results = self._emea.is_registered(reg_dict)
        assert_true(reg_results is False)

    @patch.object(ASNPrefixes, '_query_ripe')
    def test_is_ip_in_range(self, _query_ripe):
        _query_ripe.return_value = {'data': {'prefixes': [{'prefix': self._emea_ip}]}}
        ip_emea = self._emea.is_ip_in_range(self._emea_ip)
        assert_true(ip_emea is True)

    @patch.object(ASNPrefixes, '_query_ripe')
    def test_is_not_in_range(self, _query_ripe):
        _query_ripe.return_value = {'data': {'prefixes': [{'prefix': self._emea_ip}]}}
        ip_not_emea = self._emea.is_ip_in_range('208.109.192.70')
        assert_true(ip_not_emea is False)
