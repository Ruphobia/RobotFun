# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: adder.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x61\x64\x64\x65r.proto\x12\x05\x61\x64\x64\x65r\".\n\nAddRequest\x12\x0f\n\x07number1\x18\x01 \x01(\x05\x12\x0f\n\x07number2\x18\x02 \x01(\x05\"\x17\n\x08\x41\x64\x64Reply\x12\x0b\n\x03sum\x18\x01 \x01(\x05\x32;\n\x05\x41\x64\x64\x65r\x12\x32\n\nAddNumbers\x12\x11.adder.AddRequest\x1a\x0f.adder.AddReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'adder_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ADDREQUEST']._serialized_start=22
  _globals['_ADDREQUEST']._serialized_end=68
  _globals['_ADDREPLY']._serialized_start=70
  _globals['_ADDREPLY']._serialized_end=93
  _globals['_ADDER']._serialized_start=95
  _globals['_ADDER']._serialized_end=154
# @@protoc_insertion_point(module_scope)