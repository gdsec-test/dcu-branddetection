from branddetection.asnhelper import ASNPrefixes
from branddetection.interfaces.brand import Brand


class Server4UIncBrand(Brand):
    """
    For determining whether a domain is hosted or registered with Server4You/Hosting Solutions International
    """
    NAME = 'SERVER4UINC'
    HOSTING_COMPANY_NAME = 'SERVER4UINC'
    HOSTING_MATCHES = ['HOSTING SOLUTIONS INTERNATIONAL', 'SERVER4YOU', 'IP-POOL.COM', 'STARBAND', 'SERVERPROFI24',
                       'DEDICATEDPANEL', 'STARTDEDICATED', 'NAMESERVERSERVICE', 'SERVERLOFT', 'VSERVER',
                       'SERVER01.COM', 'SERVER4FREE', 'NETFABRIK', 'ROUTESERVER']
    HOSTING_ABUSE_EMAIL = 'abuse@server4you.com'

    _asns = [30083, 55225]

    def __init__(self):
        self._asn = ASNPrefixes(self._asns)

    def is_hosted(self, whois_lookup):
        pass

    def is_registered(self, whois_lookup):
        registrar = self.get_registrar_from_whois(whois_lookup)
        return registrar and self.NAME in registrar.upper()

    def is_ip_in_range(self, ip):
        return self._asn.get_network_for_ip(ip)
