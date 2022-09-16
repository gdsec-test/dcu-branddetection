import socket

from csetutils.flask.logging import get_logging

from branddetection.brands.domainfactorybrand import DomainFactoryBrand
from branddetection.brands.heartinternetbrand import HeartInternetBrand
from branddetection.brands.hosteuropebrand import HostEuropeBrand
from branddetection.brands.hosteuropeiberiabrand import HostEuropeIberia
from branddetection.brands.meshdigitalbrand import MeshDigitalBrand
from branddetection.brands.paragonbrand import ParagonBrand
from branddetection.brands.plusserverbrand import PlusServerBrand
from branddetection.brands.reg123brand import Reg123Brand
from branddetection.brands.server4ugmbhbrand import Server4UGmbH
from branddetection.brands.server4uincbrand import Server4UIncBrand
from branddetection.brands.veliabrand import VeliaBrand
from branddetection.interfaces.brand import Brand


class EMEABrand(Brand):
    """
    EMEA specific brand for determining whether or not a domain is hosted or registered with EMEA
    """
    NAME = 'EMEA'
    HOSTING_COMPANY_NAME = 'Host Europe GmbH'
    HOSTING_ABUSE_EMAIL = 'abuse-input@heg.com'
    DEFAULT_REPORT_EMAIL = 'automationfails-emea@godaddy.com'

    def __init__(self):
        self._logger = get_logging()
        self._brands = [Reg123Brand(), DomainFactoryBrand(), HeartInternetBrand(), HostEuropeBrand(),
                        HostEuropeIberia(), ParagonBrand(), Server4UIncBrand(),
                        Server4UGmbH(), VeliaBrand(), MeshDigitalBrand(), PlusServerBrand()]

    def is_hosted(self, whois_lookup: dict) -> bool:
        if isinstance(whois_lookup, dict):
            for brand in self._brands:
                hostname = self.get_hostname_from_whois(whois_lookup) or ''
                if brand.NAME in hostname.upper():
                    return True
                for hosting_string in brand.HOSTING_MATCHES:
                    if hosting_string in hostname.upper():
                        return True

                host_ip = whois_lookup.get('ip')
                # If we don't have a match, check whether Host lookup matches same pattern
                if host_ip:
                    try:
                        host_result = socket.gethostbyaddr(host_ip)[0].upper()
                        for hosting_string in brand.HOSTING_MATCHES:
                            if hosting_string in host_result:
                                return True
                    except Exception as e:
                        self._logger.warning('Unknown host for {} : {}'.format(host_ip, e))

        return False

    def is_registered(self, whois_lookup):
        for brand in self._brands:
            if brand.is_registered(whois_lookup):
                return True
        return False

    def is_ip_in_range(self, ip):
        for brand in self._brands:
            if brand.is_ip_in_range(ip):
                return True
        return False

    def get_email_from_ip(self, ip):
        for brand in self._brand:
            if brand.is_ip_in_range(ip):
                return brand.HOSTING_ABUSE_EMAIL
        return self.DEFAULT_REPORT_EMAIL

    def get_email_for_registrar_from_whois(self, whois_lookup):
        for brand in self._brands:
            if brand.is_registered(whois_lookup):
                return brand.HOSTING_ABUSE_EMAIL
        return self.DEFAULT_REPORT_EMAIL

    def get_email_for_hosted_from_whois(self, whois_lookup):
        for brand in self._brands:
            if brand.is_hosted(whois_lookup):
                return brand.HOSTING_ABUSE_EMAIL
        return self.DEFAULT_REPORT_EMAIL
