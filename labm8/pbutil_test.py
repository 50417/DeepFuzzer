"""Unit tests for //labm8:pbutil."""
import pathlib
import sys
import tempfile

import pytest
from absl import app

from labm8 import pbutil
from labm8.proto import test_protos_pb2


# A list of all of the filename suffixes to test each function with.
SUFFIXES_TO_TEST = [
  '', '.gz', '.txt', '.txt.gz', '.pbtxt', '.pbtxt.gz', '.json', '.json.gz',
  '.unknown-suffix', '.unknown-suffix.gz']


@pytest.fixture(scope='function')
def tempdir() -> pathlib.Path:
  """A pytest fixture for a temporary directory."""
  with tempfile.TemporaryDirectory(prefix='phd_') as d:
    yield pathlib.Path(d)


# ToFile() tests.

@pytest.mark.parametrize('suffix', SUFFIXES_TO_TEST)
def test_ToFile_message_missing_required_fields(suffix):
  """Test that EncodeError is raised if required field is not set."""
  with tempfile.NamedTemporaryFile(prefix='labm8_proto_',
                                   suffix=suffix) as f:
    proto = test_protos_pb2.TestMessage(number=1)
    with pytest.raises(pbutil.EncodeError):
      pbutil.ToFile(proto, pathlib.Path(f.name))


@pytest.mark.parametrize('suffix', SUFFIXES_TO_TEST)
def test_ToFile_parent_directory_does_not_exist(suffix):
  """Test that FileNotFoundError raised if parent directory doesn't exist."""
  with tempfile.TemporaryDirectory() as d:
    proto = test_protos_pb2.TestMessage(string='abc', number=1)
    with pytest.raises(FileNotFoundError):
      pbutil.ToFile(proto, pathlib.Path(d) / 'notadir' / f'proto{suffix}')


@pytest.mark.parametrize('suffix', SUFFIXES_TO_TEST)
def test_ToFile_path_is_directory(suffix):
  """Test that IsADirectoryError raised if path is a directory."""
  with tempfile.TemporaryDirectory(suffix=suffix) as d:
    proto = test_protos_pb2.TestMessage(string='abc', number=1)
    with pytest.raises(IsADirectoryError) as e_info:
      pbutil.ToFile(proto, pathlib.Path(d))
    assert str(e_info.value).endswith(f"Is a directory: '{d}'")


# FromString() tests.

def test_FromString_empty_string():
  """Test that an empty string can be parsed as a proto."""
  proto = pbutil.FromString('', test_protos_pb2.AnotherTestMessage())
  assert not proto.number


def test_FromString_empty_string_required_fields():
  """Test that an empty string raises DecodeError if uninitialized fields."""
  with pytest.raises(pbutil.DecodeError):
    pbutil.FromString('', test_protos_pb2.TestMessage())


def test_FromString_empty_string_required_fields_uninitialized_okay():
  """Test that an empty string raises DecodeError if uninitialized fields."""
  proto = pbutil.FromString(
      '', test_protos_pb2.TestMessage(), uninitialized_okay=True)
  assert not proto.string


def test_FromString_valid_input():
  """Test that an valid input is decoded."""
  proto = pbutil.FromString('number: 5', test_protos_pb2.AnotherTestMessage())
  assert 5 == proto.number


def test_FromString_DecodeError_unknown_field():
  """Test that DecodeError is raised if string contains unknown field."""
  with pytest.raises(pbutil.DecodeError) as e_info:
    proto = pbutil.FromString('foo: "bar"',
                              test_protos_pb2.AnotherTestMessage())
  assert ('1:1 : Message type "labm8.AnotherTestMessage" '
          'has no field named "foo".') == str(e_info.value)


# FromFile() tests.

@pytest.mark.parametrize('suffix', SUFFIXES_TO_TEST)
def test_FromFile_FileNotFoundError(suffix):
  """Test that FileNotFoundError raised if file doesn't exist."""
  with tempfile.TemporaryDirectory(prefix='labm8_proto_') as d:
    with pytest.raises(FileNotFoundError):
      pbutil.FromFile(pathlib.Path(d) / f'proto{suffix}',
                      test_protos_pb2.TestMessage())


@pytest.mark.parametrize('suffix', SUFFIXES_TO_TEST)
def test_FromFile_IsADirectoryError(suffix):
  """Test that IsADirectoryError raised if path is a directory."""
  with tempfile.TemporaryDirectory(prefix='labm8_proto_', suffix=suffix) as d:
    with pytest.raises(IsADirectoryError):
      pbutil.FromFile(pathlib.Path(d), test_protos_pb2.TestMessage())


@pytest.mark.parametrize('suffix', SUFFIXES_TO_TEST)
def test_FromFile_required_fields_not_set(suffix):
  """Test that DecodeError raised if required fields not set."""
  with tempfile.NamedTemporaryFile(prefix='labm8_proto_',
                                   suffix=suffix) as f:
    pbutil.ToFile(test_protos_pb2.AnotherTestMessage(number=1),
                  pathlib.Path(f.name))
    with pytest.raises(pbutil.DecodeError) as e_info:
      pbutil.FromFile(pathlib.Path(f.name), test_protos_pb2.TestMessage())
    assert f"Required fields not set: '{f.name}'" == str(e_info.value)


@pytest.mark.parametrize('suffix', SUFFIXES_TO_TEST)
def test_FromFile_required_fields_not_set_uninitialized_okay(suffix):
  """Test that DecodeError not raised if required fields not set."""
  with tempfile.NamedTemporaryFile(prefix='labm8_proto_',
                                   suffix=suffix) as f:
    proto_in = test_protos_pb2.AnotherTestMessage(number=1)
    pbutil.ToFile(test_protos_pb2.AnotherTestMessage(number=1),
                  pathlib.Path(f.name))
    pbutil.FromFile(pathlib.Path(f.name), test_protos_pb2.TestMessage(),
                    uninitialized_okay=True)


@pytest.mark.parametrize('suffix', SUFFIXES_TO_TEST)
def test_ToFile_FromFile_equivalence(suffix):
  """Test that ToFile() and FromFile() are symmetrical."""
  with tempfile.TemporaryDirectory(prefix='labm8_proto_') as d:
    path = pathlib.Path(d) / f'proto{suffix}'
    proto_in = test_protos_pb2.TestMessage(string='abc', number=1)
    pbutil.ToFile(proto_in, path)
    assert path.is_file()
    proto_out = test_protos_pb2.TestMessage()
    pbutil.FromFile(path, proto_out)
    assert proto_out.string == 'abc'
    assert proto_out.number == 1
    assert proto_in == proto_out


# AssertFieldIsSet() tests.


def test_AssertFieldIsSet_invalid_field_name():
  """ValueError is raised if the requested field name does not exist."""
  t = test_protos_pb2.TestMessage()
  with pytest.raises(ValueError):
    pbutil.AssertFieldIsSet(t, 'not_a_real_field')


def test_AssertFieldIsSet_field_not_set():
  """ValueError is raised if the requested field is not set."""
  t = test_protos_pb2.TestMessage()
  with pytest.raises(pbutil.ProtoValueError) as e_info:
    pbutil.AssertFieldIsSet(t, 'string')
  assert "Field not set: 'TestMessage.string'" == str(e_info.value)
  with pytest.raises(pbutil.ProtoValueError) as e_info:
    pbutil.AssertFieldIsSet(t, 'number')
  assert "Field not set: 'TestMessage.number'" == str(e_info.value)


def test_AssertFieldIsSet_field_is_set():
  """Field value is returned when field is set."""
  t = test_protos_pb2.TestMessage()
  t.string = 'foo'
  t.number = 5
  assert 'foo' == pbutil.AssertFieldIsSet(t, 'string')
  assert 5 == pbutil.AssertFieldIsSet(t, 'number')


def test_AssertFieldIsSet_user_callback_custom_fail_message():
  """Test that the requested message is returned on callback fail."""
  t = test_protos_pb2.TestMessage()
  with pytest.raises(pbutil.ProtoValueError) as e_info:
    pbutil.AssertFieldIsSet(t, 'string', 'Hello, world!')
  assert 'Hello, world!' == str(e_info.value)
  with pytest.raises(pbutil.ProtoValueError) as e_info:
    pbutil.AssertFieldIsSet(t, 'number', fail_message='Hello, world!')
  assert 'Hello, world!' == str(e_info.value)


def test_AssFieldIsSet_oneof_field_no_return():
  """Test that no value is returned when a oneof field is set."""
  t = test_protos_pb2.TestMessage()
  t.option_a = 1
  assert pbutil.AssertFieldIsSet(t, 'union_field') is None
  assert 1 == pbutil.AssertFieldIsSet(t, 'option_a')


# AssertFieldConstraint() tests.

def test_AssertFieldConstraint_invalid_field_name():
  """ValueError is raised if the requested field name does not exist."""
  t = test_protos_pb2.TestMessage()
  with pytest.raises(ValueError):
    pbutil.AssertFieldConstraint(t, 'not_a_real_field')


def test_AssertFieldConstraint_field_not_set():
  """ValueError is raised if the requested field is not set."""
  t = test_protos_pb2.TestMessage()
  with pytest.raises(pbutil.ProtoValueError) as e_info:
    pbutil.AssertFieldConstraint(t, 'string')
  assert "Field not set: 'TestMessage.string'" == str(e_info.value)
  with pytest.raises(pbutil.ProtoValueError) as e_info:
    pbutil.AssertFieldConstraint(t, 'number')
  assert "Field not set: 'TestMessage.number'" == str(e_info.value)


def test_AssertFieldConstraint_no_callback_return_value():
  """Field value is returned when no callback and field is set."""
  t = test_protos_pb2.TestMessage()
  t.string = 'foo'
  t.number = 5
  assert 'foo' == pbutil.AssertFieldConstraint(t, 'string')
  assert 5 == pbutil.AssertFieldConstraint(t, 'number')


def test_AssertFieldConstraint_user_callback_passes():
  """Field value is returned when user callback passes."""
  t = test_protos_pb2.TestMessage()
  t.string = 'foo'
  t.number = 5
  assert 'foo' == pbutil.AssertFieldConstraint(t, 'string',
                                               lambda x: x == 'foo')
  assert 5 == pbutil.AssertFieldConstraint(t, 'number', lambda x: 1 < x < 10)


def test_AssertFieldConstraint_user_callback_fails():
  """ProtoValueError raised when when user callback fails."""
  t = test_protos_pb2.TestMessage()
  t.string = 'foo'
  t.number = 5
  with pytest.raises(pbutil.ProtoValueError) as e_info:
    pbutil.AssertFieldConstraint(t, 'string', lambda x: x == 'bar')
  assert "Field fails constraint check: 'TestMessage.string'" == str(
      e_info.value)
  with pytest.raises(pbutil.ProtoValueError) as e_info:
    pbutil.AssertFieldConstraint(t, 'number', lambda x: 10 < x < 100)
  assert "Field fails constraint check: 'TestMessage.number'" == str(
      e_info.value)


def test_AssertFieldConstraint_user_callback_raises_exception():
  """If callback raises exception, it is passed to calling code."""
  t = test_protos_pb2.TestMessage()
  t.string = 'foo'

  def CallbackWhichRaisesException(x):
    """Test callback which raises an exception"""
    raise FileExistsError('foo')

  with pytest.raises(FileExistsError) as e_info:
    pbutil.AssertFieldConstraint(t, 'string', CallbackWhichRaisesException)
  assert str(e_info.value) == 'foo'


def test_AssertFieldConstraint_user_callback_custom_fail_message():
  """Test that the requested message is returned on callback fail."""
  t = test_protos_pb2.TestMessage()
  t.string = 'foo'

  # Constraint function fails.
  with pytest.raises(pbutil.ProtoValueError) as e_info:
    pbutil.AssertFieldConstraint(t, 'string', lambda x: x == 'bar',
                                 'Hello, world!')
  assert 'Hello, world!' == str(e_info.value)

  # Field not set.
  with pytest.raises(pbutil.ProtoValueError) as e_info:
    pbutil.AssertFieldConstraint(t, 'number', fail_message='Hello, world!')
  assert 'Hello, world!' == str(e_info.value)


# ProtoBackedMixin tests.

class TestMessage(pbutil.ProtoBackedMixin):
  """Example class which implements ProtoBackedMixin interface."""
  proto_t = test_protos_pb2.TestMessage

  def __init__(self, string: str, number: int):
    self.string = string
    self.number = number

  def SetProto(self, proto: test_protos_pb2.TestMessage) -> None:
    """Set a protocol buffer representation."""
    proto.string = self.string
    proto.number = self.number

  @staticmethod
  def FromProto(proto) -> 'TestMessage':
    """Instantiate an object from protocol buffer message."""
    return TestMessage(proto.string, proto.number)


def test_ProtoBackedMixin_FromProto():
  """Test FromProto constructor for proto backed class."""
  proto = test_protos_pb2.TestMessage(string="Hello, world!", number=42)
  instance = TestMessage.FromProto(proto)
  assert instance.string == "Hello, world!"
  assert instance.number == 42


def test_ProtoBackedMixin_SetProto():
  """Test SetProto method for proto backed class."""
  proto = test_protos_pb2.TestMessage()
  TestMessage(string="Hello, world!", number=42).SetProto(proto)
  assert proto.string == "Hello, world!"
  assert proto.number == 42


def test_ProtoBackedMixin_ToProto():
  """Test FromProto constructor for proto backed class."""
  instance = TestMessage(string="Hello, world!", number=42)
  proto = instance.ToProto()
  assert proto.string == "Hello, world!"
  assert proto.number == 42


@pytest.mark.parametrize('suffix', SUFFIXES_TO_TEST)
def test_ProtoBackedMixin_FromProtoFile(suffix: str, tempdir: pathlib.Path):
  """Test FromProtoFile constructor for proto backed class."""
  proto_path = tempdir / f'proto{suffix}'
  pbutil.ToFile(test_protos_pb2.TestMessage(string="Hello, world!", number=42),
                proto_path)

  instance = TestMessage.FromProtoFile(proto_path)
  assert instance.string == "Hello, world!"
  assert instance.number == 42


def main(argv):
  del argv
  sys.exit(pytest.main([__file__, '-vv']))


if __name__ == '__main__':
  app.run(main)
