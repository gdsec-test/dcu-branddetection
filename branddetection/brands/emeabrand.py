from branddetection.interfaces.brand import Brand

from branddetection.brands.reg123brand import Reg123Brand
from branddetection.brands.domainboxbrand import DomainBoxBrand
from branddetection.brands.domainfactorybrand import DomainFactoryBrand
from branddetection.brands.domainmonsterbrand import DomainMonsterBrand
from branddetection.brands.heartinternetbrand import HeartInternetBrand
from branddetection.brands.hosteuropebrand import HostEuropeBrand
from branddetection.brands.hosteuropeiberiabrand import HostEuropeIberia
from branddetection.brands.internet24brand import Internet24Brand
from branddetection.brands.loomesbrand import LoomesBrand
from branddetection.brands.paragonbrand import ParagonBrand
from branddetection.brands.server4uincbrand import Server4UIncBrand
from branddetection.brands.server4ugmbhbrand import Server4UGmbH
from branddetection.brands.signupbrand import SignUpBrand
from branddetection.brands.veliabrand import VeliaBrand
from branddetection.brands.webfusionbrand import WebFusionBrand
from branddetection.brands.meshdigitalbrand import MeshDigitalBrand
from branddetection.brands.meshdebrand import MeshDeBrand
from branddetection.brands.mainlabbrand import MainLabBrand


class EMEABrand(Brand):
    """
    EMEA specific brand for determining whether or not a domain is hosted or registered with EMEA
    """
    NAME = 'EMEA'
    HOSTING_COMPANY_NAME = ''
    HOSTING_ABUSE_EMAIL = ''

    def __init__(self):
        self._brands = [Reg123Brand(), DomainBoxBrand(), DomainFactoryBrand(), DomainMonsterBrand(),
                        HeartInternetBrand(), HostEuropeBrand(), HostEuropeIberia(), Internet24Brand(), LoomesBrand(),
                        ParagonBrand(), Server4UIncBrand(), Server4UGmbH(), SignUpBrand(), VeliaBrand(),
                        WebFusionBrand(), MeshDigitalBrand(), MeshDeBrand(), MainLabBrand()]

    def is_hosted(self, whois_lookup):
        for brand in self._brands:
            if brand.is_hosted(whois_lookup):
                return True
        return False

    def is_registered(self, whois_lookup):
        for brand in self._brands:
            if brand.is_registered(whois_lookup):
                return True
        return False

    def is_ip_in_range(self, ip):
        for brand in self._brands:
            if brand.is_ip_in_range(ip):
                return True
        return False
