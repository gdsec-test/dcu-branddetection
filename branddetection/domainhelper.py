import logging
import re
from datetime import datetime

from dns import resolver, reversename
from ipwhois import IPWhois
from whois import whois


class DomainHelper:
    """
    DomainHelper is a helper class to perform common operations and checks on domains and ips
    """

    CNAME_TTL = 3

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    @staticmethod
    def convert_domain_to_ip(sourceDomainOrIp):
        """
        Converts a given sourceDomainOrIp into an IP address
        :param sourceDomainOrIp:
        :return:
        """
        if not sourceDomainOrIp:
            return None
        if type(sourceDomainOrIp) != str:
            sourceDomainOrIp = sourceDomainOrIp.encode('idna').decode('utf-8')
        if DomainHelper.is_ip(sourceDomainOrIp):
            ip = sourceDomainOrIp
        else:
            ip = DomainHelper.get_ip_from_domain(sourceDomainOrIp)
        return ip

    @staticmethod
    def is_ip(sourceDomainOrIp):
        """
        Helper function for determining whether a sourceDomainOrIp is an ip or not
        :return:
        :param sourceDomainOrIp:
        :return:
        """
        if type(sourceDomainOrIp) != str:
            sourceDomainOrIp = sourceDomainOrIp.decode('utf-8')
        pattern = re.compile('((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\\[]?(\\.|dot)[ )\\]]?){3}[0-9]{1,3})')

        return pattern.match(sourceDomainOrIp) is not None

    @staticmethod
    def get_ip_from_domain(domain):
        """
        Perform a lookup on domain name and attempt to retrieve the corresponding IP
        :param domain:
        :return:
        """
        try:
            dnsresolver = resolver.Resolver()
            dnsresolver.timeout = 1
            dnsresolver.lifetime = 1
            return dnsresolver.query(domain, 'A')[0].address
        except Exception as e:
            logging.error('Unable to get ip for {} : {}'.format(domain, e))

    @staticmethod
    def get_domain_from_ip(ip):
        """
        Perform a lookup on an ip and attempt to retrieve the corresponding domain name
        :param ip:
        :return:
        """
        try:
            dnsresolver = resolver.Resolver()
            dnsresolver.timeout = 1
            dnsresolver.lifetime = 1
            addr = reversename.from_address(ip)
            idna_encoded = dnsresolver.query(addr, 'PTR')[0].to_text().rstrip('.').encode('idna')
            return idna_encoded.decode('utf-8')
        except Exception as e:
            logging.error('Unable to get domain for {} : {}'.format(ip, e))

    def get_hosting_information_via_whois(self, ip):
        """
        Return hosting network company name, the ip queried, and any relevant hosting abuse emails.
        :param ip:
        :return:
        """
        COMPANY_NAME_KEY = 'hosting_company_name'
        ABUSE_EMAIL_KEY = 'hosting_abuse_email'
        IP_KEY = 'ip'
        BRAND_KEY = 'brand'

        try:
            query_value = {IP_KEY: ip}

            info = IPWhois(ip).lookup_rdap()
            query_value[COMPANY_NAME_KEY] = info.get('network').get('name')

            email_list = []
            for k, v in info['objects'].items():
                email_address = v['contact']['email']
                if not email_address:
                    continue
                for i in email_address:
                    if i['value'] not in email_list:
                        email_list.append(i['value'])

            query_value[ABUSE_EMAIL_KEY] = email_list
        except Exception as e:
            self._logger.error('Error retrieving hosting information for {} : {}'.format(ip, e))
            query_value = {BRAND_KEY: None, IP_KEY: None, COMPANY_NAME_KEY: None, ABUSE_EMAIL_KEY: None}
        return query_value

    def get_registrar_information_via_whois(self, domain):
        REGISTRAR_NAME_KEY = 'registrar_name'
        ABUSE_EMAIL_KEY = 'registrar_abuse_email'
        DOMAIN_CREATE_DATE_KEY = 'domain_create_date'
        BRAND_KEY = 'brand'

        try:
            query = whois(domain)
            if isinstance(query.emails, str):
                query.emails = [query.emails]

            registrar = query.registrar
            if registrar is None:
                regex = re.compile(r'https?://(www\.)?')
                registrar = regex.sub('', query.registrar_url) if query.registrar_url else None

            query_value = {REGISTRAR_NAME_KEY: registrar, ABUSE_EMAIL_KEY: query.emails}

            domain_create_date = query.creation_date[0] \
                if isinstance(query.creation_date, list) else query.creation_date
            domain_create_date = domain_create_date.strftime('%Y-%m-%d') \
                if domain_create_date and isinstance(domain_create_date, datetime) else None
            query_value[DOMAIN_CREATE_DATE_KEY] = domain_create_date
        except Exception as e:
            self._logger.error('Error in retrieving the registrar whois info for {} : {}'.format(domain, e))
            query_value = {BRAND_KEY: None, REGISTRAR_NAME_KEY: None, ABUSE_EMAIL_KEY: None, DOMAIN_CREATE_DATE_KEY: None}
        return query_value

    def get_cname_from_domain(self, domain):
        dnsresolver = resolver.Resolver()

        # The number of seconds to wait for a response from a server, before timing out.
        dnsresolver.timeout = self.CNAME_TTL

        # The total number of seconds to spend trying to get an answer to the question.
        dnsresolver.lifetime = self.CNAME_TTL
        cnames = set()

        try:
            if not domain.startswith('www.'):
                domain = 'www.' + domain

            answers = dnsresolver.query(domain, 'CNAME')
            for rdata in answers:
                cnames.add(rdata.target.to_text())
        except Exception as e:
            self._logger.error('Unable to get CNAME for {} : {}'.format(domain, e))
        return cnames
