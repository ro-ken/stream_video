# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: stream_video.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='stream_video.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x12stream_video.proto\"$\n\x05\x46ream\x12\x0c\n\x04size\x18\x01 \x01(\x05\x12\r\n\x05\x66ream\x18\x02 \x01(\x0c\"$\n\x05\x46rame\x12\x0c\n\x04size\x18\x01 \x01(\x05\x12\r\n\x05\x66rame\x18\x02 \x01(\x0c\"\x08\n\x06Result2\xb9\x01\n\x0bVideoStream\x12\x1e\n\tSendFream\x12\x06.Fream\x1a\x07.Result\"\x00\x12!\n\nPushStream\x12\x06.Fream\x1a\x07.Result\"\x00(\x01\x12#\n\x0bPushAndPull\x12\x06.Fream\x1a\x06.Fream\"\x00(\x01\x30\x01\x12$\n\rFaceDetection\x12\x06.Frame\x1a\x07.Result\"\x00(\x01\x12\x1c\n\x05\x43\x61nny\x12\x06.Frame\x1a\x07.Result\"\x00(\x01\x62\x06proto3'
)




_FREAM = _descriptor.Descriptor(
  name='Fream',
  full_name='Fream',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='size', full_name='Fream.size', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fream', full_name='Fream.fream', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
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
  serialized_start=22,
  serialized_end=58,
)


_FRAME = _descriptor.Descriptor(
  name='Frame',
  full_name='Frame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='size', full_name='Frame.size', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='frame', full_name='Frame.frame', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
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
  serialized_start=60,
  serialized_end=96,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=98,
  serialized_end=106,
)

DESCRIPTOR.message_types_by_name['Fream'] = _FREAM
DESCRIPTOR.message_types_by_name['Frame'] = _FRAME
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Fream = _reflection.GeneratedProtocolMessageType('Fream', (_message.Message,), {
  'DESCRIPTOR' : _FREAM,
  '__module__' : 'stream_video_pb2'
  # @@protoc_insertion_point(class_scope:Fream)
  })
_sym_db.RegisterMessage(Fream)

Frame = _reflection.GeneratedProtocolMessageType('Frame', (_message.Message,), {
  'DESCRIPTOR' : _FRAME,
  '__module__' : 'stream_video_pb2'
  # @@protoc_insertion_point(class_scope:Frame)
  })
_sym_db.RegisterMessage(Frame)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), {
  'DESCRIPTOR' : _RESULT,
  '__module__' : 'stream_video_pb2'
  # @@protoc_insertion_point(class_scope:Result)
  })
_sym_db.RegisterMessage(Result)



_VIDEOSTREAM = _descriptor.ServiceDescriptor(
  name='VideoStream',
  full_name='VideoStream',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=109,
  serialized_end=294,
  methods=[
  _descriptor.MethodDescriptor(
    name='SendFream',
    full_name='VideoStream.SendFream',
    index=0,
    containing_service=None,
    input_type=_FREAM,
    output_type=_RESULT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='PushStream',
    full_name='VideoStream.PushStream',
    index=1,
    containing_service=None,
    input_type=_FREAM,
    output_type=_RESULT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='PushAndPull',
    full_name='VideoStream.PushAndPull',
    index=2,
    containing_service=None,
    input_type=_FREAM,
    output_type=_FREAM,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='FaceDetection',
    full_name='VideoStream.FaceDetection',
    index=3,
    containing_service=None,
    input_type=_FRAME,
    output_type=_RESULT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Canny',
    full_name='VideoStream.Canny',
    index=4,
    containing_service=None,
    input_type=_FRAME,
    output_type=_RESULT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_VIDEOSTREAM)

DESCRIPTOR.services_by_name['VideoStream'] = _VIDEOSTREAM

# @@protoc_insertion_point(module_scope)
