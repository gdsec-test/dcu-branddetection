import abc
import re


class Brand(object, metaclass=abc.ABCMeta):
    """
    Abstract base class for all brands
    """

    @abc.abstractmethod
    def is_hosted(self, whois_lookup):
        """
        Determine whether a domain is hosted with a given brand
        :param whois_lookup:
        :return:
        """

    @abc.abstractmethod
    def is_registered(self, whois_lookup):
        """
        Determine whether a domain is registered with a given brand
        :param whois_lookup:
        :return:
        """

    @abc.abstractmethod
    def is_ip_in_range(self, ip):
        """
        Determine whether a given ip belongs to a given brand based on IP ranges pulled from ASN's.
        :param ip:
        :return:
        """

    def get_hostname_from_whois(self, whois_lookup):
        """
        Retrieve the hostname from a whois_lookup and strip out all non-letters else None
        :param whois_lookup:
        :return:
        """
        regex = re.compile('[^a-zA-Z1-4]')
        whois_host = whois_lookup['hosting_company_name']
        return None if whois_host is None else regex.sub('', whois_host)

    def get_registrar_from_whois(self, whois_lookup):
        """
        Retrieve the registrar from a whois_lookup and strip out all non-letters else None
        :param whois_lookup:
        :return:
        """
        regex = re.compile('[^a-zA-Z1-4]')
        whois_registrar = whois_lookup['registrar_name']
        return None if whois_registrar is None else regex.sub('', whois_registrar)
