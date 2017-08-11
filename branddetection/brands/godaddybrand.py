import logging

from branddetection.interfaces.brand import Brand
from branddetection.asnhelper import ASNPrefixes
from branddetection.domainhelper import DomainHelper


class GoDaddyBrand(Brand):
    """
    GoDaddy specific brand for determining whether or not a domain is hosted or registered with GoDaddy
    """
    NAME = 'GODADDY'
    _asns = [26496]

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._asn = ASNPrefixes(self._asns)

    def is_hosted(self, ip):
        """
        Check the ip address against the asn announced prefixes then check
        the reverse dns for secureserver.net
        """
        if self._asn.get_network_for_ip(ip):
            self._logger.info("{} hosted info found in advertised prefixes".format(ip))
            return True
        else:
            # Not sure if this will ever return true if the above is False
            reverse_dns = DomainHelper.get_domain_from_ip(ip)
            if reverse_dns is not None and 'secureserver.net' in reverse_dns:
                self._logger.info("{} hosted info found in reverse dns".format(ip))
                return True
            return False

    def is_registered(self, domain):
        return False

    def is_ip_in_range(self, ip):
        return self._asn.get_network_for_ip(ip)
