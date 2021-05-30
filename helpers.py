def is_command (msg): # Checks if the message is a command call
  if len(msg.content) == 0: return False
  elif msg.content.split()[0].startswith('--'): return True
  else: return False