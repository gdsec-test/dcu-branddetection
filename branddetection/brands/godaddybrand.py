import logging
import re

from branddetection.asnhelper import ASNPrefixes
from branddetection.domainhelper import DomainHelper
from branddetection.interfaces.brand import Brand


class GoDaddyBrand(Brand):
    """
    GoDaddy specific brand for determining whether or not a domain is hosted or registered with GoDaddy
    """
    NAME = 'GODADDY'
    HOSTING_COMPANY_NAME = 'GoDaddy.com LLC'
    HOSTING_ABUSE_EMAIL = 'abuse@godaddy.com'

    _asns = [26496]

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._asn = ASNPrefixes(self._asns)

    def is_hosted(self, whois_lookup):
        hostname = self.get_hostname_from_whois(whois_lookup)
        if hostname and self.NAME in hostname.upper():
            return True

        reverse_dns = DomainHelper.get_domain_from_ip(whois_lookup['ip'])
        if reverse_dns is not None and 'secureserver.net' in reverse_dns:
            self._logger.info("{} hosted info found in reverse dns".format(whois_lookup['ip']))
            return True
        return False

    def is_registered(self, whois_lookup):
        registrar = self.get_registrar_from_whois(whois_lookup)
        return registrar and re.search(r'(?:GODADDY|WILDWESTDOMAINS)', registrar.upper())

    def is_ip_in_range(self, ip):
        return self._asn.get_network_for_ip(ip)
