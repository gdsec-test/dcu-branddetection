import re
import json
import logging

from dns import resolver, reversename

class DomainHelper:
    """
    DomainHelper is a helper class to perform common operations and checks on domains and ips
    """

    def __init__(self):
        self._logger = logging.getLogger(__name__)

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
        :param ip:
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
            logging.error("Unable to get domain for %s : %s", ip, e.message)

    # def get_hosting_info(self, domain):
    #     """
    #     Return hosting network and email
    #     :param domain:
    #     :return:
    #     """
    #
    #     COMPANY_NAME_KEY = 'hosting_company_name'
    #     ABUSE_EMAIL_KEY = 'hosting_abuse_email'
    #     IP_KEY = 'ip'
    #     email_list = []
    #     query_value = {}
    #     try:
    #         if domain is None or domain == '':
    #             raise ValueError('Blank domain name was provided')
    #         redis_record_key = u'{}-ip_whois_info'.format(domain)
    #         query_value = self._redis.get_value(redis_record_key)
    #         if query_value is None:
    #             if domain is not str:
    #                 domain = domain.encode('idna')
    #             if self.is_ip(domain):
    #                 ip = domain
    #             else:
    #                 ip = self.get_ip_from_domain(domain)
    #             query_value = dict(ip=ip)
    #             if self._check_hosted_here(ip):
    #                 query_value[COMPANY_NAME_KEY] = self.GODADDY_NAME
    #                 query_value[ABUSE_EMAIL_KEY] = [self.GODADDY_ABUSE_EMAIL]
    #                 self._redis.set_value(redis_record_key, json.dumps({self.REDIS_DATA_KEY: query_value}))
    #                 return query_value
    #             self._logger.info("Resorting to IPWhois lookup for {}".format(ip))
    #             info = IPWhois(ip).lookup_rdap()
    #             query_value[COMPANY_NAME_KEY] = info.get('network').get('name')
    #             for k, v in info['objects'].iteritems():
    #                 email_address = v['contact']['email']
    #                 if email_address:
    #                     for i in email_address:
    #                         email_list.append(i['value'])
    #             query_value[ABUSE_EMAIL_KEY] = email_list
    #             self._redis.set_value(redis_record_key, json.dumps({self.REDIS_DATA_KEY: query_value}))
    #         else:
    #             query_value = json.loads(query_value).get(self.REDIS_DATA_KEY)
    #     except Exception as e:
    #         self._logger.error("Error in getting the hosting whois info for %s : %s", domain, e.message)
    #         # If exception occurred before query_value had completed assignment, set keys to None
    #         query_value = return_expected_dict_due_to_exception(query_value, [COMPANY_NAME_KEY,
    #                                                                           ABUSE_EMAIL_KEY,
    #                                                                           IP_KEY])
    #     return query_value

    # def get_registrar_info(self, domain):
    #     """
    #     Return registrar network, domain create date and email
    #     :param domain:
    #     :return:
    #     """
    #     REGISTRAR_NAME_KEY = 'registrar_name'
    #     ABUSE_EMAIL_KEY = 'registrar_abuse_email'
    #     DOMAIN_CREATE_DATE_KEY = 'domain_create_date'
    #     query_value = {}
    #     try:
    #         if domain is None or domain == '':
    #             raise ValueError('Blank domain name was provided')
    #         redis_record_key = u'{}-registrar_whois_info'.format(domain)
    #         query_value = self._redis.get_value(redis_record_key)
    #         if query_value is None:
    #             # Try godaddy first
    #             try:
    #                 query = WhoisEntry.load(domain, NICClient().whois(domain, 'whois.godaddy.com', True))
    #                 if query.registrar:
    #                     query.registrar = self.GODADDY_NAME
    #                     query.emails = [self.GODADDY_ABUSE_EMAIL]
    #                 else:
    #                     # If query.registrar is None, go for the alternate whois query
    #                     raise PywhoisError
    #             except PywhoisError:
    #                 query = whois(domain)
    #                 if isinstance(query.emails, basestring):
    #                     query.emails = [query.emails]
    #             query_value = dict(registrar_name=query.registrar, registrar_abuse_email=query.emails)
    #             domain_create_date = query.creation_date[0] if isinstance(query.creation_date, list)\
    #                 else query.creation_date
    #             domain_create_date = domain_create_date.strftime(self.date_format) if domain_create_date and  \
    #                 isinstance(domain_create_date, datetime) else None
    #             query_value[DOMAIN_CREATE_DATE_KEY] = domain_create_date
    #             self._redis.set_value(redis_record_key, json.dumps({self.REDIS_DATA_KEY: query_value}))
    #         else:
    #             query_value = json.loads(query_value).get(self.REDIS_DATA_KEY)
    #     except Exception as e:
    #         logging.error("Error in getting the registrar whois info for %s : %s", domain, e.message)
    #         # If exception occurred before query_value had completed assignment, set keys to None
    #         query_value = return_expected_dict_due_to_exception(query_value, [REGISTRAR_NAME_KEY,
    #                                                                           ABUSE_EMAIL_KEY,
    #                                                                           DOMAIN_CREATE_DATE_KEY])
    #     return query_value
