import logging

from branddetection.asnhelper import ASNPrefixes
from branddetection.interfaces.brand import Brand


class LoomesBrand(Brand):
    """
    LoomesBrand specific brand for determining whether or not a domain is hosted or registered with LoomesBrand
    """
    NAME = 'LOOMES'
    ORG_NAME = ['']
    ABUSE_EMAIL = ['abuse@loomes.de', 'behoerden@server4you.de']

    _asns = [8972, 20773]

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._asn = ASNPrefixes(self._asns)

    def is_hosted(self, whois_lookup):
        return Brand.determine_hosting_brand_from_whois(self, whois_lookup, self.ABUSE_EMAIL, self.ORG_NAME)

    def is_registered(self, whois_lookup):
        return Brand.determine_registrar_from_whois(self, whois_lookup, self.ABUSE_EMAIL, self.ORG_NAME)

    def is_ip_in_range(self, ip):
        return self._asn.get_network_for_ip(ip)
