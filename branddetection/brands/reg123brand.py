import logging
import re

from branddetection.asnhelper import ASNPrefixes
from branddetection.interfaces.brand import Brand


class Reg123Brand(Brand):
    """
    123Reg specific brand for determining whether or not a domain is hosted or registered with 123Reg. This brand also
    encapsulates WebFusion.
    """
    NAME = '123REG'
    HOSTING_COMPANY_NAME = 'Host Europe GmbH'
    HOSTING_ABUSE_EMAIL = 'abuse@123-reg.co.uk'

    _asns = [20738]

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._asn = ASNPrefixes(self._asns)

    def is_hosted(self, whois_lookup):
        hostname = self.get_hostname_from_whois(whois_lookup)
        return hostname and re.search(r'(?:123REG|WEBFUSION)', hostname.upper())

    def is_registered(self, whois_lookup):
        registrar = self.get_registrar_from_whois(whois_lookup)
        return registrar and re.search(r'(?:123REG|WEBFUSION)', registrar.upper())

    def is_ip_in_range(self, ip):
        return self._asn.get_network_for_ip(ip)
