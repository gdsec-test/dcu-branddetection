import logging

from branddetection.domainhelper import DomainHelper
from branddetection.brands.godaddybrand import GoDaddyBrand
from branddetection.brands.emeabrand import EMEABrand


class BrandDetector:

    def __init__(self, settings):
        self._logger = logging.getLogger(__name__)
        self._brands = [GoDaddyBrand(), EMEABrand()]
        self._helper = DomainHelper()

    def find_hosting(self, sourceDomainOrIp):
        """
        Attempt to find the appropriate brand that sourceDomainOrIp is hosted with
        :param sourceDomainOrIp:
        :return:
        """

        brand = None
        ip = sourceDomainOrIp
        if self._helper.is_ip(sourceDomainOrIp) is None:
            ip = self._helper.get_ip_from_domain(sourceDomainOrIp)

        # brand = self._is_brand_in_known_ip_range(ip)
        # if brand is None:
        #     whois = self._helper.whois_lookup(sourceDomainOrIp)
        #     if whois:
        #         for brand in self._brands:
        #             if brand.is_hosted(whois):
        #                 return brand
        return brand

    def find_registrar(self, sourceDomainOrIp):
        """
        Attempt to find the appropriate brand that sourceDomainOrIp is registered with
        :param sourceDomainOrIp:
        :return:
        """
        for brand in self._brands:
            if brand.is_registered(sourceDomainOrIp):
                self._logger.info("Successfully found a registrar: {} for domain/ip: {}".format(brand, sourceDomainOrIp))
                return brand.NAME
        self._logger.info("Unable to find a registrar for domain/ip: {}".format(sourceDomainOrIp))
        return None

    def _is_brand_in_known_ip_range(self, ip):
        """
        Attempt to determine whether a given ip is known by any of the brands
        :param ip:
        :return:
        """
        for brand in self._brands:
            if brand.is_ip_in_range(ip):
                return brand.NAME
        return None
