"""Utility code for converting between absl logging output and log protos."""
import contextlib
import datetime
import pathlib
import re
import sys
import typing

from absl import flags
from absl import logging

from labm8 import labdate
from labm8.proto import logging_pb2


FLAGS = flags.FLAGS

# A regular expression to match the components of an absl logging prefix. See:
# https://github.com/abseil/abseil-py/blob/e69e200f680a20c50e0e2cd9e74e9850ff69b856/absl/logging/__init__.py#L554-L583
ABSL_LOGGING_LINE_RE = re.compile(
    r'(?P<lvl>[IWEF])(?P<timestamp>\d\d\d\d \d\d:\d\d:\d\d.\d\d\d\d\d\d) '
    r'(?P<thread_id>\d+) (?P<filename>[^:]+):(?P<lineno>\d+)] '
    r'(?P<contents>.*)')

# Convert a single letter absl logging prefix to a LogRecord.LogLevel. Since
# absl logging uses the same prefix for logging.DEBUG and logging.INFO, this
# conversion is lossy, as LogRecord.DEBUG is never returned.
ABSL_LEVEL_TO_LOG_RECORD_LEVEL = {
  'I': logging_pb2.LogRecord.INFO,
  'W': logging_pb2.LogRecord.WARNING,
  'E': logging_pb2.LogRecord.ERROR,
  'F': logging_pb2.LogRecord.FATAL,
}


def DatetimeFromAbslTimestamp(timestamp: str) -> datetime.datetime:
  dt = datetime.datetime.strptime(
      str(datetime.datetime.utcnow().year) + timestamp, '%Y%m%d %H:%M:%S.%f')
  return dt


def ConertAbslLogToProtos(logs: str) -> typing.List[logging_pb2.LogRecord]:
  """Convert the output of logging with absl logging to LogRecord protos.

  Args:
    logs: The output from logging with absl.

  Returns:
    A list of LogRecord messages.
  """
  records = []
  starting_match = None
  lines_buffer = []

  def ConvertOne() -> logging_pb2.LogRecord:
    """Convert the current starting_match and lines_buffer into a LogRecord."""
    if starting_match:
      records.append(logging_pb2.LogRecord(
          level=ABSL_LEVEL_TO_LOG_RECORD_LEVEL[starting_match.group('lvl')],
          date_utc_epoch_ms=labdate.MillisecondsTimestamp(
              DatetimeFromAbslTimestamp(starting_match.group('timestamp'))),
          thread_id=int(starting_match.group('thread_id')),
          file_name=starting_match.group('filename'),
          line_number=int(starting_match.group('lineno')),
          message='\n'.join(
              [starting_match.group('contents')] + lines_buffer).rstrip()))

  for line in logs.split('\n'):
    m = ABSL_LOGGING_LINE_RE.match(line)
    if m:
      ConvertOne()
      starting_match = None
      lines_buffer = []
      starting_match = m
    elif line and not starting_match:
      raise ValueError(f"Failed to parse logging output at line: '{line}'")
    else:
      lines_buffer.append(line)
  ConvertOne()
  return records


def StartTeeLogsToFile(program_name: str = None, log_dir: str = None,
                       file_log_level: int = logging.DEBUG) -> None:
  """Log messages to file as well as stderr.

  Args:
    program_name: The name of the program.
    log_dir: The directory to log to.
    file_log_level: The minimum verbosity level to log to file to.

  Raises:
    FileNotFoundError: If the requested log_dir does not exist.
  """
  if not pathlib.Path(log_dir).is_dir():
    raise FileNotFoundError(f"Log directory not found: '{log_dir}'")
  old_verbosity = logging.get_verbosity()
  logging.set_verbosity(file_log_level)
  logging.set_stderrthreshold(old_verbosity)
  logging.get_absl_handler().start_logging_to_file(program_name, log_dir)
  # The Absl logging handler function start_logging_to_file() sets logtostderr
  # to False. Re-enable whatever value it was before the call.
  FLAGS.logtostderr = False


def StopTeeLogsToFile():
  """Stop logging messages to file as well as stderr."""
  logging.get_absl_handler().flush()
  logging.get_absl_handler().stream = sys.stderr
  FLAGS.logtostderr = True


@contextlib.contextmanager
def TeeLogsToFile(program_name: str = None, log_dir: str = None,
                  file_log_level: int = logging.DEBUG):
  """Temporarily enable logging to file.

  Args:
    program_name: The name of the program.
    log_dir: The directory to log to.
    file_log_level: The minimum verbosity level to log to file to.
  """
  try:
    StartTeeLogsToFile(program_name, log_dir, file_log_level)
    yield
  finally:
    StopTeeLogsToFile()
