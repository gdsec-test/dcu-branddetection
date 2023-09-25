from branddetection.asnhelper import ASNPrefixes
from branddetection.interfaces.brand import Brand


class VeliaBrand(Brand):
    """
    Velia specific brand for determining whether or not a domain is hosted or registered with Velia
    """
    NAME = 'VELIA'
    HOSTING_COMPANY_NAME = 'Velia.net Internetdienste GmbH'
    HOSTING_MATCHES = ['VELIA', 'VELIA.NET INTERNETDIENSTE GMBH', 'PROTONINTERNET']
    HOSTING_ABUSE_EMAIL = 'abuse@velia.net'
    PLID = '541136'

    _asns = [29066]

    def __init__(self):
        self._asn = ASNPrefixes(self._asns)

    def is_hosted(self, whois_lookup):
        pass

    def is_registered(self, whois_lookup):
        registrar = self.get_registrar_from_whois(whois_lookup)
        return registrar and self.NAME in registrar.upper()

    def is_ip_in_range(self, ip):
        return self._asn.get_network_for_ip(ip)
