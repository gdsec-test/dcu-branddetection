import logging
import re

from branddetection.asnhelper import ASNPrefixes
from branddetection.interfaces.brand import Brand


class PlusServerBrand(Brand):
    """
    PlusServer specific brand for determining whether or not a domain is hosted or registered with PlusServer.
    This brand also encapsulates MainLab, Mesh DE.
    """
    NAME = 'PLUSSERVER'
    HOSTING_COMPANY_NAME = 'PlusServer AG'
    HOSTING_ABUSE_EMAIL = 'abuse@plusserver.de'

    _asns = [25074]

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._asn = ASNPrefixes(self._asns)

    def is_hosted(self, whois_lookup):
        hostname = self.get_hostname_from_whois(whois_lookup)
        return hostname and re.search(r'(?:MAINLAB|MESHDE|PLUSSERVER)', hostname.upper())

    def is_registered(self, whois_lookup):
        registrar = self.get_registrar_from_whois(whois_lookup)
        return registrar and re.search(r'(?:MAINLAB|MESHDE|PLUSSERVER)', registrar.upper())

    def is_ip_in_range(self, ip):
        return self._asn.get_network_for_ip(ip)
