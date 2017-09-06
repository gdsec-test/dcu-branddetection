from nose.tools import assert_true, assert_false
from branddetection.domainhelper import DomainHelper


class TestCmapServiceHelper:
    def __init__(self):
        self._DH = DomainHelper()

    def test_convert_domain_to_ip(self):
        no_source = self._DH.convert_domain_to_ip(None)
        assert_true(no_source is None)

        domain = self._DH.convert_domain_to_ip('godaddy.com')
        assert_true(domain == '208.109.192.70')

        ip = self._DH.convert_domain_to_ip('208.109.192.70')
        assert_true(ip == '208.109.192.70')

    def test_is_ip(self):
        domain = self._DH.is_ip('comicsn.beer')
        assert_true(domain is False)

        domain = self._DH.is_ip('208.109.192.70')
        assert_true(domain is True)

    def test_get_ip_from_domain(self):
        ip = self._DH.get_ip_from_domain('godaddy.com')
        assert_true(ip == '208.109.192.70')

        # downwithtestingupwithstraighttoprod.com not registered
        ip = self._DH.get_ip_from_domain('downwithtestingupwithstraighttoprod.com')
        assert_false(ip == '92.242.140.2')

    def test_get_domain_from_ip(self):
        domain = self._DH.get_domain_from_ip('208.109.192.70')
        assert_true(domain == 'ip-208-109-192-70.ip.secureserver.net')

        domain2 = self._DH.get_domain_from_ip('127.0.0.0')
        assert_true(domain2 is None)

    def test_get_hosting_information_via_whois(self):
        query_value = self._DH.get_hosting_information_via_whois('208.109.192.70')
        ip = query_value['ip']
        org = query_value['hosting_company_name']
        email = query_value['hosting_abuse_email']
        assert_true(ip == '208.109.192.70')
        assert_true(org == 'GO-DADDY-COM-LLC')
        assert_true(email == ['abuse@godaddy.com', 'noc@godaddy.com'])

        fp_value = self._DH.get_hosting_information_via_whois('127.0.0.0')
        org = fp_value['hosting_company_name']
        assert_true(org is None)

    def test_get_registrar_information_via_whois(self):
        gd_value = self._DH.get_registrar_information_via_whois('godaddy.com')
        date = gd_value['domain_create_date']
        email = gd_value['registrar_abuse_email']
        registrar = gd_value['registrar_name']
        assert_true(date == '1999-03-02')
        assert_true(email == ['abuse@godaddy.com'])
        assert_true(registrar == 'GoDaddy.com, LLC')

        fp_value = self._DH.get_registrar_information_via_whois('downwithtestingupwithstraighttoprod.com')
        registrar = fp_value['registrar_name']
        assert_true(registrar is None)

