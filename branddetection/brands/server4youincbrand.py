from branddetection.interfaces.brand import Brand


class Server4UIncBrand(Brand):
    """
    Server4UInc specific brand for determining whether or not a domain is hosted or registered with Server4UInc
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
