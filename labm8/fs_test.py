"""Unit tests for //labm8:fs."""
import os
import pathlib
import sys
import tempfile

import pytest
from absl import app

from labm8 import fs
from labm8 import system


# path()
def test_path():
  assert "foo/bar" == fs.path("foo", "bar")
  assert "foo/bar/car" == fs.path("foo/bar", "car")


def test_path_homedir():
  assert os.path.expanduser("~") == fs.path("~")
  assert (os.path.join(os.path.expanduser("~"), "foo") == fs.path("~", "foo"))


def test_must_exist():
  with tempfile.NamedTemporaryFile(prefix='labm8_') as f:
    assert fs.must_exist(f.name) == f.name
    assert fs.must_exist(fs.dirname(f.name), fs.basename(f.name)) == f.name
  with pytest.raises(fs.File404):
    fs.must_exist("/not/a/real/path")


# abspath()
def test_abspath():
  assert (os.path.abspath(".") + "/foo/bar" == fs.abspath("foo", "bar"))
  assert (os.path.abspath(".") + "/foo/bar/car" == fs.abspath("foo/bar", "car"))


def test_abspath_homedir():
  assert os.path.expanduser("~") == fs.abspath("~")
  assert (
      os.path.join(os.path.expanduser("~"), "foo") == fs.abspath("~", "foo"))


# is_subdir()
def test_is_subdir():
  assert fs.is_subdir("/home", "/")
  assert fs.is_subdir("/proc/1", "/proc")
  assert fs.is_subdir("/proc/1", "/proc/1/")
  assert not fs.is_subdir("/proc/3", "/proc/1/")
  assert not fs.is_subdir("/", "/home")


def test_is_subdir_not_subdir():
  assert not fs.is_subdir("/", "/home")


# basename()
def test_basename():
  assert "foo" == fs.basename("foo")
  assert "foo" == fs.basename(fs.abspath("foo"))


def test_dirname():
  assert "" == fs.dirname("foo")
  assert "/tmp" == fs.dirname("/tmp/labm8.tmp")


# cd(), cdpop()
def test_cd():
  cwd = os.getcwd()
  new = fs.abspath("..")

  assert new == fs.cd("..")
  assert new == os.getcwd()

  assert cwd == fs.cdpop()
  assert cwd == os.getcwd()

  assert cwd == fs.cdpop()
  assert cwd == os.getcwd()

  assert cwd == fs.cdpop()
  assert cwd == os.getcwd()


# pwd()
def test_pwd():
  assert os.getcwd() == fs.pwd()


# exists()
def test_exists():
  assert fs.exists(__file__)
  assert fs.exists("/")
  assert not fs.exists("/not/a/real/path (I hope!)")


# isfile()
def test_isfile():
  assert fs.isfile(__file__)
  assert not fs.isfile("/")
  assert not fs.isfile("/not/a/real/path (I hope!)")


# isexe()
def test_isexe():
  assert fs.isexe("/bin/ls")
  assert not fs.isexe("/home")
  assert not fs.isexe("/not/a/real/path (I hope!)")


# isdir()
def test_isdir():
  assert not fs.isdir(__file__)
  assert fs.isdir("/")
  assert not fs.isdir("/not/a/real/path (I hope!)")


# read()
def test_read():
  assert ['Hello, world!'] == fs.read("labm8/data/test/hello_world")
  assert (['# data1 - test file', 'This', 'is a test file', 'With',
           'trailing  # comment', '', '', '', 'whitespace', '0.344'] == fs.read(
      "labm8/data/test/data1"))


def test_read_no_rstrip():
  assert (['# data1 - test file\n', 'This\n', 'is a test file\n', 'With\n',
           'trailing  # comment  \n', '\n', '\n', '\n', 'whitespace\n',
           '0.344\n'] == fs.read("labm8/data/test/data1", rstrip=False))


def test_read_ignore_comments():
  assert (
      ['This', 'is a test file', 'With', 'trailing', '', '', '', 'whitespace',
       '0.344'] == fs.read("labm8/data/test/data1", comment_char="#"))


def test_read_ignore_comments_no_rstrip():
  assert (
      ['This\n', 'is a test file\n', 'With\n', 'trailing  ', '\n', '\n', '\n',
       'whitespace\n', '0.344\n'] == fs.read("labm8/data/test/data1",
                                             rstrip=False, comment_char="#"))


def test_read_empty_file():
  assert fs.read("labm8/data/test/empty_file") == []


# mkdir()
def test_mkdir():
  fs.rm("/tmp/labm8.dir")
  assert not fs.isdir("/tmp/labm8.dir")
  fs.mkdir("/tmp/labm8.dir")
  assert fs.isdir("/tmp/labm8.dir")


def test_mkdir_parents():
  assert not fs.isdir("/tmp/labm8.dir/foo/bar")
  fs.mkdir("/tmp/labm8.dir/foo/bar")
  assert fs.isdir("/tmp/labm8.dir/foo/bar")


def test_mkdir_exists():
  fs.mkdir("/tmp/labm8.dir/")
  assert fs.isdir("/tmp/labm8.dir/")
  fs.mkdir("/tmp/labm8.dir/")
  fs.mkdir("/tmp/labm8.dir/")
  assert fs.isdir("/tmp/labm8.dir/")


# mkopen()
def test_mkopen():
  fs.rm("/tmp/labm8.dir")
  assert not fs.isdir("/tmp/labm8.dir/")
  f = fs.mkopen("/tmp/labm8.dir/foo", "w")
  assert fs.isdir("/tmp/labm8.dir/")
  f.close()


# rm()
def test_rm():
  system.echo("Hello, world!", "/tmp/labm8.tmp")
  assert fs.isfile("/tmp/labm8.tmp")
  fs.rm("/tmp/labm8.tmp")
  assert not fs.isfile("/tmp/labm8.tmp")
  fs.rm("/tmp/labm8.tmp")
  fs.rm("/tmp/labm8.tmp")
  fs.rm("/tmp/labm8.dir")
  fs.mkdir("/tmp/labm8.dir/foo/bar")
  system.echo("Hello, world!", "/tmp/labm8.dir/foo/bar/baz")
  assert fs.isfile("/tmp/labm8.dir/foo/bar/baz")
  fs.rm("/tmp/labm8.dir")
  assert not fs.isfile("/tmp/labm8.dir/foo/bar/baz")
  assert not fs.isfile("/tmp/labm8.dir/")


def test_rm_glob():
  fs.mkdir("/tmp/labm8.glob")
  system.echo("Hello, world!", "/tmp/labm8.glob/1")
  system.echo("Hello, world!", "/tmp/labm8.glob/2")
  system.echo("Hello, world!", "/tmp/labm8.glob/abc")

  fs.rm("/tmp/labm8.glob/a*", glob=False)
  assert fs.isfile("/tmp/labm8.glob/1")
  assert fs.isfile("/tmp/labm8.glob/2")
  assert fs.isfile("/tmp/labm8.glob/abc")

  fs.rm("/tmp/labm8.glob/a*")
  assert fs.isfile("/tmp/labm8.glob/1")
  assert fs.isfile("/tmp/labm8.glob/2")
  assert not fs.isfile("/tmp/labm8.glob/abc")

  fs.rm("/tmp/labm8.glob/*")
  assert not fs.isfile("/tmp/labm8.glob/1")
  assert not fs.isfile("/tmp/labm8.glob/2")
  assert not fs.isfile("/tmp/labm8.glob/abc")


# rmtrash()
@pytest.mark.skip(
    reason='Insufficient access privileges for operation on macOS')
def test_rmtrash():
  with tempfile.NamedTemporaryFile(prefix='labm8_') as f:
    assert fs.isfile(f.name)
    fs.rmtrash(f.name)
    assert not fs.isfile(f.name)
    fs.rmtrash(f.name)
    fs.rm(f.name)
  with tempfile.TemporaryDirectory() as d:
    fs.rm(d)
    fs.mkdir(d, "foo/bar")
    system.echo("Hello, world!", fs.path(d, "foo/bar/baz"))
    assert fs.isfile(f, "foo/bar/baz")
    fs.rmtrash(d)
    assert not fs.isfile(d, "foo/bar/baz")
    assert not fs.isdir(d)


def test_rmtrash_bad_path():
  fs.rmtrash("/not/a/real/path")


# cp()
def test_cp():
  system.echo("Hello, world!", "/tmp/labm8.tmp")
  assert ["Hello, world!"] == fs.read("/tmp/labm8.tmp")
  # Cleanup any existing file.
  fs.rm("/tmp/labm8.tmp.copy")
  assert not fs.exists("/tmp/labm8.tmp.copy")
  fs.cp("/tmp/labm8.tmp", "/tmp/labm8.tmp.copy")
  assert fs.read("/tmp/labm8.tmp") == fs.read("/tmp/labm8.tmp.copy")


def test_cp_no_file():
  pytest.raises(IOError, fs.cp, "/not a real src", "/not/a/real dest")


def test_cp_dir():
  fs.rm("/tmp/labm8")
  fs.rm("/tmp/labm8.copy")
  fs.mkdir("/tmp/labm8/foo/bar")
  assert not fs.exists("/tmp/labm8.copy")
  fs.cp("/tmp/labm8/", "/tmp/labm8.copy")
  assert fs.isdir("/tmp/labm8.copy")
  assert fs.isdir("/tmp/labm8.copy/foo")
  assert fs.isdir("/tmp/labm8.copy/foo/bar")


def test_cp_overwrite():
  system.echo("Hello, world!", "/tmp/labm8.tmp")
  assert ["Hello, world!"] == fs.read("/tmp/labm8.tmp")
  # Cleanup any existing file.
  fs.rm("/tmp/labm8.tmp.copy")
  assert not fs.exists("/tmp/labm8.tmp.copy")
  fs.cp("/tmp/labm8.tmp", "/tmp/labm8.tmp.copy")
  system.echo("Goodbye, world!", "/tmp/labm8.tmp")
  fs.cp("/tmp/labm8.tmp", "/tmp/labm8.tmp.copy")
  assert fs.read("/tmp/labm8.tmp") == fs.read("/tmp/labm8.tmp.copy")


def test_cp_over_dir():
  fs.mkdir("/tmp/labm8.tmp.src")
  system.echo("Hello, world!", "/tmp/labm8.tmp.src/foo")
  fs.rm("/tmp/labm8.tmp.copy")
  fs.mkdir("/tmp/labm8.tmp.copy")
  assert fs.isdir("/tmp/labm8.tmp.src")
  assert fs.isfile("/tmp/labm8.tmp.src/foo")
  assert fs.isdir("/tmp/labm8.tmp.copy")
  assert not fs.isfile("/tmp/labm8.tmp.copy/foo")
  fs.cp("/tmp/labm8.tmp.src", "/tmp/labm8.tmp.copy/")
  assert fs.isdir("/tmp/labm8.tmp.src")
  assert fs.isfile("/tmp/labm8.tmp.src/foo")
  assert fs.isdir("/tmp/labm8.tmp.copy")
  assert fs.isfile("/tmp/labm8.tmp.copy/foo")
  assert (
      fs.read("/tmp/labm8.tmp.src/foo") == fs.read("/tmp/labm8.tmp.copy/foo"))


# mv()
def test_mv():
  system.echo("Hello, world!", "/tmp/labm8.tmp")
  assert ["Hello, world!"] == fs.read("/tmp/labm8.tmp")
  # Cleanup any existing file.
  fs.rm("/tmp/labm8.tmp.copy")
  assert not fs.exists("/tmp/labm8.tmp.copy")
  fs.mv("/tmp/labm8.tmp", "/tmp/labm8.tmp.copy")
  assert ["Hello, world!"] == fs.read("/tmp/labm8.tmp.copy")
  assert not fs.exists("/tmp/labm8.tmp")


def test_mv_no_src():
  with pytest.raises(fs.File404):
    fs.mv("/bad/path", "foo")


def test_mv_no_dst():
  system.echo("Hello, world!", "/tmp/labm8.tmp")
  with pytest.raises(IOError):
    fs.mv("/tmp/labm8.tmp", "/not/a/real/path")
  fs.rm("/tmp/labm8.tmp")


# ls()
def test_ls():
  assert ["a", "b", "c", "d"] == fs.ls("labm8/data/test/testdir")


def test_ls_recursive():
  assert fs.ls("labm8/data/test/testdir", recursive=True) == ["a", "b", "c",
                                                              "c/e", "c/f",
                                                              "c/f/f",
                                                              "c/f/f/i",
                                                              "c/f/h",
                                                              "c/g", "d", ]


def test_ls_abspaths():
  fs.cp("labm8/data/test/testdir", "/tmp/testdir")
  assert fs.ls("/tmp/testdir", abspaths=True) == ["/tmp/testdir/a",
                                                  "/tmp/testdir/b",
                                                  "/tmp/testdir/c",
                                                  "/tmp/testdir/d", ]
  assert fs.ls("/tmp/testdir", recursive=True, abspaths=True) == [
    "/tmp/testdir/a", "/tmp/testdir/b", "/tmp/testdir/c", "/tmp/testdir/c/e",
    "/tmp/testdir/c/f", "/tmp/testdir/c/f/f", "/tmp/testdir/c/f/f/i",
    "/tmp/testdir/c/f/h", "/tmp/testdir/c/g", "/tmp/testdir/d", ]
  fs.rm("/tmp/testdir")


def test_ls_empty_dir():
  fs.mkdir("/tmp/labm8.empty")
  assert not fs.ls("/tmp/labm8.empty")
  fs.rm("/tmp/labm8.empty")


def test_ls_bad_path():
  with pytest.raises(OSError):
    fs.ls("/not/a/real/path/bro")


def test_ls_single_file():
  assert ["a"] == fs.ls("labm8/data/test/testdir/a")


# lsdirs()
def test_lsdirs():
  assert ["c"] == fs.lsdirs("labm8/data/test/testdir")


def test_lsdirs_recursive():
  assert fs.lsdirs("labm8/data/test/testdir", recursive=True) == ["c",
                                                                  "c/f",
                                                                  "c/f/f", ]


def test_lsdirs_bad_path():
  with pytest.raises(OSError):
    fs.lsdirs("/not/a/real/path/bro")


def test_lsdirs_single_file():
  assert not fs.lsdirs("labm8/data/test/testdir/a")


# lsdirs()
def test_lsfiles():
  assert fs.lsfiles("labm8/data/test/testdir") == ["a", "b", "d"]


def test_lsfiles_recursive():
  assert fs.lsfiles("labm8/data/test/testdir", recursive=True) == ["a", "b",
                                                                   "c/e",
                                                                   "c/f/f/i",
                                                                   "c/f/h",
                                                                   "c/g",
                                                                   "d", ]


def test_lsfiles_bad_path():
  with pytest.raises(OSError):
    fs.lsfiles("/not/a/real/path/bro")


def test_lsfiles_single_file():
  assert fs.lsfiles("labm8/data/test/testdir/a") == ["a"]


def test_directory_is_empty_empty_dir():
  """Test that en empty directory returns True."""
  with tempfile.TemporaryDirectory() as d:
    assert fs.directory_is_empty(d)


def test_directory_is_empty_only_subdirs():
  """Test that a subdirectory means the directory is not empty."""
  with tempfile.TemporaryDirectory() as d:
    (pathlib.Path(d) / 'a').mkdir()
    assert not fs.directory_is_empty(d)


def test_directory_is_empty_file():
  """Test that a file means the directory is not empty."""
  with tempfile.TemporaryDirectory() as d:
    (pathlib.Path(d) / 'a').touch()
    assert not fs.directory_is_empty(d)


def test_directory_is_empty_non_existent():
  """Test that a non-existent path is an empty directory."""
  with tempfile.TemporaryDirectory() as d:
    assert fs.directory_is_empty(pathlib.Path(d) / 'a')


def test_directory_is_empty_file_argument():
  """Test that path to a file is an empty directory."""
  with tempfile.TemporaryDirectory() as d:
    (pathlib.Path(d) / 'a').touch()
    assert fs.directory_is_empty(pathlib.Path(d) / 'a')


# chdir()

def test_chdir_yield_value():
  """Test that chdir() yields the requested directory as a pathlib.Path."""
  with tempfile.TemporaryDirectory() as d:
    with fs.chdir(d) as d2:
      assert pathlib.Path(d) == d2


def test_chdir_cwd():
  """Test that chdir() correctly changes the working directory."""
  with tempfile.TemporaryDirectory() as d:
    with fs.chdir(d):
      # Bazel sandboxing only changes to directories within the sandbox, so
      # there may be an unwanted prefix like /private that we can ignore.
      assert os.getcwd().endswith(d)


def test_chdir_not_a_directory():
  """Test that FileNotFoundError is raised if requested path does not exist."""
  with pytest.raises(FileNotFoundError) as e_info:
    with fs.chdir('/not/a/real/path'):
      pass
  assert "No such file or directory: '/not/a/real/path'" in str(e_info)


def test_chdir_file_argument():
  """Test that NotADirectoryError is raised if requested path is a file."""
  with tempfile.NamedTemporaryFile(prefix='labm8_') as f:
    with pytest.raises(NotADirectoryError) as e_info:
      with fs.chdir(f.name):
        pass
    # Bazel sandboxing only changes to directories within the sandbox, so there
    # may be an unwanted prefix like /private that we can ignore.
    assert f"Not a directory: '" in str(e_info)
    assert f.name in str(e_info)


def main(argv):  # pylint: disable=missing-docstring
  del argv
  sys.exit(pytest.main([__file__, '-v']))


if __name__ == '__main__':
  app.run(main)
