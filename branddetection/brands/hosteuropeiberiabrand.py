from branddetection.asnhelper import ASNPrefixes
from branddetection.interfaces.brand import Brand


class HostEuropeIberia(Brand):
    """
    HostEuropeIberia specific brand for determining whether or not a domain is hosted or registered with HostEuropeIberia
    """
    NAME = 'HOSTEUROPEIBERIA'
    HOSTING_COMPANY_NAME = 'Host Europe Iberia SL'
    HOSTING_MATCHES = ['HOSTEUROPEIBERIA', 'HOST EUROPE IBERIA SL']
    HOSTING_ABUSE_EMAIL = 'abuse@hosteurope.es'

    # AS44497 currently has no originating prefixes
    _asns = [44497]

    def __init__(self):
        self._asn = ASNPrefixes(self._asns)

    def is_hosted(self, whois_lookup):
        pass

    def is_registered(self, whois_lookup):
        registrar = self.get_registrar_from_whois(whois_lookup)
        return registrar and self.NAME in registrar.upper()

    def is_ip_in_range(self, ip):
        return self._asn.get_network_for_ip(ip)
