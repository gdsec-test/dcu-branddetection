# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import domainservice_pb2 as domainservice__pb2


class DomainServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SuspendDomains = channel.unary_unary(
        '/domainmessages.DomainService/SuspendDomains',
        request_serializer=domainservice__pb2.SuspendDomainsRequest.SerializeToString,
        response_deserializer=domainservice__pb2.SuspendDomainsResponse.FromString,
        )
    self.UnSuspendDomains = channel.unary_unary(
        '/domainmessages.DomainService/UnSuspendDomains',
        request_serializer=domainservice__pb2.UnSuspendDomainsRequest.SerializeToString,
        response_deserializer=domainservice__pb2.UnSuspendDomainsResponse.FromString,
        )
    self.DomainInfo = channel.unary_unary(
        '/domainmessages.DomainService/DomainInfo',
        request_serializer=domainservice__pb2.DomainInfoRequest.SerializeToString,
        response_deserializer=domainservice__pb2.DomainInfoResponse.FromString,
        )


class DomainServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def SuspendDomains(self, request, context):
    """Adds an abuse lock for a domain
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UnSuspendDomains(self, request, context):
    """Removes an abuse lock for a domain
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DomainInfo(self, request, context):
    """Gathers information about a given domain
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_DomainServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SuspendDomains': grpc.unary_unary_rpc_method_handler(
          servicer.SuspendDomains,
          request_deserializer=domainservice__pb2.SuspendDomainsRequest.FromString,
          response_serializer=domainservice__pb2.SuspendDomainsResponse.SerializeToString,
      ),
      'UnSuspendDomains': grpc.unary_unary_rpc_method_handler(
          servicer.UnSuspendDomains,
          request_deserializer=domainservice__pb2.UnSuspendDomainsRequest.FromString,
          response_serializer=domainservice__pb2.UnSuspendDomainsResponse.SerializeToString,
      ),
      'DomainInfo': grpc.unary_unary_rpc_method_handler(
          servicer.DomainInfo,
          request_deserializer=domainservice__pb2.DomainInfoRequest.FromString,
          response_serializer=domainservice__pb2.DomainInfoResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'domainmessages.DomainService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
