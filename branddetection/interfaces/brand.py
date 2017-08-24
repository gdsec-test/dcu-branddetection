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

    def determine_hosting_brand_from_whois(self, whois_lookup, brand_abuse_emails, brand_org_names):
        """
        Common code for looking at a whois_lookup and finding matches for the hosting abuse emails and org names
        :param whois_lookup:
        :param brand_abuse_emails:
        :param brand_org_names:
        :return:
        """
        whois_abuse_emails = [] if whois_lookup['hosting_abuse_email'] is None else whois_lookup['hosting_abuse_email']
        for email in whois_abuse_emails:
            if email in brand_abuse_emails:
                return True

        whois_org_names = [] if whois_lookup['hosting_company_name'] is None else whois_lookup['hosting_company_name']
        for org_name in whois_org_names:
            if org_name in brand_org_names:
                return True
        return False

    def determine_registrar_from_whois(self, whois_lookup, brand_abuse_emails, brand_org_names):
        """
        Commond code for looking at a whois_lookup and finding matches for the registrar abuse emails and org names
        :param whois_lookup:
        :param brand_abuse_emails:
        :param brand_org_names:
        :return:
        """
        whois_abuse_emails = [] if whois_lookup['registrar_abuse_email'] is None else whois_lookup['registrar_abuse_email']
        for email in whois_abuse_emails:
            if email in brand_abuse_emails:
                return True

        whois_org_names = [] if whois_lookup['registrar_name'] is None else whois_lookup['registrar_name']
        for org_name in whois_org_names:
            if org_name in brand_org_names:
                return True
        return False
