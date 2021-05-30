import os
import discord
from dotenv import load_dotenv
from sentiment_analysis import get_sentiment
import helpers

load_dotenv()

client = discord.Client()

LIMIT = 100

@client.event
async def on_ready():
    print(f'logged in as {client.user}')

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

    async for msg in message.channel.history(limit=LIMIT):                 
      if msg.content and not msg.author.bot and not helpers.is_command(msg):
        (score, prediction) = get_sentiment(msg.content, "model_artifacts") # prediction is positive or negative, score is how positive or negative it is
        
        print(
          f"Message: {msg.content}"
          f"\tPredicted sentiment: {prediction}"
          f"\tScore: {score}"
        )

  
client.run(os.getenv("DISCORD_TOKEN"))