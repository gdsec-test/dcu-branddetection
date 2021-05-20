from dcustructuredloggingflask.flasklogger import get_logging

from branddetection.asnhelper import ASNPrefixes
from branddetection.interfaces.brand import Brand


class ParagonBrand(Brand):
    """
    Paragon specific brand for determining whether or not a domain is hosted or registered with Paragon
    """
    NAME = 'PARAGON'
    HOSTING_COMPANY_NAME = 'Paragon Internet Group Limited'
    HOSTING_ABUSE_EMAIL = 'abuse@paragon.net.uk'

    _asns = [133882, 198047]

    def __init__(self):
        self._logger = get_logging()
        self._asn = ASNPrefixes(self._asns)

    def is_hosted(self, whois_lookup):
        hostname = self.get_hostname_from_whois(whois_lookup)
        return hostname and self.NAME in hostname.upper()

    def is_registered(self, whois_lookup):
        registrar = self.get_registrar_from_whois(whois_lookup)
        return registrar and self.NAME in registrar.upper()

    def is_ip_in_range(self, ip):
        return self._asn.get_network_for_ip(ip)
