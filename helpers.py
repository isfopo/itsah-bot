from re import match


def is_command (msg: str) -> bool:
  '''
  Takes a message and determines if it is a command
  '''
  if len(msg.content) == 0: return False
  elif msg.content.split()[0].startswith('--'): return True
  else: return False


def filter_by_regex(values: list = [], regex: str = "*") -> list:
  '''
  Filters a list of strings and returns a list only containing strings that match the given regex
  '''
  return list(filter(lambda v: match(regex, v), values))


def first_or_none(values: list = []) -> list:
  '''
  Returns the first value of a list, but there is none, returns None
  '''
  return values[0] if len(values) > 0 else None


def last_or_none(values: list = []) -> list:
  '''
  Returns the last value of a list, but there is none, returns None
  '''
  return values[-1] if len(values) > 0 else None


def extract_param(params: list, keyword: str):
  '''
  Gets the parameter for a given keyword
  '''
  param = first_or_none(filter_by_regex(params, f"^{keyword}.*$"))
  if param:
    return last_or_none(param.split("="))
  else: return None


def to_percent(decimal: int):
  '''
  Converts a decimal to a percentage
  '''
  return int(decimal * 100)
