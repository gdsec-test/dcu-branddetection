import datetime
from unittest import TestCase

import dns.rdtypes.IN.A as mock_dns
from dns import resolver
from ipwhois.ipwhois import IPWhois
from mock import patch
from whois.parser import WhoisCom

from branddetection.domainhelper import DomainHelper


class MockDNSResolver(mock_dns.A):
    address = '0.0.0.0'


class MockDNSResolver1():
    text = b'ip-0-0-0-0.ip.secureserver.net'

    def to_text(self):
        return self.text.decode('utf-8')


class MockWhoisResponse(WhoisCom):
    registrar = 'GoDaddy.com, LLC'
    emails = ''

    def __init__(self, reg=None):
        super().__init__('', '')
        if reg is not None:
            self.registrar = None

        self.creation_date = datetime.datetime.strptime('1999-03-02', '%Y-%m-%d')


class TestDomainHelper(TestCase):
    _gd_ip = '0.0.0.0'
    _gd_abuse_email = 'abuse@godaddy.com'
    _gd_domain = 'godaddy.com'
    _gd_llc = 'GO-DADDY-COM-LLC'
    _gd_noc_email = 'noc@godaddy.com'
    _intl_domain = 'Bücher.example'
    _local_ip = '127.0.0.0'
    _random = 'a;sdlkj'
    _random_bytes = b'a;sdlkj'
    _rdap_ip = '192.186.254.8'
    _rdap_dict = {
        'network': {'name': _gd_llc},
        'hosting_company_name': _gd_llc,
        'hosting_abuse_email': _gd_abuse_email,
        'objects': {
            'GODAD': {
                'contact': {
                    'email': [
                        {
                            'type': None,
                            'value': _gd_abuse_email
                        }
                    ]
                }
            },
            'NOC124-ARIN': {
                'contact': {
                    'email': [
                        {
                            'type': None,
                            'value': _gd_noc_email
                        }
                    ]
                }
            }
        }
    }

    def setUp(self):
        self._DH = DomainHelper()

    def test_none_convert_domain_to_ip(self):
        no_source = self._DH.convert_domain_to_ip(None)
        self.assertIsNone(no_source)

    @patch.object(resolver.Resolver, 'query', return_value=[MockDNSResolver])
    def test_convert_intl_domain_to_ip(self, get_ip):
        domain = self._DH.convert_domain_to_ip(self._intl_domain)
        self.assertEqual(domain, self._gd_ip)

    @patch.object(resolver.Resolver, 'query', return_value=[MockDNSResolver])
    def test_convert_domain_to_ip(self, get_ip):
        domain = self._DH.convert_domain_to_ip(self._gd_domain)
        self.assertEqual(domain, self._gd_ip)

    def test_ip_empty_convert_domain_to_ip(self):
        ip = self._DH.convert_domain_to_ip('')
        self.assertIsNone(ip)

    def test_str_ip_convert_domain_to_ip(self):
        ip = self._DH.convert_domain_to_ip(self._gd_ip)
        self.assertEqual(ip, self._gd_ip)

    def test_false_is_ip(self):
        domain = self._DH.is_ip('comicsn.beer')
        self.assertFalse(domain)

    def test_is_ip_string_ip(self):
        ip = self._DH.is_ip(self._gd_ip)
        self.assertTrue(ip)

    def test_is_ip_string_random(self):
        ip = self._DH.is_ip(self._random)
        self.assertFalse(ip)

    def test_is_ip_bytes_random(self):
        ip = self._DH.is_ip(self._random_bytes)
        self.assertFalse(ip)

    def test_is_not_ip_secureserverip(self):
        ip = self._DH.is_ip("120.136.206.88.host.secureserver.net")
        self.assertFalse(ip)

    def test_is_ipv6_regular(self):
        ip = self._DH.is_ip("2001:db8:3333:4444:5555:6666:7777:8888")
        self.assertTrue(ip)

    def test_is_ip_regular(self):
        ip = self._DH.is_ip("120.136.206.88")
        self.assertTrue(ip)

    def test_is_domain_not_ip(self):
        ip = self._DH.is_ip("http://www.abc.com")
        self.assertFalse(ip)

    @patch.object(resolver.Resolver, 'query', return_value=[MockDNSResolver1()])
    @patch('branddetection.domainhelper.reversename.from_address', return_value='0.0.0.0.in-addr.arpa.')
    def test_gd_get_domain_from_ip(self, get_reverse_name, get_byte_string):
        ip = self._DH.get_domain_from_ip(self._gd_ip)
        self.assertEqual(ip, 'ip-0-0-0-0.ip.secureserver.net')

    def test_none_domain_from_ip(self):
        domain = self._DH.get_domain_from_ip(self._local_ip)
        self.assertTrue(domain is None or domain == 'localhost')

    @patch('branddetection.domainhelper.whois', return_value=MockWhoisResponse())
    @patch.object(IPWhois, 'lookup_rdap', return_value=_rdap_dict)
    def test_gd_get_hosting_information_via_whois(self, get_rdap, get_whois):
        query_value = self._DH.get_hosting_information_via_whois(self._rdap_ip)
        ip = query_value['ip']
        org = query_value['hosting_company_name']
        email = query_value['hosting_abuse_email']
        self.assertEqual(ip, self._rdap_ip)
        self.assertEqual(org, self._gd_llc)
        self.assertEqual(email, [self._gd_abuse_email, self._gd_noc_email])

    @patch('branddetection.domainhelper.whois', return_value=MockWhoisResponse())
    def test_none_get_hosting_information_via_whois(self, get_whois):
        fp_value = self._DH.get_hosting_information_via_whois(self._local_ip)
        org = fp_value['hosting_company_name']
        self.assertIsNone(org)

    @patch('branddetection.domainhelper.whois', return_value=MockWhoisResponse())
    def test_gd_get_registrar_information_via_whois(self, get_whois):
        gd_value = self._DH.get_registrar_information_via_whois(self._gd_domain)
        date = gd_value['domain_create_date']
        email = gd_value['registrar_abuse_email']
        registrar = gd_value['registrar_name']
        self.assertTrue(date == '1999-03-02')

        # sometimes ['abuse@godaddy.com', 'companynames@godaddy.com'] or ['abuse@godaddy.com']
        self.assertTrue(email == [self._gd_abuse_email] or [self._gd_abuse_email, 'companynames@godaddy.com'])

        # sometimes GoDaddy.com, LLC, or 'GO-DADDY-COM-LLC'
        self.assertTrue(registrar == self._gd_llc or registrar == 'GoDaddy.com, LLC')

    @patch('branddetection.domainhelper.whois', return_value=MockWhoisResponse(''))
    def test_none_get_registrar_information_via_whois(self, get_whois):
        fp_value = self._DH.get_registrar_information_via_whois(self._gd_domain)
        registrar = fp_value['registrar_name']
        self.assertIsNone(registrar)
