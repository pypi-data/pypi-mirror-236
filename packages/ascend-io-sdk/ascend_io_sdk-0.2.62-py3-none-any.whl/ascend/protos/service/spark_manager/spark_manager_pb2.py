# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ascend/protos/service/spark_manager/spark_manager.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from ascend.protos.core import core_pb2 as ascend_dot_protos_dot_core_dot_core__pb2
from ascend.protos.environment import environment_pb2 as ascend_dot_protos_dot_environment_dot_environment__pb2
from ascend.protos.fault import fault_pb2 as ascend_dot_protos_dot_fault_dot_fault__pb2
from ascend.protos.task import task_pb2 as ascend_dot_protos_dot_task_dot_task__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ascend/protos/service/spark_manager/spark_manager.proto',
  package='spark_manager',
  syntax='proto3',
  serialized_options=b'\n&io.ascend.protos.service.spark_managerP\001\240\001\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n7ascend/protos/service/spark_manager/spark_manager.proto\x12\rspark_manager\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1d\x61scend/protos/core/core.proto\x1a+ascend/protos/environment/environment.proto\x1a\x1f\x61scend/protos/fault/fault.proto\x1a\x1d\x61scend/protos/task/task.proto\"o\n\x07TaskRun\x1a\x64\n\x08Response\x1aX\n\x03Try\x12)\n\x07success\x18\x01 \x01(\x0b\x32\x16.google.protobuf.EmptyH\x00\x12\x1f\n\x07\x66\x61ilure\x18\x02 \x01(\x0b\x32\x0c.fault.FaultH\x00\x42\x05\n\x03try\"\xa1\x01\n\x10SparkClusterPool\x1a\x8c\x01\n\x06Status\x1a\"\n\x07Request\x12\x17\n\x0f\x63luster_pool_id\x18\x01 \x01(\t\x1a^\n\x08Response\x12\x17\n\x0f\x63luster_pool_id\x18\x01 \x01(\t\x12\x39\n\x10\x63luster_statuses\x18\x02 \x03(\x0b\x32\x1f.environment.SparkClusterStatus2\xc1\x01\n\x0bTaskService\x12\x1e\n\x04Ping\x12\n.core.Ping\x1a\n.core.Pong\x12:\n\x07RunTask\x12\n.task.Task\x1a#.spark_manager.TaskRun.Response.Try\x12&\n\tTaskState\x12\x08.task.Id\x1a\x0f.task.State.Try\x12.\n\nCancelTask\x12\x08.task.Id\x1a\x16.google.protobuf.Empty2\xb0\x01\n\x18\x43lusterPoolStatusService\x12\x1e\n\x04Ping\x12\n.core.Ping\x1a\n.core.Pong\x12t\n\x11\x43lusterPoolStatus\x12..spark_manager.SparkClusterPool.Status.Request\x1a/.spark_manager.SparkClusterPool.Status.ResponseB-\n&io.ascend.protos.service.spark_managerP\x01\xa0\x01\x01\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,ascend_dot_protos_dot_core_dot_core__pb2.DESCRIPTOR,ascend_dot_protos_dot_environment_dot_environment__pb2.DESCRIPTOR,ascend_dot_protos_dot_fault_dot_fault__pb2.DESCRIPTOR,ascend_dot_protos_dot_task_dot_task__pb2.DESCRIPTOR,])




_TASKRUN_RESPONSE_TRY = _descriptor.Descriptor(
  name='Try',
  full_name='spark_manager.TaskRun.Response.Try',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='spark_manager.TaskRun.Response.Try.success', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='failure', full_name='spark_manager.TaskRun.Response.Try.failure', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
    _descriptor.OneofDescriptor(
      name='try', full_name='spark_manager.TaskRun.Response.Try.try',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=266,
  serialized_end=354,
)

_TASKRUN_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='spark_manager.TaskRun.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[_TASKRUN_RESPONSE_TRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=254,
  serialized_end=354,
)

_TASKRUN = _descriptor.Descriptor(
  name='TaskRun',
  full_name='spark_manager.TaskRun',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[_TASKRUN_RESPONSE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=243,
  serialized_end=354,
)


_SPARKCLUSTERPOOL_STATUS_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='spark_manager.SparkClusterPool.Status.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_pool_id', full_name='spark_manager.SparkClusterPool.Status.Request.cluster_pool_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=388,
  serialized_end=422,
)

_SPARKCLUSTERPOOL_STATUS_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='spark_manager.SparkClusterPool.Status.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cluster_pool_id', full_name='spark_manager.SparkClusterPool.Status.Response.cluster_pool_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cluster_statuses', full_name='spark_manager.SparkClusterPool.Status.Response.cluster_statuses', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=424,
  serialized_end=518,
)

_SPARKCLUSTERPOOL_STATUS = _descriptor.Descriptor(
  name='Status',
  full_name='spark_manager.SparkClusterPool.Status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[_SPARKCLUSTERPOOL_STATUS_REQUEST, _SPARKCLUSTERPOOL_STATUS_RESPONSE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=378,
  serialized_end=518,
)

_SPARKCLUSTERPOOL = _descriptor.Descriptor(
  name='SparkClusterPool',
  full_name='spark_manager.SparkClusterPool',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[_SPARKCLUSTERPOOL_STATUS, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=357,
  serialized_end=518,
)

_TASKRUN_RESPONSE_TRY.fields_by_name['success'].message_type = google_dot_protobuf_dot_empty__pb2._EMPTY
_TASKRUN_RESPONSE_TRY.fields_by_name['failure'].message_type = ascend_dot_protos_dot_fault_dot_fault__pb2._FAULT
_TASKRUN_RESPONSE_TRY.containing_type = _TASKRUN_RESPONSE
_TASKRUN_RESPONSE_TRY.oneofs_by_name['try'].fields.append(
  _TASKRUN_RESPONSE_TRY.fields_by_name['success'])
_TASKRUN_RESPONSE_TRY.fields_by_name['success'].containing_oneof = _TASKRUN_RESPONSE_TRY.oneofs_by_name['try']
_TASKRUN_RESPONSE_TRY.oneofs_by_name['try'].fields.append(
  _TASKRUN_RESPONSE_TRY.fields_by_name['failure'])
_TASKRUN_RESPONSE_TRY.fields_by_name['failure'].containing_oneof = _TASKRUN_RESPONSE_TRY.oneofs_by_name['try']
_TASKRUN_RESPONSE.containing_type = _TASKRUN
_SPARKCLUSTERPOOL_STATUS_REQUEST.containing_type = _SPARKCLUSTERPOOL_STATUS
_SPARKCLUSTERPOOL_STATUS_RESPONSE.fields_by_name['cluster_statuses'].message_type = ascend_dot_protos_dot_environment_dot_environment__pb2._SPARKCLUSTERSTATUS
_SPARKCLUSTERPOOL_STATUS_RESPONSE.containing_type = _SPARKCLUSTERPOOL_STATUS
_SPARKCLUSTERPOOL_STATUS.containing_type = _SPARKCLUSTERPOOL
DESCRIPTOR.message_types_by_name['TaskRun'] = _TASKRUN
DESCRIPTOR.message_types_by_name['SparkClusterPool'] = _SPARKCLUSTERPOOL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TaskRun = _reflection.GeneratedProtocolMessageType('TaskRun', (_message.Message,), {

  'Response' : _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {

    'Try' : _reflection.GeneratedProtocolMessageType('Try', (_message.Message,), {
      'DESCRIPTOR' : _TASKRUN_RESPONSE_TRY,
      '__module__' : 'ascend.protos.service.spark_manager.spark_manager_pb2'
      # @@protoc_insertion_point(class_scope:spark_manager.TaskRun.Response.Try)
      })
    ,
    'DESCRIPTOR' : _TASKRUN_RESPONSE,
    '__module__' : 'ascend.protos.service.spark_manager.spark_manager_pb2'
    # @@protoc_insertion_point(class_scope:spark_manager.TaskRun.Response)
    })
  ,
  'DESCRIPTOR' : _TASKRUN,
  '__module__' : 'ascend.protos.service.spark_manager.spark_manager_pb2'
  # @@protoc_insertion_point(class_scope:spark_manager.TaskRun)
  })
_sym_db.RegisterMessage(TaskRun)
_sym_db.RegisterMessage(TaskRun.Response)
_sym_db.RegisterMessage(TaskRun.Response.Try)

SparkClusterPool = _reflection.GeneratedProtocolMessageType('SparkClusterPool', (_message.Message,), {

  'Status' : _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), {

    'Request' : _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
      'DESCRIPTOR' : _SPARKCLUSTERPOOL_STATUS_REQUEST,
      '__module__' : 'ascend.protos.service.spark_manager.spark_manager_pb2'
      # @@protoc_insertion_point(class_scope:spark_manager.SparkClusterPool.Status.Request)
      })
    ,

    'Response' : _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
      'DESCRIPTOR' : _SPARKCLUSTERPOOL_STATUS_RESPONSE,
      '__module__' : 'ascend.protos.service.spark_manager.spark_manager_pb2'
      # @@protoc_insertion_point(class_scope:spark_manager.SparkClusterPool.Status.Response)
      })
    ,
    'DESCRIPTOR' : _SPARKCLUSTERPOOL_STATUS,
    '__module__' : 'ascend.protos.service.spark_manager.spark_manager_pb2'
    # @@protoc_insertion_point(class_scope:spark_manager.SparkClusterPool.Status)
    })
  ,
  'DESCRIPTOR' : _SPARKCLUSTERPOOL,
  '__module__' : 'ascend.protos.service.spark_manager.spark_manager_pb2'
  # @@protoc_insertion_point(class_scope:spark_manager.SparkClusterPool)
  })
_sym_db.RegisterMessage(SparkClusterPool)
_sym_db.RegisterMessage(SparkClusterPool.Status)
_sym_db.RegisterMessage(SparkClusterPool.Status.Request)
_sym_db.RegisterMessage(SparkClusterPool.Status.Response)


DESCRIPTOR._options = None

_TASKSERVICE = _descriptor.ServiceDescriptor(
  name='TaskService',
  full_name='spark_manager.TaskService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=521,
  serialized_end=714,
  methods=[
  _descriptor.MethodDescriptor(
    name='Ping',
    full_name='spark_manager.TaskService.Ping',
    index=0,
    containing_service=None,
    input_type=ascend_dot_protos_dot_core_dot_core__pb2._PING,
    output_type=ascend_dot_protos_dot_core_dot_core__pb2._PONG,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='RunTask',
    full_name='spark_manager.TaskService.RunTask',
    index=1,
    containing_service=None,
    input_type=ascend_dot_protos_dot_task_dot_task__pb2._TASK,
    output_type=_TASKRUN_RESPONSE_TRY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='TaskState',
    full_name='spark_manager.TaskService.TaskState',
    index=2,
    containing_service=None,
    input_type=ascend_dot_protos_dot_task_dot_task__pb2._ID,
    output_type=ascend_dot_protos_dot_task_dot_task__pb2._STATE_TRY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CancelTask',
    full_name='spark_manager.TaskService.CancelTask',
    index=3,
    containing_service=None,
    input_type=ascend_dot_protos_dot_task_dot_task__pb2._ID,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TASKSERVICE)

DESCRIPTOR.services_by_name['TaskService'] = _TASKSERVICE


_CLUSTERPOOLSTATUSSERVICE = _descriptor.ServiceDescriptor(
  name='ClusterPoolStatusService',
  full_name='spark_manager.ClusterPoolStatusService',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=717,
  serialized_end=893,
  methods=[
  _descriptor.MethodDescriptor(
    name='Ping',
    full_name='spark_manager.ClusterPoolStatusService.Ping',
    index=0,
    containing_service=None,
    input_type=ascend_dot_protos_dot_core_dot_core__pb2._PING,
    output_type=ascend_dot_protos_dot_core_dot_core__pb2._PONG,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ClusterPoolStatus',
    full_name='spark_manager.ClusterPoolStatusService.ClusterPoolStatus',
    index=1,
    containing_service=None,
    input_type=_SPARKCLUSTERPOOL_STATUS_REQUEST,
    output_type=_SPARKCLUSTERPOOL_STATUS_RESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_CLUSTERPOOLSTATUSSERVICE)

DESCRIPTOR.services_by_name['ClusterPoolStatusService'] = _CLUSTERPOOLSTATUSSERVICE

# @@protoc_insertion_point(module_scope)
