from nose.tools import assert_true
from branddetection.domainhelper import DomainHelper


class TestDomainHelper:
    _gd_ip = '208.109.192.70'
    _gd_abuse_email = 'abuse@godaddy.com'
    _gd_domain = 'godaddy.com'
    _gd_llc = 'GO-DADDY-COM-LLC'
    _local_ip = '127.0.0.0'
    _test_domain = 'downwithtestingupwithstraighttoprod.com'  # downwithtestingupwithstraighttoprod.com not registered

    def __init__(self):
        self._DH = DomainHelper()

    def test_none_convert_domain_to_ip(self):
        no_source = self._DH.convert_domain_to_ip(None)
        assert_true(no_source is None)

    def test_empty_convert_domain_to_ip(self):
        no_source = self._DH.convert_domain_to_ip('')
        assert_true(no_source is None)

    def test_gd_empty_convert_domain_to_ip(self):
        domain = self._DH.convert_domain_to_ip(self._gd_domain)
        assert_true(domain == self._gd_ip)

    def test_ip_empty_convert_domain_to_ip(self):
        ip = self._DH.convert_domain_to_ip(self._gd_ip)
        assert_true(ip == self._gd_ip)

    def test_false_is_ip(self):
        domain = self._DH.is_ip('comicsn.beer')
        assert_true(domain is False)

    def test_true_is_ip(self):
        ip = self._DH.is_ip(self._gd_ip)
        assert_true(ip is True)

    def test_gd_get_ip_from_domain(self):
        domain = self._DH.get_ip_from_domain(self._gd_domain)
        assert_true(domain == self._gd_ip)

    def test_none_ip_from_domain(self):
        fp_domain = self._DH.get_ip_from_domain(self._test_domain)
        assert_true(fp_domain is None)

    def test_gd_get_domain_from_ip(self):
        domain = self._DH.get_domain_from_ip(self._gd_ip)
        assert_true(domain == 'ip-208-109-192-70.ip.secureserver.net')

    def test_none_domain_from_ip(self):
        domain2 = self._DH.get_domain_from_ip(self._local_ip)
        assert_true(domain2 is None)

    def test_gd_get_hosting_information_via_whois(self):
        query_value = self._DH.get_hosting_information_via_whois(self._gd_ip)
        ip = query_value['ip']
        org = query_value['hosting_company_name']
        email = query_value['hosting_abuse_email']
        assert_true(ip == self._gd_ip)
        assert_true(org == self._gd_llc)
        assert_true(email == [self._gd_abuse_email, 'noc@godaddy.com'])

    def test_none_get_hosting_information_via_whois(self):
        fp_value = self._DH.get_hosting_information_via_whois(self._local_ip)
        org = fp_value['hosting_company_name']
        assert_true(org is None)

    def test_gd_get_registrar_information_via_whois(self):
        gd_value = self._DH.get_registrar_information_via_whois(self._gd_domain)
        date = gd_value['domain_create_date']
        email = gd_value['registrar_abuse_email']
        registrar = gd_value['registrar_name']
        assert_true(date == '1999-03-02')

        # sometimes ['abuse@godaddy.com', 'companynames@godaddy.com'] or ['abuse@godaddy.com']
        assert_true(email == [self._gd_abuse_email] or [self._gd_abuse_email, 'companynames@godaddy.com'])
        assert_true(registrar == self._gd_llc)

    def test_none_get_registrar_information_via_whois(self):
        fp_value = self._DH.get_registrar_information_via_whois(self._test_domain)
        registrar = fp_value['registrar_name']
        assert_true(registrar is None)

