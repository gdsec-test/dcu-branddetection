import logging
import domainservice_pb2
import domainservice_pb2_grpc
import grpc

class DomainServce:

    # These will likely go away with new RegDB rest API
    _STATUS_CODES = [0, 3, 4, 12, 16, 46, 77, 78, 79, 83, 93, 98, 239, 240, 242, 243]

    def __init__(self, settings):
        self._logger = logging.getLogger(__name__)
        self._url = settings.DOMAIN_SERVICES_URL

    def get_registration(self, domain):
        channel = grpc.insecure_channel(self._url)
        ready_future = grpc.channel_ready_future(channel)
        stub = domainservice_pb2_grpc.DomainServiceStub(channel)

        resp = None

        try:
            ready_future.result(timeout=5)
        except grpc.FutureTimeoutError:
            self._logger.error("Unable to connect to: {}".format(self._url))
        else:
            try:
               resp = stub.DomainInfo(domainservice_pb2.DomainInfoRequest(domain=domain), timeout=5)
            except grpc.RpcError as e:
                self._logger.error("Unable to determine registrar for domain {} : {}".format(domain, e.message))
        finally:
            return resp

