"""Unit tests for //labm8:decorators.py."""
import sys
import typing

import pytest
from absl import app
from absl import flags

from labm8 import decorators


FLAGS = flags.FLAGS


class DummyClass(object):

  def __init__(self):
    self.memoized_property_run_count = 0

  @decorators.memoized_property
  def memoized_property(self):
    self.memoized_property_run_count += 1
    # In "real world" usage, this would be an expensive computation who's result
    # we would like to memoize.
    return 5


def test_memoized_property_value():
  """Test that memoized property returns expected value."""
  c = DummyClass()
  assert c.memoized_property == 5


def test_memoized_property_run_count():
  """Test that repeated access to property returns memoized value."""
  c = DummyClass()
  _ = c.memoized_property
  _ = c.memoized_property
  _ = c.memoized_property
  assert c.memoized_property_run_count == 1


def main(argv: typing.List[str]):
  """Main entry point."""
  if len(argv) > 1:
    raise app.UsageError("Unknown arguments: '{}'.".format(' '.join(argv[1:])))
  sys.exit(pytest.main([__file__, '-vv']))


if __name__ == '__main__':
  flags.FLAGS(['argv[0]', '-v=1'])
  app.run(main)
