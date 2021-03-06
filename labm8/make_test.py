"""Unit tests for //labm8:make."""
import sys

import pytest
from absl import app

from labm8 import fs
from labm8 import make


# make()
def test_make():
  ret, out, err = make.make(dir="labm8/data/test/makeproj")
  assert not ret
  assert out
  assert fs.isfile("labm8/data/test/makeproj/foo")
  assert fs.isfile("labm8/data/test/makeproj/foo.o")


def test_make_bad_target():
  with pytest.raises(make.NoTargetError):
    make.make(target="bad-target", dir="labm8/data/test/makeproj")


def test_make_bad_target():
  with pytest.raises(make.NoMakefileError):
    make.make(dir="/bad/path")
  with pytest.raises(make.NoMakefileError):
    make.make(target="foo", dir="labm8/data/test")


def test_make_fail():
  with pytest.raises(make.MakeError):
    make.make(target="fail", dir="labm8/data/test/makeproj")


# clean()
def test_make_clean():
  fs.cd("labm8/data/test/makeproj")
  make.make()
  assert fs.isfile("foo")
  assert fs.isfile("foo.o")
  make.clean()
  assert not fs.isfile("foo")
  assert not fs.isfile("foo.o")
  fs.cdpop()


def main(argv):  # pylint: disable=missing-docstring
  del argv
  sys.exit(pytest.main([__file__, '-v']))


if __name__ == '__main__':
  app.run(main)
