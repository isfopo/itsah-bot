from re import match

def is_command (msg) -> bool: # Checks if the message is a command call
  if len(msg.content) == 0: return False
  elif msg.content.split()[0].startswith('--'): return True
  else: return False

def filter_by_regex(values: list = [], regex: str = "*") -> list:
  return list(filter(lambda v: match(regex, v), values))

def first_or_none(values: list = []) -> list:
  return values[0] if len(values) > 0 else []