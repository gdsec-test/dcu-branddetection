from branddetection.interfaces.brand import Brand


class ParagonBrand(Brand):
    """
    Paragon specific brand for determining whether or not a domain is hosted or registered with Paragon
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
