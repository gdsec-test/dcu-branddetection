# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: domainservice.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='domainservice.proto',
  package='domainmessages',
  syntax='proto3',
  serialized_pb=_b('\n\x13\x64omainservice.proto\x12\x0e\x64omainmessages\"*\n\x06\x44omain\x12\x0e\n\x06\x64omain\x18\x01 \x01(\t\x12\x10\n\x08\x64omainid\x18\x02 \x01(\t\"\'\n\x11GetDomainsRequest\x12\x12\n\ncustomerid\x18\x01 \x01(\t\"=\n\x12GetDomainsResponse\x12\'\n\x07\x64omains\x18\x01 \x03(\x0b\x32\x16.domainmessages.Domain\"F\n\x15SuspendDomainsRequest\x12\x11\n\tdomainids\x18\x01 \x03(\t\x12\x0c\n\x04note\x18\x02 \x01(\t\x12\x0c\n\x04user\x18\x03 \x01(\t\"\'\n\x16SuspendDomainsResponse\x12\r\n\x05\x63ount\x18\x01 \x01(\x05\"H\n\x17UnSuspendDomainsRequest\x12\x11\n\tdomainids\x18\x01 \x03(\t\x12\x0c\n\x04note\x18\x02 \x01(\t\x12\x0c\n\x04user\x18\x03 \x01(\t\")\n\x18UnSuspendDomainsResponse\x12\r\n\x05\x63ount\x18\x01 \x01(\x05\"7\n\x15\x44omainInStatusRequest\x12\x0e\n\x06\x64omain\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x03(\x05\"\'\n\x16\x44omainInStatusResponse\x12\r\n\x05\x66ound\x18\x01 \x01(\x08\x32\x8d\x03\n\rDomainService\x12S\n\nGetDomains\x12!.domainmessages.GetDomainsRequest\x1a\".domainmessages.GetDomainsResponse\x12_\n\x0eSuspendDomains\x12%.domainmessages.SuspendDomainsRequest\x1a&.domainmessages.SuspendDomainsResponse\x12\x65\n\x10UnSuspendDomains\x12\'.domainmessages.UnSuspendDomainsRequest\x1a(.domainmessages.UnSuspendDomainsResponse\x12_\n\x0e\x44omainInStatus\x12%.domainmessages.DomainInStatusRequest\x1a&.domainmessages.DomainInStatusResponseB\x04Z\x02pbb\x06proto3')
)




_DOMAIN = _descriptor.Descriptor(
  name='Domain',
  full_name='domainmessages.Domain',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='domain', full_name='domainmessages.Domain.domain', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='domainid', full_name='domainmessages.Domain.domainid', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=39,
  serialized_end=81,
)


_GETDOMAINSREQUEST = _descriptor.Descriptor(
  name='GetDomainsRequest',
  full_name='domainmessages.GetDomainsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='customerid', full_name='domainmessages.GetDomainsRequest.customerid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=83,
  serialized_end=122,
)


_GETDOMAINSRESPONSE = _descriptor.Descriptor(
  name='GetDomainsResponse',
  full_name='domainmessages.GetDomainsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='domains', full_name='domainmessages.GetDomainsResponse.domains', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=124,
  serialized_end=185,
)


_SUSPENDDOMAINSREQUEST = _descriptor.Descriptor(
  name='SuspendDomainsRequest',
  full_name='domainmessages.SuspendDomainsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='domainids', full_name='domainmessages.SuspendDomainsRequest.domainids', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='note', full_name='domainmessages.SuspendDomainsRequest.note', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='user', full_name='domainmessages.SuspendDomainsRequest.user', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=187,
  serialized_end=257,
)


_SUSPENDDOMAINSRESPONSE = _descriptor.Descriptor(
  name='SuspendDomainsResponse',
  full_name='domainmessages.SuspendDomainsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='count', full_name='domainmessages.SuspendDomainsResponse.count', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=259,
  serialized_end=298,
)


_UNSUSPENDDOMAINSREQUEST = _descriptor.Descriptor(
  name='UnSuspendDomainsRequest',
  full_name='domainmessages.UnSuspendDomainsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='domainids', full_name='domainmessages.UnSuspendDomainsRequest.domainids', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='note', full_name='domainmessages.UnSuspendDomainsRequest.note', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='user', full_name='domainmessages.UnSuspendDomainsRequest.user', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=300,
  serialized_end=372,
)


_UNSUSPENDDOMAINSRESPONSE = _descriptor.Descriptor(
  name='UnSuspendDomainsResponse',
  full_name='domainmessages.UnSuspendDomainsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='count', full_name='domainmessages.UnSuspendDomainsResponse.count', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=374,
  serialized_end=415,
)


_DOMAININSTATUSREQUEST = _descriptor.Descriptor(
  name='DomainInStatusRequest',
  full_name='domainmessages.DomainInStatusRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='domain', full_name='domainmessages.DomainInStatusRequest.domain', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='domainmessages.DomainInStatusRequest.status', index=1,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=417,
  serialized_end=472,
)


_DOMAININSTATUSRESPONSE = _descriptor.Descriptor(
  name='DomainInStatusResponse',
  full_name='domainmessages.DomainInStatusResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='found', full_name='domainmessages.DomainInStatusResponse.found', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=474,
  serialized_end=513,
)

_GETDOMAINSRESPONSE.fields_by_name['domains'].message_type = _DOMAIN
DESCRIPTOR.message_types_by_name['Domain'] = _DOMAIN
DESCRIPTOR.message_types_by_name['GetDomainsRequest'] = _GETDOMAINSREQUEST
DESCRIPTOR.message_types_by_name['GetDomainsResponse'] = _GETDOMAINSRESPONSE
DESCRIPTOR.message_types_by_name['SuspendDomainsRequest'] = _SUSPENDDOMAINSREQUEST
DESCRIPTOR.message_types_by_name['SuspendDomainsResponse'] = _SUSPENDDOMAINSRESPONSE
DESCRIPTOR.message_types_by_name['UnSuspendDomainsRequest'] = _UNSUSPENDDOMAINSREQUEST
DESCRIPTOR.message_types_by_name['UnSuspendDomainsResponse'] = _UNSUSPENDDOMAINSRESPONSE
DESCRIPTOR.message_types_by_name['DomainInStatusRequest'] = _DOMAININSTATUSREQUEST
DESCRIPTOR.message_types_by_name['DomainInStatusResponse'] = _DOMAININSTATUSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Domain = _reflection.GeneratedProtocolMessageType('Domain', (_message.Message,), dict(
  DESCRIPTOR = _DOMAIN,
  __module__ = 'domainservice_pb2'
  # @@protoc_insertion_point(class_scope:domainmessages.Domain)
  ))
_sym_db.RegisterMessage(Domain)

GetDomainsRequest = _reflection.GeneratedProtocolMessageType('GetDomainsRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETDOMAINSREQUEST,
  __module__ = 'domainservice_pb2'
  # @@protoc_insertion_point(class_scope:domainmessages.GetDomainsRequest)
  ))
_sym_db.RegisterMessage(GetDomainsRequest)

GetDomainsResponse = _reflection.GeneratedProtocolMessageType('GetDomainsResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETDOMAINSRESPONSE,
  __module__ = 'domainservice_pb2'
  # @@protoc_insertion_point(class_scope:domainmessages.GetDomainsResponse)
  ))
_sym_db.RegisterMessage(GetDomainsResponse)

SuspendDomainsRequest = _reflection.GeneratedProtocolMessageType('SuspendDomainsRequest', (_message.Message,), dict(
  DESCRIPTOR = _SUSPENDDOMAINSREQUEST,
  __module__ = 'domainservice_pb2'
  # @@protoc_insertion_point(class_scope:domainmessages.SuspendDomainsRequest)
  ))
_sym_db.RegisterMessage(SuspendDomainsRequest)

SuspendDomainsResponse = _reflection.GeneratedProtocolMessageType('SuspendDomainsResponse', (_message.Message,), dict(
  DESCRIPTOR = _SUSPENDDOMAINSRESPONSE,
  __module__ = 'domainservice_pb2'
  # @@protoc_insertion_point(class_scope:domainmessages.SuspendDomainsResponse)
  ))
_sym_db.RegisterMessage(SuspendDomainsResponse)

UnSuspendDomainsRequest = _reflection.GeneratedProtocolMessageType('UnSuspendDomainsRequest', (_message.Message,), dict(
  DESCRIPTOR = _UNSUSPENDDOMAINSREQUEST,
  __module__ = 'domainservice_pb2'
  # @@protoc_insertion_point(class_scope:domainmessages.UnSuspendDomainsRequest)
  ))
_sym_db.RegisterMessage(UnSuspendDomainsRequest)

UnSuspendDomainsResponse = _reflection.GeneratedProtocolMessageType('UnSuspendDomainsResponse', (_message.Message,), dict(
  DESCRIPTOR = _UNSUSPENDDOMAINSRESPONSE,
  __module__ = 'domainservice_pb2'
  # @@protoc_insertion_point(class_scope:domainmessages.UnSuspendDomainsResponse)
  ))
_sym_db.RegisterMessage(UnSuspendDomainsResponse)

DomainInStatusRequest = _reflection.GeneratedProtocolMessageType('DomainInStatusRequest', (_message.Message,), dict(
  DESCRIPTOR = _DOMAININSTATUSREQUEST,
  __module__ = 'domainservice_pb2'
  # @@protoc_insertion_point(class_scope:domainmessages.DomainInStatusRequest)
  ))
_sym_db.RegisterMessage(DomainInStatusRequest)

DomainInStatusResponse = _reflection.GeneratedProtocolMessageType('DomainInStatusResponse', (_message.Message,), dict(
  DESCRIPTOR = _DOMAININSTATUSRESPONSE,
  __module__ = 'domainservice_pb2'
  # @@protoc_insertion_point(class_scope:domainmessages.DomainInStatusResponse)
  ))
_sym_db.RegisterMessage(DomainInStatusResponse)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('Z\002pb'))

_DOMAINSERVICE = _descriptor.ServiceDescriptor(
  name='DomainService',
  full_name='domainmessages.DomainService',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=516,
  serialized_end=913,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetDomains',
    full_name='domainmessages.DomainService.GetDomains',
    index=0,
    containing_service=None,
    input_type=_GETDOMAINSREQUEST,
    output_type=_GETDOMAINSRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SuspendDomains',
    full_name='domainmessages.DomainService.SuspendDomains',
    index=1,
    containing_service=None,
    input_type=_SUSPENDDOMAINSREQUEST,
    output_type=_SUSPENDDOMAINSRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='UnSuspendDomains',
    full_name='domainmessages.DomainService.UnSuspendDomains',
    index=2,
    containing_service=None,
    input_type=_UNSUSPENDDOMAINSREQUEST,
    output_type=_UNSUSPENDDOMAINSRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='DomainInStatus',
    full_name='domainmessages.DomainService.DomainInStatus',
    index=3,
    containing_service=None,
    input_type=_DOMAININSTATUSREQUEST,
    output_type=_DOMAININSTATUSRESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_DOMAINSERVICE)

DESCRIPTOR.services_by_name['DomainService'] = _DOMAINSERVICE

try:
  # THESE ELEMENTS WILL BE DEPRECATED.
  # Please use the generated *_pb2_grpc.py files instead.
  import grpc
  from grpc.beta import implementations as beta_implementations
  from grpc.beta import interfaces as beta_interfaces
  from grpc.framework.common import cardinality
  from grpc.framework.interfaces.face import utilities as face_utilities


  class DomainServiceStub(object):
    # missing associated documentation comment in .proto file
    pass

    def __init__(self, channel):
      """Constructor.

      Args:
        channel: A grpc.Channel.
      """
      self.GetDomains = channel.unary_unary(
          '/domainmessages.DomainService/GetDomains',
          request_serializer=GetDomainsRequest.SerializeToString,
          response_deserializer=GetDomainsResponse.FromString,
          )
      self.SuspendDomains = channel.unary_unary(
          '/domainmessages.DomainService/SuspendDomains',
          request_serializer=SuspendDomainsRequest.SerializeToString,
          response_deserializer=SuspendDomainsResponse.FromString,
          )
      self.UnSuspendDomains = channel.unary_unary(
          '/domainmessages.DomainService/UnSuspendDomains',
          request_serializer=UnSuspendDomainsRequest.SerializeToString,
          response_deserializer=UnSuspendDomainsResponse.FromString,
          )
      self.DomainInStatus = channel.unary_unary(
          '/domainmessages.DomainService/DomainInStatus',
          request_serializer=DomainInStatusRequest.SerializeToString,
          response_deserializer=DomainInStatusResponse.FromString,
          )


  class DomainServiceServicer(object):
    # missing associated documentation comment in .proto file
    pass

    def GetDomains(self, request, context):
      """Retrieves domains for the given shopper
      """
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')

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

    def DomainInStatus(self, request, context):
      """Determines if the given domain has a status code in the provided list
      """
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')


  def add_DomainServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'GetDomains': grpc.unary_unary_rpc_method_handler(
            servicer.GetDomains,
            request_deserializer=GetDomainsRequest.FromString,
            response_serializer=GetDomainsResponse.SerializeToString,
        ),
        'SuspendDomains': grpc.unary_unary_rpc_method_handler(
            servicer.SuspendDomains,
            request_deserializer=SuspendDomainsRequest.FromString,
            response_serializer=SuspendDomainsResponse.SerializeToString,
        ),
        'UnSuspendDomains': grpc.unary_unary_rpc_method_handler(
            servicer.UnSuspendDomains,
            request_deserializer=UnSuspendDomainsRequest.FromString,
            response_serializer=UnSuspendDomainsResponse.SerializeToString,
        ),
        'DomainInStatus': grpc.unary_unary_rpc_method_handler(
            servicer.DomainInStatus,
            request_deserializer=DomainInStatusRequest.FromString,
            response_serializer=DomainInStatusResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'domainmessages.DomainService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


  class BetaDomainServiceServicer(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    # missing associated documentation comment in .proto file
    pass
    def GetDomains(self, request, context):
      """Retrieves domains for the given shopper
      """
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def SuspendDomains(self, request, context):
      """Adds an abuse lock for a domain
      """
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def UnSuspendDomains(self, request, context):
      """Removes an abuse lock for a domain
      """
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
    def DomainInStatus(self, request, context):
      """Determines if the given domain has a status code in the provided list
      """
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)


  class BetaDomainServiceStub(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    # missing associated documentation comment in .proto file
    pass
    def GetDomains(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      """Retrieves domains for the given shopper
      """
      raise NotImplementedError()
    GetDomains.future = None
    def SuspendDomains(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      """Adds an abuse lock for a domain
      """
      raise NotImplementedError()
    SuspendDomains.future = None
    def UnSuspendDomains(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      """Removes an abuse lock for a domain
      """
      raise NotImplementedError()
    UnSuspendDomains.future = None
    def DomainInStatus(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      """Determines if the given domain has a status code in the provided list
      """
      raise NotImplementedError()
    DomainInStatus.future = None


  def beta_create_DomainService_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_deserializers = {
      ('domainmessages.DomainService', 'DomainInStatus'): DomainInStatusRequest.FromString,
      ('domainmessages.DomainService', 'GetDomains'): GetDomainsRequest.FromString,
      ('domainmessages.DomainService', 'SuspendDomains'): SuspendDomainsRequest.FromString,
      ('domainmessages.DomainService', 'UnSuspendDomains'): UnSuspendDomainsRequest.FromString,
    }
    response_serializers = {
      ('domainmessages.DomainService', 'DomainInStatus'): DomainInStatusResponse.SerializeToString,
      ('domainmessages.DomainService', 'GetDomains'): GetDomainsResponse.SerializeToString,
      ('domainmessages.DomainService', 'SuspendDomains'): SuspendDomainsResponse.SerializeToString,
      ('domainmessages.DomainService', 'UnSuspendDomains'): UnSuspendDomainsResponse.SerializeToString,
    }
    method_implementations = {
      ('domainmessages.DomainService', 'DomainInStatus'): face_utilities.unary_unary_inline(servicer.DomainInStatus),
      ('domainmessages.DomainService', 'GetDomains'): face_utilities.unary_unary_inline(servicer.GetDomains),
      ('domainmessages.DomainService', 'SuspendDomains'): face_utilities.unary_unary_inline(servicer.SuspendDomains),
      ('domainmessages.DomainService', 'UnSuspendDomains'): face_utilities.unary_unary_inline(servicer.UnSuspendDomains),
    }
    server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
    return beta_implementations.server(method_implementations, options=server_options)


  def beta_create_DomainService_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_serializers = {
      ('domainmessages.DomainService', 'DomainInStatus'): DomainInStatusRequest.SerializeToString,
      ('domainmessages.DomainService', 'GetDomains'): GetDomainsRequest.SerializeToString,
      ('domainmessages.DomainService', 'SuspendDomains'): SuspendDomainsRequest.SerializeToString,
      ('domainmessages.DomainService', 'UnSuspendDomains'): UnSuspendDomainsRequest.SerializeToString,
    }
    response_deserializers = {
      ('domainmessages.DomainService', 'DomainInStatus'): DomainInStatusResponse.FromString,
      ('domainmessages.DomainService', 'GetDomains'): GetDomainsResponse.FromString,
      ('domainmessages.DomainService', 'SuspendDomains'): SuspendDomainsResponse.FromString,
      ('domainmessages.DomainService', 'UnSuspendDomains'): UnSuspendDomainsResponse.FromString,
    }
    cardinalities = {
      'DomainInStatus': cardinality.Cardinality.UNARY_UNARY,
      'GetDomains': cardinality.Cardinality.UNARY_UNARY,
      'SuspendDomains': cardinality.Cardinality.UNARY_UNARY,
      'UnSuspendDomains': cardinality.Cardinality.UNARY_UNARY,
    }
    stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
    return beta_implementations.dynamic_stub(channel, 'domainmessages.DomainService', cardinalities, options=stub_options)
except ImportError:
  pass
# @@protoc_insertion_point(module_scope)
