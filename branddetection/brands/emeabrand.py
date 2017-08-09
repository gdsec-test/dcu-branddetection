from branddetection.interfaces.brand import Brand


class EMEABrand(Brand):
    """
    EMEA specific brand for determining whether or not a domain is hosted or registered with EMEA
    """

    def __init__(self):
        self._brands = []
        self._ip_ranges = []
        self._asns = []

    def is_hosted(self, domain):
        for brand in self._brands:
            if brand.is_hosted(domain):
                return True
        return False

    def is_registered(self, domain):
        for brand in self._brands:
            if brand.is_registered(domain):
                return True
        return False

    def is_ip_in_range(self, ip):
        for brand in self._brands:
            if brand.is_ip_in_range(ip):
                return True
        return False
