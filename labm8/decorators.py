"""Useful function decorators."""
import functools
import typing

from absl import flags


FLAGS = flags.FLAGS

# A type hint that specifies a callable function with any number of arguments
# and any return type.
AnyFunction = typing.Callable[..., typing.Any]


def memoized_property(func: AnyFunction) -> AnyFunction:
  """A property decorator that memoizes the result.

  This is used to memoize the results of class properties, to be used when
  computing the property value is expensive.

  Args:
    func: The function which should be made to a property.

  Returns:
    The decorated property function.
  """
  # Based on Danijar Hafner's implementation of a lazy property, available at:
  # https://danijar.com/structuring-your-tensorflow-models/
  attribute_name = '_memoized_property_' + func.__name__

  @property
  @functools.wraps(func)
  def decorator(self):
    if not hasattr(self, attribute_name):
      setattr(self, attribute_name, func(self))
    return getattr(self, attribute_name)

  return decorator
