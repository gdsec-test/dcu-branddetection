import logging

from branddetection.asnhelper import ASNPrefixes
from branddetection.interfaces.brand import Brand


class VeliaBrand(Brand):
    """
    Velia specific brand for determining whether or not a domain is hosted or registered with Velia
    """
    NAME = 'VELIA'
    HOSTING_COMPANY_NAME = ''
    HOSTING_ABUSE_EMAIL = 'abuse@velia.net'

    _asns = [29066]

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._asn = ASNPrefixes(self._asns)

    def is_hosted(self, whois_lookup):
        hostname = self.get_hostname_from_whois(whois_lookup)
        return hostname and self.NAME in hostname.upper()

    def is_registered(self, whois_lookup):
        registrar = self.get_registrar_from_whois(whois_lookup)
        return registrar and self.NAME in registrar.upper()

    def is_ip_in_range(self, ip):
        return self._asn.get_network_for_ip(ip)
