"""Unit tests for //deeplearning/clgen/cli.py."""
import os
import pathlib
import sys
import tempfile

import pytest
from absl import app
from absl import flags

from deeplearning.clgen import clgen
from deeplearning.clgen import errors
from deeplearning.clgen.proto import clgen_pb2
from labm8 import pbutil


FLAGS = flags.FLAGS


# Instance tests.


def test_Instance_no_working_dir_field(abc_instance_config):
  """Test that working_dir is None when no working_dir field in config."""
  abc_instance_config.ClearField('working_dir')
  instance = clgen.Instance(abc_instance_config)
  assert instance.working_dir is None


def test_Instance_working_dir_shell_variable_expansion(abc_instance_config):
  """Test that shell variables are expanded in working_dir."""
  working_dir = abc_instance_config.working_dir
  os.environ['FOO'] = working_dir
  abc_instance_config.working_dir = '$FOO/'
  instance = clgen.Instance(abc_instance_config)
  assert str(instance.working_dir) == working_dir


def test_Instance_no_model_field(abc_instance_config):
  """Test that UserError is raised when no model field in config."""
  abc_instance_config.ClearField('model_specification')
  with pytest.raises(errors.UserError) as e_info:
    clgen.Instance(abc_instance_config)
  assert "Field not set: 'Instance.model_specification'" == str(e_info.value)


def test_Instance_no_sampler_field(abc_instance_config):
  """Test that UserError is raised when no model field in config."""
  abc_instance_config.ClearField('model_specification')
  with pytest.raises(errors.UserError) as e_info:
    clgen.Instance(abc_instance_config)
  assert "Field not set: 'Instance.model_specification'" == str(e_info.value)


def test_Instance_Session_clgen_dir(abc_instance_config):
  """Test that $CLEN_CACHE is set to working_dir inside a session."""
  instance = clgen.Instance(abc_instance_config)
  with instance.Session():
    assert os.environ['CLGEN_CACHE'] == abc_instance_config.working_dir


def test_Instance_Session_no_working_dir(abc_instance_config):
  """Test that $CLEN_CACHE is not set when there's no working_dir."""
  abc_instance_config.ClearField('working_dir')
  os.environ['CLGEN_CACHE'] = 'foo'
  instance = clgen.Instance(abc_instance_config)
  with instance.Session():
    assert os.environ['CLGEN_CACHE'] == 'foo'


def test_Instance_Session_yield_value(abc_instance_config):
  """Test that Session() yields the instance."""
  instance = clgen.Instance(abc_instance_config)
  with instance.Session() as s:
    assert instance == s


def test_Instance_ToProto_equality(abc_instance_config):
  """Test that ToProto() returns the same as the input config."""
  instance = clgen.Instance(abc_instance_config)
  assert abc_instance_config == instance.ToProto()


# RunWithErrorHandling() tests.

def test_RunWithErrorHandling_return_value(clgen_cache_dir):
  """Test that RunWithErrorHandling() returns correct value for function."""
  del clgen_cache_dir
  assert clgen.RunWithErrorHandling(lambda a, b: a // b, 4, 2) == 2


def test_RunWithErrorHandling_system_exit(clgen_cache_dir):
  """Test that SystemExit is raised on exception."""
  del clgen_cache_dir
  with pytest.raises(SystemExit):
    clgen.RunWithErrorHandling(lambda a, b: a // b, 1, 0)


def test_RunWithErrorHandling_exception_debug(clgen_cache_dir):
  """Test that FLAGS.debug disables exception catching."""
  del clgen_cache_dir
  flags.FLAGS(['argv[0]', '--clgen_debug'])
  with pytest.raises(ZeroDivisionError):
    clgen.RunWithErrorHandling(lambda a, b: a // b, 1, 0)


# main tests.

def test_main_unrecognized_arguments():
  """Test that UsageError is raised if arguments are not recognized."""
  with pytest.raises(app.UsageError) as e_info:
    clgen.main(['argv[0]', '--foo', '--bar'])
  assert "Unrecognized command line options: '--foo --bar'" == str(e_info.value)


def test_main_no_config_flag():
  """Test that UsageError is raised if --config flag not set."""
  with pytest.raises(app.UsageError) as e_info:
    clgen.main(['argv[0]'])
  assert "Missing required argument: '--config'" == str(e_info.value)


def test_main_config_file_not_found():
  """Test that UsageError is raised if --config flag not found."""
  with tempfile.TemporaryDirectory() as d:
    flags.FLAGS.unparse_flags()
    flags.FLAGS(['argv[0]', '--config', f'{d}/config.pbtxt'])
    with pytest.raises(app.UsageError) as e_info:
      clgen.main(['argv[0]'])
    assert f"File not found: '{d}/config.pbtxt'" == str(e_info.value)


def test_main_print_cache_path_corpus(abc_instance_file, capsys):
  """Test that --print_cache_path=corpus prints directory path."""
  flags.FLAGS.unparse_flags()
  flags.FLAGS(
      ['argv[0]', '--config', abc_instance_file, '--print_cache_path=corpus'])
  clgen.main([])
  out, err = capsys.readouterr()
  assert '/corpus/' in out
  assert pathlib.Path(out.strip()).is_dir()


def test_main_print_cache_path_model(abc_instance_file, capsys):
  """Test that --print_cache_path=model prints directory path."""
  flags.FLAGS.unparse_flags()
  flags.FLAGS(
      ['argv[0]', '--config', abc_instance_file, '--print_cache_path=model'])
  clgen.main([])
  out, err = capsys.readouterr()
  assert '/model/' in out
  assert pathlib.Path(out.strip()).is_dir()


def test_main_print_cache_path_sampler(abc_instance_file, capsys):
  """Test that --print_cache_path=sampler prints directory path."""
  flags.FLAGS.unparse_flags()
  flags.FLAGS(
      ['argv[0]', '--config', abc_instance_file, '--print_cache_path=sampler'])
  clgen.main([])
  out, err = capsys.readouterr()
  assert '/samples/' in out
  # A sampler's cache isn't created until Sample() is called.
  assert not pathlib.Path(out.strip()).is_dir()


def test_main_print_cache_invalid_argument(abc_instance_file):
  """Test that UsageError raised if --print_cache_path arg not valid."""
  flags.FLAGS.unparse_flags()
  flags.FLAGS(
      ['argv[0]', '--config', abc_instance_file, '--print_cache_path=foo'])
  with pytest.raises(app.UsageError) as e_info:
    clgen.main([])
  assert "Invalid --print_cache_path argument: 'foo'" == str(e_info.value)


def test_main_min_samples(abc_instance_file):
  """Test that min_samples samples are produced."""
  flags.FLAGS.unparse_flags()
  flags.FLAGS(['argv[0]', '--config', abc_instance_file, '--min_samples', '1'])
  clgen.main([])


def test_main_stop_after_corpus(abc_instance_file):
  """Test that --stop_after corpus prevents model training."""
  flags.FLAGS.unparse_flags()
  flags.FLAGS(
      ['argv[0]', '--config', abc_instance_file, '--stop_after', 'corpus'])
  clgen.main([])
  instance = clgen.Instance(
      pbutil.FromFile(pathlib.Path(abc_instance_file), clgen_pb2.Instance()))
  assert not instance.model.is_trained


def test_main_stop_after_train(abc_instance_file):
  """Test that --stop_after train trains the model."""
  flags.FLAGS.unparse_flags()
  flags.FLAGS(
      ['argv[0]', '--config', abc_instance_file, '--stop_after', 'train'])
  clgen.main([])
  instance = clgen.Instance(
      pbutil.FromFile(pathlib.Path(abc_instance_file), clgen_pb2.Instance()))
  assert instance.model.is_trained


def main(argv):
  """Main entry point."""
  if len(argv) > 1:
    raise app.UsageError('Unrecognized command line flags.')
  sys.exit(pytest.main([__file__, '-v']))


if __name__ == '__main__':
  app.run(main)
