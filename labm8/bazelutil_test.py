"""Unit tests for //labm8/bazelutil.py."""
import sys
import tempfile

import pytest
from absl import app

from labm8 import bazelutil
from labm8 import fs


# IsBazelSandbox() tests.

def test_IsBazelSandbox_different_working_directories():
  """Test IsBazelSandboxed() returns the same result from different dirs."""
  sandbox = bazelutil.IsBazelSandbox()
  # We can't test the expected value of this since we don't know it.
  assert sandbox or True
  with tempfile.TemporaryDirectory() as d:
    with fs.chdir(d):
      assert bazelutil.IsBazelSandbox() == sandbox
  with fs.chdir('/tmp'):
    assert bazelutil.IsBazelSandbox() == sandbox


# DataPath() tests.

def test_DataPath_path_not_found():
  """Test that FileNotFoundError is raised if the file is not found."""
  with pytest.raises(FileNotFoundError) as e_info:
    bazelutil.DataPath('')
  assert f"No such file or directory: ''" in str(e_info)

  with pytest.raises(FileNotFoundError) as e_info:
    bazelutil.DataPath('/not/a/real/path')
  assert f"No such file or directory: '/not/a/real/path'" in str(e_info)


def test_DataPath_missing_data_dep():
  """FileNotFoundError is raised if the file exists is not in target data."""
  # The file //labm8/data/test/diabetes.csv exists, but is not a data
  # dependency of this test target, so is not found.
  with pytest.raises(FileNotFoundError) as e_info:
    bazelutil.DataPath('phd/labm8/data/test/diabetes.csv')
  assert ("No such file or directory: "
          "'phd/labm8/data/test/diabetes.csv'") in str(e_info)


def test_DataPath_missing_data_dep_not_must_exist():
  """Path is returned if the file doesn't exist."""
  # The file //labm8/data/test/diabetes.csv exists, but is not a data
  # dependency of this test target, so is not found.
  assert bazelutil.DataPath(
      'phd/labm8/data/test/diabetes.csv', must_exist=False)


def test_DataPath_read_file():
  """Test that DataPath is correct for a known data file."""
  with open(bazelutil.DataPath('phd/labm8/data/test/hello_world')) as f:
    assert f.read() == 'Hello, world!\n'


def test_DataPath_directory():
  """Test that DataPath returns the path to a directory."""
  assert str(bazelutil.DataPath('phd/labm8/data/test')).endswith(
      'phd/labm8/data/test')


def test_DataPath_different_working_dir():
  """Test that DataPath is not affected by current working dir."""
  p = bazelutil.DataPath('phd/labm8/data/test/hello_world')
  with fs.chdir('/tmp'):
    assert bazelutil.DataPath('phd/labm8/data/test/hello_world') == p
  with tempfile.TemporaryDirectory() as d:
    with fs.chdir(d):
      assert bazelutil.DataPath('phd/labm8/data/test/hello_world') == p


def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Unrecognized command line flags.')
  sys.exit(pytest.main([__file__, '-vv']))


if __name__ == '__main__':
  app.run(main)
