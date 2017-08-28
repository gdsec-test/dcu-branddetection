import re
import logging
import json

from ipwhois import IPWhois
from whois import whois
from datetime import datetime
from dns import resolver, reversename
from branddetection.rediscache import RedisCache


class DomainHelper:
    """
    DomainHelper is a helper class to perform common operations and checks on domains and ips
    """
    def __init__(self, settings):
        self._logger = logging.getLogger(__name__)
        self._redis = RedisCache(settings)

    @staticmethod
    def is_ip(sourceDomainOrIp):
        """
        Helper function for determining whether a sourceDomainOrIp is an ip or not
        :return:
        :param sourceDomainOrIp:
        :return:
        """
        pattern = re.compile(r"((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\[]?(\.|dot)[ )\]]?){3}[0-9]{1,3})")
        return pattern.match(sourceDomainOrIp) is not None

    @staticmethod
    def get_ip_from_domain(domain):
        """
        Perform a lookup on domain name and attempt to retrieve the corresponding IP
        :param domain:
        :return:
        """
        dnsresolver = resolver.Resolver()
        dnsresolver.timeout = 1
        dnsresolver.lifetime = 1
        try:
            return dnsresolver.query(domain, 'A')[0].address
        except Exception as e:
            logging.error("Unable to get ip for %s : %s", domain, e.message)

    @staticmethod
    def convert_domain_to_ip(sourceDomainOrIp):
        if sourceDomainOrIp is None or sourceDomainOrIp == '':
            return None
        if sourceDomainOrIp is not str:
            sourceDomainOrIp = sourceDomainOrIp.encode('idna')
        if DomainHelper.is_ip(sourceDomainOrIp):
            ip = sourceDomainOrIp
        else:
            ip = DomainHelper.get_ip_from_domain(sourceDomainOrIp)
        return ip

    @staticmethod
    def get_domain_from_ip(ip):
        """
        Perform a lookup on an ip and attempt to retrieve the corresponding domain name
        :param ip:
        :return:
        """
        dnsresolver = resolver.Resolver()
        addr = reversename.from_address(ip)
        dnsresolver.timeout = 1
        dnsresolver.lifetime = 1
        try:
            return dnsresolver.query(addr, 'PTR')[0].to_text().rstrip('.').encode('idna')
        except Exception as e:
            logging.error("Unable to get domain for {} : {}", ip, e.message)

    def get_whois_info_from_cache(self, redis_record_key):
        query_value = self._redis.get_value(redis_record_key)
        return None if query_value is None else json.loads(query_value).get('result')

    def add_whois_info_to_cache(self, redis_record_key, query_value):
        self._redis.set_value(redis_record_key, json.dumps({'result': query_value}))

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
            redis_record_key = u'{}-hosting_whois_info'.format(ip)
            query_value = self.get_whois_info_from_cache(redis_record_key)

            if query_value is None:
                query_value = {IP_KEY: ip}

                info = IPWhois(ip).lookup_rdap()
                query_value[COMPANY_NAME_KEY] = info.get('network').get('name')

                email_list = []
                for k, v in info['objects'].iteritems():
                    email_address = v['contact']['email']
                    if email_address:
                        for i in email_address:
                            email_list.append(i['value'])
                query_value[ABUSE_EMAIL_KEY] = email_list
        except Exception as e:
            self._logger.error("Error retrieving hosting information for {} : {}".format(ip, e.message))
            query_value = {BRAND_KEY: None, IP_KEY: None, COMPANY_NAME_KEY: None, ABUSE_EMAIL_KEY: None}
        return query_value

    def get_registrar_information_via_whois(self, domain):
        REGISTRAR_NAME_KEY = 'registrar_name'
        ABUSE_EMAIL_KEY = 'registrar_abuse_email'
        DOMAIN_CREATE_DATE_KEY = 'domain_create_date'
        BRAND_KEY = 'brand'

        try:
            redis_record_key = u'{}-registrar_whois_info'.format(domain)
            query_value = self.get_whois_info_from_cache(redis_record_key)

            if query_value is None:
                query = whois(domain)
                if isinstance(query.emails, basestring):
                    query.emails = [query.emails]

                query_value = {REGISTRAR_NAME_KEY: query.registrar, ABUSE_EMAIL_KEY: query.emails}

                domain_create_date = query.creation_date[0] \
                    if isinstance(query.creation_date, list) else query.creation_date
                domain_create_date = domain_create_date.strftime("%Y-%m-%d") \
                    if domain_create_date and isinstance(domain_create_date, datetime) else None
                query_value[DOMAIN_CREATE_DATE_KEY] = domain_create_date
        except Exception as e:
            self._logger.error("Error in retrieving the registrar whois info for {} : {}".format(domain, e.message))
            query_value = {BRAND_KEY: None, REGISTRAR_NAME_KEY: None, ABUSE_EMAIL_KEY: None, DOMAIN_CREATE_DATE_KEY: None}
        return query_value
