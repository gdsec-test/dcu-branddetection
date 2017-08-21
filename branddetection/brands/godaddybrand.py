import logging

from branddetection.interfaces.brand import Brand
from branddetection.asnhelper import ASNPrefixes
from branddetection.domainhelper import DomainHelper


class GoDaddyBrand(Brand):
    """
    GoDaddy specific brand for determining whether or not a domain is hosted or registered with GoDaddy
    """
    NAME = 'GODADDY'
    ORG_NAME = 'GoDaddy.com LLC'
    ABUSE_EMAIL = ['abuse@godaddy.com']

    _asns = [26496]

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._asn = ASNPrefixes(self._asns)

    def is_hosted(self, whois_lookup):
        """
        Check the ip address against the asn announced prefixes then check
        the reverse dns for secureserver.net
        """
        if Brand.determine_hosting_brand_from_whois(self, whois_lookup, self.ABUSE_EMAIL, self.ORG_NAME):
            return True

        reverse_dns = DomainHelper.get_domain_from_ip(whois_lookup['ip'])
        if reverse_dns is not None and 'secureserver.net' in reverse_dns:
            self._logger.info("{} hosted info found in reverse dns".format(whois_lookup['ip']))
            return True
        return False

    def is_registered(self, whois_lookup):
        return Brand.determine_registrar_from_whois(self, whois_lookup, self.ABUSE_EMAIL, self.ORG_NAME)

    def is_ip_in_range(self, ip):
        return self._asn.get_network_for_ip(ip)
