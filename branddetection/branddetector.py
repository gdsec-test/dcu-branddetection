import logging


from ipwhois import IPWhois
from whois import NICClient, whois
from whois.parser import PywhoisError, WhoisEntry

from datetime import datetime

from branddetection.domainhelper import DomainHelper
from branddetection.brands.godaddybrand import GoDaddyBrand
from branddetection.brands.emeabrand import EMEABrand
from branddetection.interfaces.brand import ForeignBrand


class BrandDetector:

    def __init__(self, settings):
        self._logger = logging.getLogger(__name__)
        #self._brands = [GoDaddyBrand(), EMEABrand()]
        self._brands = [GoDaddyBrand()]
        self._helper = DomainHelper()

    def find_hosting(self, sourceDomainOrIp):
        """
        Attempt to find the appropriate brand that sourceDomainOrIp is hosted with
        :param sourceDomainOrIp:
        :return:
        """
        if sourceDomainOrIp is None or sourceDomainOrIp == '':
            return None
        if sourceDomainOrIp is not str:
            sourceDomainOrIp = sourceDomainOrIp.encode('idna')
        if DomainHelper.is_ip(sourceDomainOrIp):
            ip = sourceDomainOrIp
        else:
            ip = DomainHelper.get_ip_from_domain(sourceDomainOrIp)

        brand = self._is_brand_in_known_ip_range(ip)

        if brand is None:
            brand = self._deterime_hosting_by_fallback(ip)
        return brand.NAME

    def _deterime_hosting_by_fallback(self, ip):
        for brand in self._brands:
            if brand.is_hosted(ip):
                self._logger.info("Brand found by using a fallback method: {}".format(brand.NAME))
                return brand.NAME
        return ForeignBrand()

    def find_registrar(self, sourceDomainOrIp):
        """
        Attempt to find the appropriate brand that sourceDomainOrIp is registered with
        :param sourceDomainOrIp:
        :return:
        """
        return self._retreive_registrar_information(sourceDomainOrIp)
        # for brand in self._brands:
        #     if brand.is_registered(sourceDomainOrIp):
        #         self._logger.info("Successfully found a registrar: {} for domain/ip: {}".format(brand, sourceDomainOrIp))
        #         return brand.NAME
        # self._logger.info("Unable to find a registrar for domain/ip: {}".format(sourceDomainOrIp))
        # return None

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

    def _retrieve_hosting_information_via_whois(self, ip):
        """
        Return hosting network company name, the ip queried, and any relevant hosting abuse emails.
        :param ip:
        :return:
        """
        COMPANY_NAME_KEY = 'hosting_company_name'
        ABUSE_EMAIL_KEY = 'hosting_abuse_email'
        IP_KEY = 'ip'
        query_value = {}

        try:
            query_value[IP_KEY] = ip
            email_list = []
            info = IPWhois(ip).lookup_rdap()
            query_value[COMPANY_NAME_KEY] = info.get('network').get('name')

            for k, v in info['objects'].iteritems():
                email_address = v['contact']['email']
                if email_address:
                    for i in email_address:
                        email_list.append(i['value'])
            query_value[ABUSE_EMAIL_KEY] = email_list
        except Exception as e:
            self._logger.error("Error retrieving hosting information: {}".format(e.message))
            query_value = {IP_KEY: None, COMPANY_NAME_KEY: None, ABUSE_EMAIL_KEY: None}
        return query_value

    def _retreive_registrar_information(self, ip):
        GODADDY_NAME = 'GoDaddy.com LLC'
        GODADDY_ABUSE_EMAIL = 'abuse@godaddy.com'

        REGISTRAR_NAME_KEY = 'registrar_name'
        ABUSE_EMAIL_KEY = 'registrar_abuse_email'
        DOMAIN_CREATE_DATE_KEY = 'domain_create_date'

        query_value = {}

        try:
            query = WhoisEntry.load(ip, NICClient().whois(ip, 'whois.godaddy.com', True))
            if query.registrar:
                query.registrar = GODADDY_NAME
                query.emails = [GODADDY_ABUSE_EMAIL]
            else:
                query = whois(ip)
                if isinstance(query.emails, basestring):
                    query.emails = [query.emails]

            query_value[REGISTRAR_NAME_KEY] = query.registrar
            query_value[ABUSE_EMAIL_KEY] = query.emails

            domain_create_date = query.creation_date[0] if isinstance(query.creation_date, list) \
                else query.creation_date
            domain_create_date = domain_create_date.strftime("%Y-%m-%d") if domain_create_date and \
                isinstance(domain_create_date, datetime) else None

            query_value[DOMAIN_CREATE_DATE_KEY] = domain_create_date
        except Exception as e:
            self._logger.error("Error in retrieving the registrar whois info for {} : {}".format(ip, e.message))
            query_value = {REGISTRAR_NAME_KEY: None, ABUSE_EMAIL_KEY: None, DOMAIN_CREATE_DATE_KEY: None}
        return query_value
