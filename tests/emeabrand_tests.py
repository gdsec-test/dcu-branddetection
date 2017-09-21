from nose.tools import assert_true
from branddetection.brands.emeabrand import EMEABrand
from branddetection.asnhelper import ASNPrefixes
from mock import patch
from branddetection.brands.reg123brand import Reg123Brand


class TestEMEA:
    def __init__(self):
        pass

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def test_is_hosted(self, _ripe_get_prefixes_per_asn):
        emea = EMEABrand()
        _ripe_get_prefixes_per_asn.return_value = ['212.48.64.1']
        emea._brands = [Reg123Brand()]
        hosted_dict = {'brand': None, 'ip': None, 'hosting_company_name': '123REG', 'hosting_abuse_email': None}
        hosted_results = emea.is_hosted(hosted_dict)
        assert_true(hosted_results is True)

        test_dict = {'brand': None, 'ip': None, 'hosting_company_name': 'GoDaddy', 'hosting_abuse_email': None}
        hosted_results = emea.is_hosted(test_dict)
        assert_true(hosted_results is False)

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def test_is_registered(self, _ripe_get_prefixes_per_asn):
        emea = EMEABrand()
        _ripe_get_prefixes_per_asn.return_value = ['212.48.64.1']
        emea._brands = [Reg123Brand()]
        reg_dict = {'brand': None, 'registrar_name': '123REG', 'registrar_abuse_email': None, 'domain_create_date': None}
        reg_results = emea.is_registered(reg_dict)
        assert_true(reg_results is True)

        reg_dict = {'brand': None, 'registrar_name': 'GoDaddy', 'registrar_abuse_email': None, 'domain_create_date': None}
        reg_results = emea.is_registered(reg_dict)
        assert_true(reg_results is False)

    @patch.object(ASNPrefixes, '_ripe_get_prefixes_per_asn')
    def test_is_ip_in_range(self, _ripe_get_prefixes_per_asn):
        emea = EMEABrand()
        _ripe_get_prefixes_per_asn.return_value = ['80.90.194.0']
        emea._brands = [Reg123Brand()]
        ip_emea = emea.is_ip_in_range('80.90.194.0')
        assert_true(ip_emea is True)

        ip_not_emea = emea.is_ip_in_range('208.109.192.70')
        assert_true(ip_not_emea is False)
