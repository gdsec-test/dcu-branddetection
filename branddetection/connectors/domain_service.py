import logging

import grpc

import pb.domainservice_pb2
import pb.domainservice_pb2_grpc


class DomainService:
    def __init__(self, settings):
        self._logger = logging.getLogger(__name__)
        self._url = settings.DOMAIN_SERVICE_URL

    def get_registration(self, domain):
        """
        Retrieves the information from Domain Service via gRPC
        NOTE: Both the connection and call to the gRPC service are bound by a 5 second timeout
        :param domain:
        :return:
        """
        channel = grpc.insecure_channel(self._url)
        ready_future = grpc.channel_ready_future(channel)
        stub = pb.domainservice_pb2_grpc.DomainServiceStub(channel)

        resp = None

        try:
            ready_future.result(timeout=5)
        except grpc.FutureTimeoutError:
            self._logger.error("Unable to connect to: {}".format(self._url))
        else:
            try:
                resp = stub.DomainInfo(pb.domainservice_pb2.DomainInfoRequest(domain=domain), timeout=5)
            except grpc.RpcError as e:
                self._logger.error("Unable to retrieve domain from RegDb for domain {} : {}".format(domain, e.code()))
        finally:
            return resp
