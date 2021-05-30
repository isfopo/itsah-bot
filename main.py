import os
import discord
import pandas as pd
from dotenv import load_dotenv
from sentiment_analysis import get_sentiment
import helpers

load_dotenv()

client = discord.Client()

LIMIT = 100

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
  else: return

  if cmd == "hello":
    await message.channel.send("hello")

  elif cmd == 'scan':
    data = pd.DataFrame(columns=['content', 'time', 'author'])

    async for msg in message.channel.history(limit=LIMIT):
      if not msg.author.bot and not helpers.is_command(msg):                             
          data = data.append({'content': msg.content,
                              'time': msg.created_at,
                              'author': msg.author.name}, ignore_index=True)
          if len(data) == LIMIT:
            break
      
    file_location = "data.csv"
    data.to_csv(file_location)

(score, prediction) = get_sentiment("Transcendently beautiful in moments outside the office, it seems almost sitcom-like in those scenes. When Toni Colette walks out and ponders life silently, it's gorgeous.", "model_artifacts")

print(
  f"Predicted sentiment: {prediction}"
  f"\tScore: {score}"
)

  
client.run(os.getenv("DISCORD_TOKEN"))