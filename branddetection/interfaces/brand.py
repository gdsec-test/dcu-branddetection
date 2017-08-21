import abc


class Brand(object):
    """
    Abstract base class for all brands
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def is_hosted(self, whois_lookup):
        """
        Determine whether a domain is hosted with a given brand
        :param whois_lookup:
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

    def determine_hosting_brand_from_whois(self, whois_lookup, abuse_email, org_name):
        """
        Common code for looking at a whois_lookup and finding matches for the abuse_emails and org_name
        :param whois_lookup:
        :param abuse_email:
        :param org_name:
        :return:
        """
        for email in whois_lookup['hosting_abuse_email']:
            if email in abuse_email:
                return True
        return whois_lookup['hosting_company_name'] == org_name

    def determine_registrar_from_whois(self, whois_lookup, abuse_email, org_name):
        for email in whois_lookup['registrar_abuse_email']:
            if email in abuse_email:
                return True
        return whois_lookup['registrar_abuse_email'] == org_name


class ForeignBrand(Brand):

    NAME = "FOREIGN"

    def is_hosted(self, whois_lookup):
        return False

    def is_registered(self, domain):
        return False

    def is_ip_in_range(self, ip):
        return False
