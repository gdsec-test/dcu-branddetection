import logging

from branddetection.asnhelper import ASNPrefixes
from branddetection.interfaces.brand import Brand


class Server4UIncBrand(Brand):
    """
    Server4UInc specific brand for determining whether or not a domain is hosted or registered with Server4UInc
    """
    NAME = 'SERVER4UINC'
    _asns = [30083, 55225]

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._asn = ASNPrefixes(self._asns)

    def is_hosted(self, whois_lookup):
        return False

    def is_registered(self, domain):
        return False

    def is_ip_in_range(self, ip):
        return self._asn.get_network_for_ip(ip)
