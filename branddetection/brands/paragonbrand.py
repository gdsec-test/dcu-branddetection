from branddetection.asnhelper import ASNPrefixes
from branddetection.interfaces.brand import Brand


class ParagonBrand(Brand):
    """
    Paragon specific brand for determining whether or not a domain is hosted or registered with Paragon
    """
    NAME = 'PARAGON'
    HOSTING_COMPANY_NAME = 'Paragon Internet Group Limited'
    HOSTING_MATCHES = ['PARAGON', 'PARAGON INTERNET GROUP LIMITED', 'PRGN.MISP.CO.UK']
    HOSTING_ABUSE_EMAIL = 'abuse@tsohost.com'

    _asns = [133882, 198047]

    def __init__(self):
        self._asn = ASNPrefixes(self._asns)

    def is_hosted(self, whois_lookup):
        pass

    def is_registered(self, whois_lookup):
        registrar = self.get_registrar_from_whois(whois_lookup)
        return registrar and self.NAME in registrar.upper()

    def is_ip_in_range(self, ip):
        return self._asn.get_network_for_ip(ip)
