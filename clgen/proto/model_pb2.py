# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: clgen/proto/model.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from clgen.proto import corpus_pb2 as clgen_dot_proto_dot_corpus__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='clgen/proto/model.proto',
  package='clgen',
  syntax='proto2',
  serialized_options=_b('\n\022clgen'),
  serialized_pb=_b('\n\x17\x63lgen/proto/model.proto\x12\x05\x63lgen\x1a\x18\x63lgen/proto/corpus.proto\"\x82\x01\n\x05Model\x12\x1d\n\x06\x63orpus\x18\x01 \x01(\x0b\x32\r.clgen.Corpus\x12\x30\n\x0c\x61rchitecture\x18\x02 \x01(\x0b\x32\x1a.clgen.NetworkArchitecture\x12(\n\x08training\x18\x03 \x01(\x0b\x32\x16.clgen.TrainingOptions\"\xc0\x02\n\x13NetworkArchitecture\x12\x33\n\x07\x62\x61\x63kend\x18\x01 \x01(\x0e\x32\".clgen.NetworkArchitecture.Backend\x12\x16\n\x0e\x65mbedding_size\x18\x02 \x01(\x05\x12:\n\x0bneuron_type\x18\x03 \x01(\x0e\x32%.clgen.NetworkArchitecture.NeuronType\x12\x19\n\x11neurons_per_layer\x18\x04 \x01(\x05\x12\x12\n\nnum_layers\x18\x05 \x01(\x05\x12!\n\x19post_layer_dropout_micros\x18\x06 \x01(\x05\"$\n\x07\x42\x61\x63kend\x12\x0e\n\nTENSORFLOW\x10\x00\x12\t\n\x05KERAS\x10\x01\"(\n\nNeuronType\x12\x08\n\x04LSTM\x10\x00\x12\x07\n\x03RNN\x10\x01\x12\x07\n\x03GRU\x10\x02\"\xf9\x01\n\x0fTrainingOptions\x12\x12\n\nnum_epochs\x18\x01 \x01(\x05\x12\x17\n\x0fsequence_length\x18\x02 \x01(\x05\x12\x32\n*shuffle_corpus_contentfiles_between_epochs\x18\x03 \x01(\x08\x12\x12\n\nbatch_size\x18\x04 \x01(\x05\x12.\n\x0e\x61\x64\x61m_optimizer\x18\n \x01(\x0b\x32\x14.clgen.AdamOptimizerH\x00\x12\x34\n\x11rmsprop_optimizer\x18\x0b \x01(\x0b\x32\x17.clgen.RmsPropOptimizerH\x00\x42\x0b\n\toptimizer\"\xba\x01\n\rAdamOptimizer\x12$\n\x1cinitial_learning_rate_micros\x18\x01 \x01(\x05\x12,\n$learning_rate_decay_per_epoch_micros\x18\x02 \x01(\x05\x12\x15\n\rbeta_1_micros\x18\x03 \x01(\x05\x12\x15\n\rbeta_2_micros\x18\x04 \x01(\x05\x12\'\n\x1fnormalized_gradient_clip_micros\x18\x05 \x01(\x05\"f\n\x10RmsPropOptimizer\x12$\n\x1cinitial_learning_rate_micros\x18\x01 \x01(\x05\x12,\n$learning_rate_decay_per_epoch_micros\x18\x02 \x01(\x05\"{\n\x06Sample\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x16\n\x0esample_time_ms\x18\x02 \x01(\x05\x12\x14\n\x0cwall_time_ms\x18\x03 \x01(\x05\x12!\n\x19sample_start_epoch_ms_utc\x18\x04 \x01(\x03\x12\x12\n\nnum_tokens\x18\x05 \x01(\x05\x42\x14\n\x12\x64\x65\x65plearning.clgen')
  ,
  dependencies=[clgen_dot_proto_dot_corpus__pb2.DESCRIPTOR,])



_NETWORKARCHITECTURE_BACKEND = _descriptor.EnumDescriptor(
  name='Backend',
  full_name='clgen.NetworkArchitecture.Backend',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TENSORFLOW', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='KERAS', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=436,
  serialized_end=472,
)
_sym_db.RegisterEnumDescriptor(_NETWORKARCHITECTURE_BACKEND)

_NETWORKARCHITECTURE_NEURONTYPE = _descriptor.EnumDescriptor(
  name='NeuronType',
  full_name='clgen.NetworkArchitecture.NeuronType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LSTM', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RNN', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GRU', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=474,
  serialized_end=514,
)
_sym_db.RegisterEnumDescriptor(_NETWORKARCHITECTURE_NEURONTYPE)


_MODEL = _descriptor.Descriptor(
  name='Model',
  full_name='clgen.Model',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='corpus', full_name='clgen.Model.corpus', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='architecture', full_name='clgen.Model.architecture', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='training', full_name='clgen.Model.training', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=61,
  serialized_end=191,
)


_NETWORKARCHITECTURE = _descriptor.Descriptor(
  name='NetworkArchitecture',
  full_name='clgen.NetworkArchitecture',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='backend', full_name='clgen.NetworkArchitecture.backend', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='embedding_size', full_name='clgen.NetworkArchitecture.embedding_size', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='neuron_type', full_name='clgen.NetworkArchitecture.neuron_type', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='neurons_per_layer', full_name='clgen.NetworkArchitecture.neurons_per_layer', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='num_layers', full_name='clgen.NetworkArchitecture.num_layers', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='post_layer_dropout_micros', full_name='clgen.NetworkArchitecture.post_layer_dropout_micros', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _NETWORKARCHITECTURE_BACKEND,
    _NETWORKARCHITECTURE_NEURONTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=194,
  serialized_end=514,
)


_TRAININGOPTIONS = _descriptor.Descriptor(
  name='TrainingOptions',
  full_name='clgen.TrainingOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='num_epochs', full_name='clgen.TrainingOptions.num_epochs', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sequence_length', full_name='clgen.TrainingOptions.sequence_length', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shuffle_corpus_contentfiles_between_epochs', full_name='clgen.TrainingOptions.shuffle_corpus_contentfiles_between_epochs', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='batch_size', full_name='clgen.TrainingOptions.batch_size', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='adam_optimizer', full_name='clgen.TrainingOptions.adam_optimizer', index=4,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rmsprop_optimizer', full_name='clgen.TrainingOptions.rmsprop_optimizer', index=5,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='optimizer', full_name='clgen.TrainingOptions.optimizer',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=517,
  serialized_end=766,
)


_ADAMOPTIMIZER = _descriptor.Descriptor(
  name='AdamOptimizer',
  full_name='clgen.AdamOptimizer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='initial_learning_rate_micros', full_name='clgen.AdamOptimizer.initial_learning_rate_micros', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='learning_rate_decay_per_epoch_micros', full_name='clgen.AdamOptimizer.learning_rate_decay_per_epoch_micros', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='beta_1_micros', full_name='clgen.AdamOptimizer.beta_1_micros', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='beta_2_micros', full_name='clgen.AdamOptimizer.beta_2_micros', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='normalized_gradient_clip_micros', full_name='clgen.AdamOptimizer.normalized_gradient_clip_micros', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=769,
  serialized_end=955,
)


_RMSPROPOPTIMIZER = _descriptor.Descriptor(
  name='RmsPropOptimizer',
  full_name='clgen.RmsPropOptimizer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='initial_learning_rate_micros', full_name='clgen.RmsPropOptimizer.initial_learning_rate_micros', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='learning_rate_decay_per_epoch_micros', full_name='clgen.RmsPropOptimizer.learning_rate_decay_per_epoch_micros', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=957,
  serialized_end=1059,
)


_SAMPLE = _descriptor.Descriptor(
  name='Sample',
  full_name='clgen.Sample',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='text', full_name='clgen.Sample.text', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sample_time_ms', full_name='clgen.Sample.sample_time_ms', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='wall_time_ms', full_name='clgen.Sample.wall_time_ms', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sample_start_epoch_ms_utc', full_name='clgen.Sample.sample_start_epoch_ms_utc', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='num_tokens', full_name='clgen.Sample.num_tokens', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1061,
  serialized_end=1184,
)

_MODEL.fields_by_name['corpus'].message_type = clgen_dot_proto_dot_corpus__pb2._CORPUS
_MODEL.fields_by_name['architecture'].message_type = _NETWORKARCHITECTURE
_MODEL.fields_by_name['training'].message_type = _TRAININGOPTIONS
_NETWORKARCHITECTURE.fields_by_name['backend'].enum_type = _NETWORKARCHITECTURE_BACKEND
_NETWORKARCHITECTURE.fields_by_name['neuron_type'].enum_type = _NETWORKARCHITECTURE_NEURONTYPE
_NETWORKARCHITECTURE_BACKEND.containing_type = _NETWORKARCHITECTURE
_NETWORKARCHITECTURE_NEURONTYPE.containing_type = _NETWORKARCHITECTURE
_TRAININGOPTIONS.fields_by_name['adam_optimizer'].message_type = _ADAMOPTIMIZER
_TRAININGOPTIONS.fields_by_name['rmsprop_optimizer'].message_type = _RMSPROPOPTIMIZER
_TRAININGOPTIONS.oneofs_by_name['optimizer'].fields.append(
  _TRAININGOPTIONS.fields_by_name['adam_optimizer'])
_TRAININGOPTIONS.fields_by_name['adam_optimizer'].containing_oneof = _TRAININGOPTIONS.oneofs_by_name['optimizer']
_TRAININGOPTIONS.oneofs_by_name['optimizer'].fields.append(
  _TRAININGOPTIONS.fields_by_name['rmsprop_optimizer'])
_TRAININGOPTIONS.fields_by_name['rmsprop_optimizer'].containing_oneof = _TRAININGOPTIONS.oneofs_by_name['optimizer']
DESCRIPTOR.message_types_by_name['Model'] = _MODEL
DESCRIPTOR.message_types_by_name['NetworkArchitecture'] = _NETWORKARCHITECTURE
DESCRIPTOR.message_types_by_name['TrainingOptions'] = _TRAININGOPTIONS
DESCRIPTOR.message_types_by_name['AdamOptimizer'] = _ADAMOPTIMIZER
DESCRIPTOR.message_types_by_name['RmsPropOptimizer'] = _RMSPROPOPTIMIZER
DESCRIPTOR.message_types_by_name['Sample'] = _SAMPLE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Model = _reflection.GeneratedProtocolMessageType('Model', (_message.Message,), dict(
  DESCRIPTOR = _MODEL,
  __module__ = 'clgen.proto.model_pb2'
  # @@protoc_insertion_point(class_scope:clgen.Model)
  ))
_sym_db.RegisterMessage(Model)

NetworkArchitecture = _reflection.GeneratedProtocolMessageType('NetworkArchitecture', (_message.Message,), dict(
  DESCRIPTOR = _NETWORKARCHITECTURE,
  __module__ = 'clgen.proto.model_pb2'
  # @@protoc_insertion_point(class_scope:clgen.NetworkArchitecture)
  ))
_sym_db.RegisterMessage(NetworkArchitecture)

TrainingOptions = _reflection.GeneratedProtocolMessageType('TrainingOptions', (_message.Message,), dict(
  DESCRIPTOR = _TRAININGOPTIONS,
  __module__ = 'clgen.proto.model_pb2'
  # @@protoc_insertion_point(class_scope:clgen.TrainingOptions)
  ))
_sym_db.RegisterMessage(TrainingOptions)

AdamOptimizer = _reflection.GeneratedProtocolMessageType('AdamOptimizer', (_message.Message,), dict(
  DESCRIPTOR = _ADAMOPTIMIZER,
  __module__ = 'clgen.proto.model_pb2'
  # @@protoc_insertion_point(class_scope:clgen.AdamOptimizer)
  ))
_sym_db.RegisterMessage(AdamOptimizer)

RmsPropOptimizer = _reflection.GeneratedProtocolMessageType('RmsPropOptimizer', (_message.Message,), dict(
  DESCRIPTOR = _RMSPROPOPTIMIZER,
  __module__ = 'clgen.proto.model_pb2'
  # @@protoc_insertion_point(class_scope:clgen.RmsPropOptimizer)
  ))
_sym_db.RegisterMessage(RmsPropOptimizer)

Sample = _reflection.GeneratedProtocolMessageType('Sample', (_message.Message,), dict(
  DESCRIPTOR = _SAMPLE,
  __module__ = 'clgen.proto.model_pb2'
  # @@protoc_insertion_point(class_scope:clgen.Sample)
  ))
_sym_db.RegisterMessage(Sample)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
