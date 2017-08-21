import logging

from branddetection.domainhelper import DomainHelper
from branddetection.brands.godaddybrand import GoDaddyBrand
from branddetection.brands.emeabrand import EMEABrand
from branddetection.interfaces.brand import ForeignBrand


class BrandDetector:

    def __init__(self, settings):
        self._logger = logging.getLogger(__name__)
        #self._brands = [GoDaddyBrand(), EMEABrand()]
        self._brands = [GoDaddyBrand()]

    def find_hosting(self, sourceDomainOrIp):
        """
        Attempt to find the appropriate brand that sourceDomainOrIp is hosted with
        :param sourceDomainOrIp:
        :return:
        """
        ip = DomainHelper.convert_domain_to_ip(sourceDomainOrIp)

        brand = self._is_brand_in_known_ip_range(ip)
        if brand is None:
            brand = self._determine_hosting_by_fallback(ip)
        return brand.NAME

    def find_registrar(self, sourceDomainOrIp):
        """
        Attempt to find the appropriate brand that sourceDomainOrIp is registered with
        :param sourceDomainOrIp:
        :return:
        """
        whois_lookup = DomainHelper.retreive_registrar_information(sourceDomainOrIp)
        for brand in self._brands:
            if brand.is_registered(whois_lookup):
                self._logger.info("Successfully found a registrar: {} for domain/ip: {}".format(brand, sourceDomainOrIp))
                return brand.NAME
        self._logger.info("Unable to find a registrar for domain/ip: {}".format(sourceDomainOrIp))
        return ForeignBrand().NAME

    def _is_brand_in_known_ip_range(self, ip):
        """
        Attempt to determine whether a given ip is known by any of the brands
        :param ip:
        :return:
        """
        for brand in self._brands:
            if brand.is_ip_in_range(ip):
                self._logger.info("Brand found by examining IP ranges: {}".format(brand.NAME))
                return brand
        return None

    def _determine_hosting_by_fallback(self, ip):
        """
        If unable to determine hosting via ip lookup, fall back and use each brand's own way of determining hosting
        :param ip:
        :return:
        """
        whois_lookup = DomainHelper.retrieve_hosting_information_via_whois(ip)
        for brand in self._brands:
            if brand.is_hosted(whois_lookup):
                self._logger.info("Brand found by using a fallback method: {}".format(brand.NAME))
                return brand
        return ForeignBrand()

