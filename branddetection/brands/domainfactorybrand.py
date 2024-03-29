from branddetection.asnhelper import ASNPrefixes
from branddetection.interfaces.brand import Brand


class DomainFactoryBrand(Brand):
    """
    DomainFactory specific brand for determining whether or not a domain is hosted or registered with DomainFactory
    """
    NAME = 'DOMAINFACTORY'
    HOSTING_COMPANY_NAME = 'DomainFactory GmbH'
    HOSTING_MATCHES = ['DOMAINFACTORY', 'DOMAINFACTORY GMBH', 'ISPGATEWAY', 'DF.EU', 'JIFFYBOX', 'JIFFYBOXSERVERS']
    HOSTING_ABUSE_EMAIL = 'abuse@domainfactory.de'
    PLID = '525845'

    # AS34011 currently has no originating prefixes
    _asns = [34011]

    def __init__(self):
        self._asn = ASNPrefixes(self._asns)

    def is_hosted(self, whois_lookup):
        pass

    def is_registered(self, whois_lookup):
        registrar = self.get_registrar_from_whois(whois_lookup)
        return registrar and self.NAME in registrar.upper()

    def is_ip_in_range(self, ip):
        return self._asn.get_network_for_ip(ip)
