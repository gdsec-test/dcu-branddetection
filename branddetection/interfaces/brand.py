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

    def determine_hosting_brand_from_whois(self, whois_lookup, brand_abuse_email, brand_org_name):
        """
        Common code for looking at a whois_lookup and finding matches for the hosting abuse emails and org names
        :param whois_lookup:
        :param brand_abuse_email:
        :param brand_org_name:
        :return:
        """
        abuse_emails = [] if whois_lookup['hosting_abuse_email'] is None else whois_lookup['hosting_abuse_email']
        for email in abuse_emails:
            if email in brand_abuse_email:
                return True
        return whois_lookup['hosting_company_name'] == brand_org_name

    def determine_registrar_from_whois(self, whois_lookup, brand_abuse_email, brand_org_name):
        """
        Commond code for looking at a whois_lookup and finding matches for the registrar abuse emails and org names
        :param whois_lookup:
        :param brand_abuse_email:
        :param brand_org_name:
        :return:
        """
        whois_abuse_emails = [] if whois_lookup['registrar_abuse_email'] is None else whois_lookup['registrar_abuse_email']
        for email in whois_abuse_emails:
            if email in brand_abuse_email:
                return True
        return whois_lookup['registrar_name'] == brand_org_name
