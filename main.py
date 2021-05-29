import os
import csv
import random
import discord
import spacy
import pandas as pd
from dotenv import load_dotenv

nlp = spacy.load("en_core_web_sm")

load_dotenv()

client = discord.Client()

LIMIT = 100

def load_training_data(
    data_directory: str = "dataset/train.csv",
    split: float = 0.8,
    limit: int = 0
) -> tuple:
  messages = []
  with open(data_directory) as f:
    csv_data = csv.reader(f, delimiter = ",")
    line_count = 0
    for row in csv_data:
      if line_count == 0:
        pass
      else: 
        spacy_label = {
          "cats": {
            "pos": row[1] == 1,
            "neg": row[1] == 0
          }
        }
        messages.append((row[2], spacy_label))
  random.shuffle(messages)
  if limit:
    messages = messages[:limit]
  split = int(len(messages) * split)
  return messages[:split], messages[split:]

def is_command (msg): # Checks if the message is a command call
  if len(msg.content) == 0: return False
  elif msg.content.split()[0].startswith('--'): return True
  else: return False

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user or message.author.bot:
    return
  elif message.content.startswith("--"):
    cmd = message.content.split()[0].replace("--", "")
    params = message.content.split()[1:] if len(message.content.split()) > 1 else None #IDEA: use params to get the sentiment from a particular user like "user=isfopo"
  else:
    return

  if cmd == "hello":
    await message.channel.send("hello")

  elif cmd == 'scan':
    data = pd.DataFrame(columns=['content', 'time', 'author'])

    async for msg in message.channel.history(limit=LIMIT):
      if not msg.author.bot and not is_command(msg):                             
          data = data.append({'content': msg.content,
                              'time': msg.created_at,
                              'author': msg.author.name}, ignore_index=True)
          if len(data) == LIMIT:
            break
      
    file_location = "data.csv"
    data.to_csv(file_location)

client.run(os.getenv("DISCORD_TOKEN"))