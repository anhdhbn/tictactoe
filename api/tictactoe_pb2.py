# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tictactoe.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tictactoe.proto',
  package='tictactoe',
  syntax='proto3',
  serialized_options=b'Z\rapi/tictactoe',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0ftictactoe.proto\x12\ttictactoe\"N\n\x0eMessageRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04init\x18\x02 \x01(\x08\x12\x0c\n\x04room\x18\x03 \x01(\t\x12\t\n\x01x\x18\x04 \x01(\x05\x12\t\n\x01y\x18\x05 \x01(\x05\"\xf8\x01\n\x0fMessageResponse\x12/\n\x05state\x18\x01 \x01(\x0e\x32 .tictactoe.MessageResponse.State\x12&\n\x03req\x18\x02 \x01(\x0b\x32\x19.tictactoe.MessageRequest\x12\x0b\n\x03isX\x18\x03 \x01(\x08\x12\x18\n\x10isCompetitorSend\x18\x04 \x01(\x08\"e\n\x05State\x12\t\n\x05\x44RAWN\x10\x00\x12\n\n\x06X_WINS\x10\x01\x12\n\n\x06O_WINS\x10\x02\x12\x10\n\x0cNOT_FINISHED\x10\x03\x12\x0b\n\x07WAITING\x10\x04\x12\r\n\tWAIT_TURN\x10\x05\x12\x0b\n\x07INVALID\x10\x06\x32T\n\tTictactoe\x12G\n\nPlayStream\x12\x19.tictactoe.MessageRequest\x1a\x1a.tictactoe.MessageResponse(\x01\x30\x01\x42\x0fZ\rapi/tictactoeb\x06proto3'
)



_MESSAGERESPONSE_STATE = _descriptor.EnumDescriptor(
  name='State',
  full_name='tictactoe.MessageResponse.State',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DRAWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='X_WINS', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='O_WINS', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NOT_FINISHED', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WAITING', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WAIT_TURN', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=258,
  serialized_end=359,
)
_sym_db.RegisterEnumDescriptor(_MESSAGERESPONSE_STATE)


_MESSAGEREQUEST = _descriptor.Descriptor(
  name='MessageRequest',
  full_name='tictactoe.MessageRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='tictactoe.MessageRequest.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='init', full_name='tictactoe.MessageRequest.init', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='room', full_name='tictactoe.MessageRequest.room', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='x', full_name='tictactoe.MessageRequest.x', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='y', full_name='tictactoe.MessageRequest.y', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=30,
  serialized_end=108,
)


_MESSAGERESPONSE = _descriptor.Descriptor(
  name='MessageResponse',
  full_name='tictactoe.MessageResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='tictactoe.MessageResponse.state', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='req', full_name='tictactoe.MessageResponse.req', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='isX', full_name='tictactoe.MessageResponse.isX', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='isCompetitorSend', full_name='tictactoe.MessageResponse.isCompetitorSend', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MESSAGERESPONSE_STATE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=111,
  serialized_end=359,
)

_MESSAGERESPONSE.fields_by_name['state'].enum_type = _MESSAGERESPONSE_STATE
_MESSAGERESPONSE.fields_by_name['req'].message_type = _MESSAGEREQUEST
_MESSAGERESPONSE_STATE.containing_type = _MESSAGERESPONSE
DESCRIPTOR.message_types_by_name['MessageRequest'] = _MESSAGEREQUEST
DESCRIPTOR.message_types_by_name['MessageResponse'] = _MESSAGERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MessageRequest = _reflection.GeneratedProtocolMessageType('MessageRequest', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGEREQUEST,
  '__module__' : 'tictactoe_pb2'
  # @@protoc_insertion_point(class_scope:tictactoe.MessageRequest)
  })
_sym_db.RegisterMessage(MessageRequest)

MessageResponse = _reflection.GeneratedProtocolMessageType('MessageResponse', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGERESPONSE,
  '__module__' : 'tictactoe_pb2'
  # @@protoc_insertion_point(class_scope:tictactoe.MessageResponse)
  })
_sym_db.RegisterMessage(MessageResponse)


DESCRIPTOR._options = None

_TICTACTOE = _descriptor.ServiceDescriptor(
  name='Tictactoe',
  full_name='tictactoe.Tictactoe',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=361,
  serialized_end=445,
  methods=[
  _descriptor.MethodDescriptor(
    name='PlayStream',
    full_name='tictactoe.Tictactoe.PlayStream',
    index=0,
    containing_service=None,
    input_type=_MESSAGEREQUEST,
    output_type=_MESSAGERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TICTACTOE)

DESCRIPTOR.services_by_name['Tictactoe'] = _TICTACTOE

# @@protoc_insertion_point(module_scope)