import logging

from branddetection.domainhelper import DomainHelper
from branddetection.brands.godaddybrand import GoDaddyBrand
from branddetection.brands.emeabrand import EMEABrand
from branddetection.interfaces.brand import ForeignBrand


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
        who_is = {}
        ip = self._domain_helper.convert_domain_to_ip(sourceDomainOrIp)

        # If a conversion from domain to ip fails, just return a foreign brand
        if ip is not None:
            brand = self._is_brand_in_known_ip_range(ip)
            if brand is None:
                who_is = self._determine_hosting_by_fallback(ip)
            else:
                who_is = {'brand': brand.NAME,
                         'hosting_company_name': brand.ORG_NAME,
                         'hosting_abuse_email': brand.ABUSE_EMAIL,
                         'ip': ip
                 }

        else:
            who_is = {'brand': None,
                     'hosting_company_name': None,
                     'hosting_abuse_email': None,
                     'ip': None
            }
        return who_is

    def get_registrar_info(self, sourceDomainOrIp):
        """
        Attempt to find the appropriate brand that sourceDomainOrIp is registered with
        :param sourceDomainOrIp:
        :return:
        """
        whois_lookup = self._domain_helper.retreive_registrar_information(sourceDomainOrIp)
        for brand in self._brands:
            if brand.is_registered(whois_lookup):
                self._logger.info("Successfully found a registrar: {} for domain/ip: {}"
                                  .format(brand.NAME, sourceDomainOrIp))
                whois_lookup['brand'] = brand.NAME
                return whois_lookup
        self._logger.info("Unable to find a registrar for domain/ip: {}".format(sourceDomainOrIp))
        whois_lookup['brand'] = ForeignBrand().NAME
        return whois_lookup

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
        whois_lookup = self._domain_helper.retrieve_hosting_information_via_whois(ip)
        if whois_lookup is not None:
            for brand in self._brands:
                if brand.is_hosted(whois_lookup):
                    self._logger.info("Brand found by using a fallback method: {}".format(brand.NAME))
                    whois_lookup['brand'] = brand.NAME
                    return whois_lookup
        whois_lookup['brand'] = ForeignBrand().NAME
        return whois_lookup

