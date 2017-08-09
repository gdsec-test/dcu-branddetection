

class DomainHelper:
    """
    DomainHelper is a helper class to perform common operations and checks on domains and ips
    """

    def __init__(self):
        pass

    def is_domain(self, sourceDomainOrIp):
        """
        Helper function for determining whether a sourceDomainOrIp is a domain or not
        :param sourceDomainOrIp:
        :return:
        """
        return False

    def is_ip(self, sourceDomainOrIp):
        """
        Helper function for determining whether a sourceDomainOrIp is an ip or not
        :param sourceDomainOrIp:
        :return:
        """
        return False

    def nslookup(self, ip):
        """
        Perform an nslookup on ip and return the result
        :param ip:
        :return:
        """
        return None

    def whois_lookup(self, domain):
        """
        Perform a whois lookup on domain and return the result
        :param domain:
        :return:
        """
        return None
