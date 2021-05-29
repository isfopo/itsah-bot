import os
import discord
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

client = discord.Client()

LIMIT = 100

def is_command (msg): # Checks if the message is a command call
  if len(msg.content) == 0:
      return False
  elif msg.content.split()[0].startswith('--'):
      return True
  else:
      return False

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  elif message.content.startswith("--"):
    cmd = message.content.split()[0].replace("--", "")
    if len(message.content.split()) > 1:
      params = message.content.split()[1:]

  if cmd == "hello":
    await message.channel.send("hello")

  if cmd == 'scan':
    data = pd.DataFrame(columns=['content', 'time', 'author'])


    async for msg in message.channel.history(limit=LIMIT): # As an example, I've set the limit to 10000
      if msg.author != client.user:                        # meaning it'll read 10000 messages instead of           
          if not is_command(msg):                          # the default amount of 100        
              data = data.append({'content': msg.content,
                                  'time': msg.created_at,
                                  'author': msg.author.name}, ignore_index=True)
          if len(data) == LIMIT:
              break
      
    file_location = "data.csv"
    data.to_csv(file_location)

client.run(os.getenv("DISCORD_TOKEN"))