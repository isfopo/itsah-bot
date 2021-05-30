import os
import discord
from dotenv import load_dotenv
from numpy import negative
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

  if cmd == 'itsah':
    await message.channel.send("Starting Analysis")
    message_count = 0
    overall_score = 0.0

    async for msg in message.channel.history(limit=LIMIT):                 
      if msg.content and not msg.author.bot and not helpers.is_command(msg):
        (prediction, score) = get_sentiment(msg.content, "model_artifacts")
        if   prediction == "positive": overall_score += score
        elif prediction == "negative": overall_score -= score
        message_count += 1

    if message_count:
      await message.channel.send(
        f"\tOverall Score: {overall_score / message_count}"
      )
    else:
      await message.channel.send("There are no messages to analyze!")

  
client.run(os.getenv("DISCORD_TOKEN"))