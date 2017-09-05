from nose.tools import assert_true
from branddetection.domainhelper import DomainHelper


class TestCmapServiceHelper:
    def __init__(self):
        self._DH = DomainHelper()

    def test_convert_domain_to_ip(self):
        no_source = self._DH.convert_domain_to_ip(None)
        assert_true(no_source is None)

        domain = self._DH.convert_domain_to_ip('comicsn.beer')
        assert_true(domain == '160.153.77.227')

        ip = self._DH.convert_domain_to_ip('160.153.77.227')
        assert_true(ip == '160.153.77.227')

    def test_is_ip(self):
        domain = self._DH.is_ip('comicsn.beer')
        assert_true(domain is False)

        domain = self._DH.is_ip('160.153.77.227')
        assert_true(domain is True)

    def test_get_ip_from_domain(self):
        pass

    def test_get_domain_from_ip(self):
        pass

    def test_get_hosting_information_via_whois(self):
        pass

    def test_get_registrar_information_via_whois(self):
        pass
