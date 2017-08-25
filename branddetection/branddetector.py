import logging

from branddetection.domainhelper import DomainHelper
from branddetection.brands.godaddybrand import GoDaddyBrand
from branddetection.brands.emeabrand import EMEABrand


class BrandDetector:

    def __init__(self, settings):
        self._logger = logging.getLogger(__name__)
        self._domain_helper = DomainHelper(settings)

        # self._brands = [GoDaddyBrand(), EMEABrand()]
        self._brands = [GoDaddyBrand()]

    def get_hosting_info(self, sourceDomainOrIp):
        """
        Attempt to find the appropriate brand that sourceDomainOrIp is hosted with
        :param sourceDomainOrIp:
        :return:
        """
        ip = self._domain_helper.convert_domain_to_ip(sourceDomainOrIp)

        # If a conversion from domain to ip fails, just return a foreign brand
        if ip is not None:
            redis_record_key = u'{}-hosting_whois_info'.format(ip)
            whois_lookup = self._domain_helper.get_whois_info_from_cache(redis_record_key)

            if whois_lookup is None:
                whois_lookup = self._get_hosting_in_known_ip_range(ip)
                if whois_lookup is None:
                    whois_lookup = self._get_hosting_by_fallback(ip)
                if whois_lookup:
                    self._domain_helper.add_whois_info_to_cache(redis_record_key, whois_lookup)
        else:
            whois_lookup = {'brand': None, 'hosting_company_name': None, 'hosting_abuse_email': None, 'ip': None}
        return whois_lookup

    def get_registrar_info(self, domain):
        """
        Attempt to find the appropriate brand that sourceDomainOrIp is registered with
        :param domain:
        :return:
        """
        whois_lookup = self._domain_helper.get_registrar_information_via_whois(domain)
        for brand in self._brands:
            if brand.is_registered(whois_lookup):
                self._logger.info("Successfully found a registrar: {} for domain/ip: {}"
                                  .format(brand.NAME, domain))
                whois_lookup['brand'] = brand.NAME
                return whois_lookup
        self._logger.info("Unable to find a matching registrar for domain/ip: {}. Brand is FOREIGN".format(domain))
        whois_lookup['brand'] = "FOREIGN"
        return whois_lookup

    def _get_hosting_in_known_ip_range(self, ip):
        """
        Attempt to determine whether a given ip is known by any of the brands
        :param ip:
        :return:
        """
        for brand in self._brands:
            if brand.is_ip_in_range(ip):
                self._logger.info("Successfully found a hosting provider: {} for domain/ip: {}".format(brand.NAME, ip))
                return {'brand': brand.NAME, 'hosting_company_name': brand.ORG_NAME[0], 'ip': ip,
                                'hosting_abuse_email': [brand.ABUSE_EMAIL[0]]}
        return None

    def _get_hosting_by_fallback(self, ip):
        """
        If unable to determine hosting via ip lookup, fall back and use each brand's own way of determining hosting
        :param ip:
        :return:
        """
        whois_lookup = self._domain_helper.get_hosting_information_via_whois(ip)
        for brand in self._brands:
            if brand.is_hosted(whois_lookup):
                self._logger.info("Successfully found a hosting provider using fallback method: {} for domain/ip: {}"
                                  .format(brand.NAME, ip))
                whois_lookup['brand'] = brand.NAME
                return whois_lookup
        self._logger.info("Unable to find a matching hosting provider for domain/ip: {}. Brand is FOREIGN.".format(ip))
        whois_lookup['brand'] = "FOREIGN"
        return whois_lookup

