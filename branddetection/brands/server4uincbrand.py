import socket

from dcustructuredloggingflask.flasklogger import get_logging

from branddetection.asnhelper import ASNPrefixes
from branddetection.interfaces.brand import Brand


class Server4UIncBrand(Brand):
    """
    For determining whether a domain is hosted or registered with Server4You/Hosting Solutions International
    """
    NAME = 'SERVER4UINC'
    HOSTING_MATCHES = ['HOSTING SOLUTIONS INTERNATIONAL', 'SERVER4YOU', 'IP-POOL.COM', 'STARBAND.NET',
                       'SERVERPROFI24.COM', 'DEDICATEDPANEL.COM', 'STARTDEDICATED.COM',
                       'NAMESERVERSERVICE.COM']
    HOSTING_ABUSE_EMAIL = 'abuse@server4you.com'

    _asns = [30083, 55225]

    def __init__(self):
        self._logger = get_logging()
        self._asn = ASNPrefixes(self._asns)

    def is_hosted(self, whois_lookup):
        if isinstance(whois_lookup, dict):
            hostname = self.get_hostname_from_whois(whois_lookup) or ''
            for hosting_string in self.HOSTING_MATCHES:
                if hosting_string in hostname.upper():
                    return True
            # If we don't have a match, check whether Host lookup matches same pattern
            try:
                host_ip = whois_lookup.get('ip')
                host_result = socket.gethostbyaddr(host_ip)[0].upper()
                for hosting_string in self.HOSTING_MATCHES:
                    if hosting_string in host_result:
                        return True
            except Exception as e:
                self._logger.warning('Unknown host for {} : {}'.format(host_ip, e))
        return False

    def is_registered(self, whois_lookup):
        registrar = self.get_registrar_from_whois(whois_lookup)
        return registrar and self.NAME in registrar.upper()

    def is_ip_in_range(self, ip):
        return self._asn.get_network_for_ip(ip)
