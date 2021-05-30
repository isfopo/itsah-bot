import os
import discord
from dotenv import load_dotenv
from sentiment_analysis import get_sentiment
import helpers

load_dotenv()

client = discord.Client()

LIMIT = 1000

@client.event
async def on_ready():
    print(f'logged in as {client.user}')

@client.event
async def on_message(message):
  if message.author == client.user or message.author.bot:
    return
  elif message.content.startswith("--"):
    cmd = message.content.split()[0].replace("--", "")
    params = message.content.split()[1:] if len(message.content.split()) > 1 else [] #IDEA: use params to get the sentiment from a particular user like "user=isfopo"
  else: return

  if cmd == 'itsah':
    await message.channel.send("Starting Analysis") # TODO: maybe this can be deleted when analysis is done or show progress
    message_count = 0
    overall_score = 0.0
    details = []

    user_param = helpers.extract_param(params, "user")

    async for msg in message.channel.history(limit=LIMIT):                 
      if msg.content and not msg.author.bot and not helpers.is_command(msg):
        if user_param and not msg.author.name == user_param:
          continue
        (prediction, score) = get_sentiment(msg.content, "model_artifacts")
        details.append({"content": msg.content, "author": msg.author.name, "prediction": prediction, "score": score})
        if   prediction == "positive": overall_score += score
        elif prediction == "negative": overall_score -= score
        message_count += 1

    if not "details" in params:
      if message_count:
        await message.channel.send(
          f"\tOverall Score for {user_param if user_param else 'channel'}: {overall_score / message_count}"
        )
      else:
        await message.channel.send("There are no messages to analyze!")

    elif "details" in params:
      details_message = ""
      details.reverse()
      for detail in details:
        details_message += f"Message: {detail['content']} \tAuthor: {detail['author']} \tPrediction: {detail['prediction']} \tScore: {detail['score']}\n"
      details_message += f"\nOverall Score: {overall_score / message_count}"
      await message.author.send(details_message)

  
client.run(os.getenv("DISCORD_TOKEN"))