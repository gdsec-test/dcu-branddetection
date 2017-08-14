import abc


class Brand(object):
    """
    Abstract base class for all brands
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def is_hosted(self, domain):
        """
        Determine whether a domain is hosted with a given brand
        :param domain:
        :return:
        """

    @abc.abstractmethod
    def is_registered(self, domain):
        """
        Determine whether a domain is registered with a given brand
        :param domain:
        :return:
        """

    @abc.abstractmethod
    def is_ip_in_range(self, ip):
        """
        Determine whether a given ip belongs to a given brand based on IP ranges pulled from ASN's.
        :param ip:
        :return:
        """

class ForeignBrand(Brand):

    NAME = "FOREIGN"

    def is_hosted(self, domain):
        return False

    def is_registered(self, domain):
        return False

    def is_ip_in_range(self, ip):
        return False