from branddetection.asnhelper import ASNPrefixes
from branddetection.interfaces.brand import Brand


class HeartInternetBrand(Brand):
    """
    HeartInternet specific brand for determining whether or not a domain is hosted or registered with HeartInternet
    """
    NAME = 'HEARTINTERNET'
    HOSTING_COMPANY_NAME = 'Heart Internet Ltd'
    HOSTING_MATCHES = ['HEARTINTERNET', 'HEART INTERNET', 'VPS-10', 'DS-10', 'EXTENDCP', 'EXTENDNET']
    HOSTING_ABUSE_EMAIL = 'abuse@heartinternet.co.uk'

    # AS43788 currently has no originating prefixes
    _asns = [43788]

    def __init__(self):
        self._asn = ASNPrefixes(self._asns)

    def is_hosted(self, whois_lookup):
        pass

    def is_registered(self, whois_lookup):
        registrar = self.get_registrar_from_whois(whois_lookup)
        return registrar and self.NAME in registrar.upper()

    def is_ip_in_range(self, ip):
        return self._asn.get_network_for_ip(ip)
