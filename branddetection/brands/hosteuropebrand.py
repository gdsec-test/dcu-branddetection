from branddetection.asnhelper import ASNPrefixes
from branddetection.interfaces.brand import Brand


class HostEuropeBrand(Brand):
    """
    HostEuropeBrand specific brand for determining whether or not a domain is hosted or registered with HostEuropeBrand
    """
    NAME = 'HOSTEUROPE'
    HOSTING_COMPANY_NAME = 'Host Europe GmbH'
    HOSTING_MATCHES = ['HOSTEUROPE', 'HOST EUROPE GMBH', 'HOSTEUROPEIBERIA']
    HOSTING_ABUSE_EMAIL = 'abuse@hosteurope.de'
    PLID = '525847'
    _asns = [20773]

    def __init__(self):
        self._asn = ASNPrefixes(self._asns)

    def is_hosted(self, whois_lookup):
        pass

    def is_registered(self, whois_lookup):
        registrar = self.get_registrar_from_whois(whois_lookup)
        return registrar and self.NAME in registrar.upper() and 'HOSTEUROPEIBERIA' not in registrar.upper()

    def is_ip_in_range(self, ip):
        return self._asn.get_network_for_ip(ip)
