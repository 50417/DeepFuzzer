"""Python type utilities.
"""
import inspect
import itertools
import sys
import typing
from collections import Mapping

from six import string_types


def is_str(s):
  """
  Return whether variable is string type.

  On python 3, unicode encoding is *not* string type. On python 2, it is.

  Arguments:
      s: Value.

  Returns:
      bool: True if is string, else false.
  """
  return isinstance(s, string_types)


def is_dict(obj):
  """
  Check if an object is a dict.
  """
  return isinstance(obj, dict)


def is_seq(obj):
  """
  Check if an object is a sequence.
  """
  return (not is_str(obj) and not is_dict(obj) and
          (hasattr(obj, "__getitem__") or hasattr(obj, "__iter__")))


def flatten(lists):
  """
  Flatten a list of lists.
  """
  return [item for sublist in lists for item in sublist]


def update(dst, src):
  """
  Recursively update values in dst from src.

  Unlike the builtin dict.update() function, this method will decend into
  nested dicts, updating all nested values.

  Arguments:
      dst (dict): Destination dict.
      src (dict): Source dict.

  Returns:
      dict: dst updated with entries from src.
  """
  for k, v in src.items():
    if isinstance(v, Mapping):
      r = update(dst.get(k, {}), v)
      dst[k] = r
    else:
      dst[k] = src[k]
  return dst


def dict_values(src):
  """
  Recursively get values in dict.

  Unlike the builtin dict.values() function, this method will descend into
  nested dicts, returning all nested values.

  Arguments:
      src (dict): Source dict.

  Returns:
      list: List of values.
  """
  for v in src.values():
    if isinstance(v, dict):
      for v in dict_values(v):
        yield v
    else:
      yield v


def get_class_that_defined_method(meth):
  """
  Return the class that defines a method.

  Arguments:
      meth (str): Class method.

  Returns:
      class: Class object, or None if not a class method.
  """
  if sys.version_info >= (3, 0):
    # Written by @Yoel http://stackoverflow.com/a/25959545
    if inspect.ismethod(meth):
      for cls in inspect.getmro(meth.__self__.__class__):
        if cls.__dict__.get(meth.__name__) is meth:
          return cls
      meth = meth.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
      cls = getattr(inspect.getmodule(meth),
                    meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[
                      0])
      if isinstance(cls, type):
        return cls
  else:
    try:
      # Writted by @Alex Martelli http://stackoverflow.com/a/961057
      for cls in inspect.getmro(meth.im_class):
        if meth.__name__ in cls.__dict__:
          return cls
    except AttributeError:
      return None
  return None


class ReprComparable(object):
  """
  An abstract class which may be inherited from in order to enable __repr__.
  """

  def __lt__(self, other):
    return str(self) < str(other)

  def __le__(self, other):
    return str(self) <= str(other)

  def __eq__(self, other):
    return str(self) == str(other)

  def __ne__(self, other):
    return str(self) != str(other)

  def __gt__(self, other):
    return str(self) > str(other)

  def __ge__(self, other):
    return str(self) >= str(other)


def PairwiseIterator(iterable: typing.Iterator[typing.Any]
                     ) -> typing.Iterator[typing.Tuple[typing.Any, typing.Any]]:
  """Construct a pairwise iterator for a input generator.

  Given an iterator, produces an iterator of overlapping pairs from the input:
  s -> (s0,s1), (s1,s2), (s2, s3), ...

  Args:
    iterable: The input iterable. Once called, this iterable should not be
      used any more.

  Returns:
    An iterator of pairs.
  """
  # Split the iterable into two.
  a, b = itertools.tee(iterable)
  # Advance the second iterable by one.
  next(b, None)
  # Return the pairs.
  return zip(a, b)


def SetDiff(a: typing.Iterator[typing.Any],
            b: typing.Iterator[typing.Any]) -> typing.List[typing.Any]:
  """Return the set difference between two sequences.

  Args:
    a: An iterable.
    b: An iterable.

  Returns:
    The difference between the elements in the two iterables as a set.
  """
  set_a = set(a)
  set_b = set(b)
  return (set_a - set_b).union(set_b - set_a)
