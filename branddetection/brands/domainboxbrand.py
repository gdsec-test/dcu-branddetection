from branddetection.interfaces.brand import Brand


class DomainBoxBrand(Brand):
    """
    DomainBox specific brand for determining whether or not a domain is hosted or registered with DomainBox
    """

    def __init__(self):
        self._ip_ranges = []
        self._asns = []

    def is_hosted(self, domain):
        return False

    def is_registered(self, domain):
        return False

    def is_ip_in_range(self, ip):
        return False
