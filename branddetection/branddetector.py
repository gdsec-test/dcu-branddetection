import json

from csetutils.flask.logging import get_logging

from branddetection.brands.emeabrand import EMEABrand
from branddetection.brands.godaddybrand import GoDaddyBrand
from branddetection.connectors.domain_service import DomainService
from branddetection.domainhelper import DomainHelper


class BrandDetectorDecorator:
    _HOSTING_REDIS_KEY = '{}-hosting_whois_info'
    _REGISTRAR_REDIS_KEY = '{}-registrar_whois_info'

    def __init__(self, decorated, redis):
        self._decorated = decorated
        self._redis = redis

    def get_hosting_info(self, sourceDomainOrIp):
        """
        Decorator function that validates data and checks the cache before handing the get_hosting_info call off to the
        decorated class
        :param sourceDomainOrIp:
        :return:
        """
        ip = DomainHelper.convert_domain_to_ip(sourceDomainOrIp)
        if ip is None:
            return {'brand': None, 'hosting_company_name': None, 'hosting_abuse_email': None, 'ip': None}

        redis_record_key = self._HOSTING_REDIS_KEY.format(ip)
        whois_lookup = self._get_whois_info_from_cache(redis_record_key)

        if whois_lookup is None:
            domain = DomainHelper.get_domain_from_ip(sourceDomainOrIp) if DomainHelper.is_ip(sourceDomainOrIp) else sourceDomainOrIp
            whois_lookup = self._decorated.get_hosting_info(ip, domain)

            if whois_lookup.get('brand', None) is not None:
                self._add_whois_info_to_cache(redis_record_key, whois_lookup)
        return whois_lookup

    def get_registrar_info(self, domain):
        """
        Decorator function that checks the cache before handing the get_registrar_info call off to the decorated class.
        :param domain:
        :return:
        """
        redis_record_key = self._REGISTRAR_REDIS_KEY.format(domain)
        whois_lookup = self._get_whois_info_from_cache(redis_record_key)

        if whois_lookup is None:
            whois_lookup = self._decorated.get_registrar_info(domain)

            if whois_lookup.get('brand', None) is not None:
                self._add_whois_info_to_cache(redis_record_key, whois_lookup)
        return whois_lookup

    def _get_whois_info_from_cache(self, redis_record_key):
        """
        Attempts to retrieve the record from the cache with key redis_record_key otherwise None
        :param redis_record_key:
        :return:
        """
        query_value = self._redis.get_value(redis_record_key)
        if query_value and type(query_value) != str:
            query_value = query_value.decode('utf-8')
        return None if not query_value else json.loads(query_value).get('result')

    def _add_whois_info_to_cache(self, redis_record_key, query_value):
        """
        Attempts to add the query_value record with key redis_record_key into the cache
        :param redis_record_key:
        :param query_value:
        :return:
        """
        self._redis.set_value(redis_record_key, json.dumps({'result': query_value}))


class BrandDetector:
    def __init__(self, settings):
        self._logger = get_logging()
        self._domain_helper = DomainHelper()
        self._domain_service = DomainService(settings)

        self._brands = [GoDaddyBrand(), EMEABrand()]

    def get_hosting_info(self, ip, domain):
        """
        Attempt to find the appropriate brand that sourceDomainOrIp is hosted with
        :param ip:
        :param domain:
        :return:
        """
        whois_lookup = self._get_hosting_in_known_ip_range(ip)
        if whois_lookup is None:
            whois_lookup = self._get_hosting_by_fallback(ip, domain)

        return whois_lookup

    def get_registrar_info(self, domain):
        """
        Attempt to find the appropriate brand that sourceDomainOrIp is registered with by connecting to DomainService
        :param domain:
        :return:
        """
        resp = self._domain_service.get_registration(domain)
        if resp:
            # NOTE: Since hosting/registrar contacts are the same for GoDaddy, we reuse fields like HOSTING_ABUSE_EMAIL
            return {'brand': GoDaddyBrand.NAME, 'registrar_name': GoDaddyBrand.HOSTING_COMPANY_NAME,
                    'registrar_abuse_email': [GoDaddyBrand.HOSTING_ABUSE_EMAIL], 'domain_create_date': resp.createDate,
                    'domain_id': resp.domainId, 'first_pass_enrichment': 'regdb'}
        else:
            return self._get_registrar_by_fallback(domain)

    def _get_registrar_by_fallback(self, domain):
        """
        Attempt to find the appropriate brand that sourceDomainOrIp is registered with via a whois lookup
        :param domain:
        :return:
        """
        whois_lookup = self._domain_helper.get_registrar_information_via_whois(domain)
        whois_lookup['first_pass_enrichment'] = 'whois'
        whois_lookup['domain_id'] = None  # Created for consistency; if DomainService call fails domain_id will be empty
        for brand in self._brands:
            if brand.is_registered(whois_lookup):
                self._logger.info("Successfully found a registrar: {} for domain/ip: {}"
                                  .format(brand.NAME, domain))
                whois_lookup['brand'] = brand.NAME
                return whois_lookup

        self._logger.info("Unable to find a matching registrar for domain/ip: {}. Brand is FOREIGN".format(domain))
        whois_lookup['brand'] = "FOREIGN"
        return whois_lookup

    def _get_hosting_in_known_ip_range(self, ip):
        """
        Attempt to determine whether a given ip is known by any of the brands
        :param ip:
        :return:
        """
        for brand in self._brands:
            if brand.is_ip_in_range(ip):
                self._logger.info("Successfully found a hosting provider: {} for domain/ip: {}".format(brand.NAME, ip))
                return {'brand': brand.NAME, 'hosting_company_name': brand.HOSTING_COMPANY_NAME, 'ip': ip,
                        'hosting_abuse_email': [brand.HOSTING_ABUSE_EMAIL], }
        return None

    def _get_hosting_by_fallback(self, ip, domain):
        """
        If unable to determine hosting via ip lookup, fall back and use each brand's own way of determining hosting
        :param ip:
        :param domain:
        :return:
        """
        whois_lookup = self._domain_helper.get_hosting_information_via_whois(ip)
        for brand in self._brands:
            if brand.is_hosted(whois_lookup):
                self._logger.info("Successfully found a hosting provider using fallback method: {} for domain/ip: {}"
                                  .format(brand.NAME, ip))
                whois_lookup['brand'] = brand.NAME
                whois_lookup['hosting_company_name'] = brand.HOSTING_COMPANY_NAME
                return whois_lookup

        # Retrieving CNAMES to check for Website Builder for Designers (WSBD) products.
        cnames = self._domain_helper.get_cname_from_domain(domain)
        for cname in cnames:
            if 'godaddysiteonline.com' in cname or 'godaddysiteonline.com' in domain:
                whois_lookup['brand'] = GoDaddyBrand.NAME
                whois_lookup['hosting_company_name'] = GoDaddyBrand.HOSTING_COMPANY_NAME
                whois_lookup['hosting_abuse_email'] = [GoDaddyBrand.HOSTING_ABUSE_EMAIL]
                return whois_lookup

        self._logger.info("Unable to find a matching hosting provider for domain/ip: {}. Brand is FOREIGN.".format(ip))
        whois_lookup['brand'] = "FOREIGN"
        return whois_lookup

    def get_plid_email(self, plid):
        """
        Function that does BLAH LKM TODO
        :param plid:
        :return:
        """
        mail_to = {'525844': 'abuse@123-reg.co.uk',  # 123REG
                   '525845': 'abuse@df.eu',  # Domain Factory
                   '525848': 'abuse@heartinternet.uk',  # Heart Internet
                   '525847': 'abuse@hosteurope.de',  # HostEurope
                   '527397': 'abuse@tsohost.com',  # TSOHost
                   '541136': 'abuse@velia.net',  # Velia
                   '536004': 'abuse@webhuset.no',  # Webhuset
                   'default': 'automationfails-emea@godaddy.com'  # Default address for undefined PLID or enrichment error
                   }
        return {'email': mail_to.get(plid, self.mail_to.get('default'))}
