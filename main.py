import logging
import os
import discord
from datetime import datetime
from dotenv import load_dotenv
from sentiment_analysis import get_sentiment
from sentiment_analysis import load_training_data
from sentiment_analysis import train_model
from helpers import *

logging.basicConfig(filename='.log', level=logging.INFO)

load_dotenv()

client = discord.Client()


@client.event
async def on_ready():
  print(f'logged in as {client.user}')
  logging.info(f'log in as {client.user} at {datetime.now()}')
  if not os.path.isdir(os.getenv("MODEL_PATH")):
    train, test = load_training_data(os.getenv("TRAINING_DATASET_PATH"), rating_column=1, text_column=2)
    train_model(train, test, os.getenv("MODEL_PATH"))


@client.event
async def on_message(message):
  if message.author == client.user or message.author.bot:
    return
  elif message.content.startswith("--"):
    cmd = message.content.split()[0].replace("--", "")
    params = message.content.split()[1:] if len(message.content.split()) > 1 else []
  else: return

  if cmd == 'senti':
    response_message = await message.channel.send("Starting analysis...")
    logging.info(f"{message.author} called \"{message.content}\" at {datetime.now()}")
    message_count = 0
    overall_score = 0.0
    details = []

    user_param = extract_param(params, "user")

    async for msg in message.channel.history(limit=1000):                 
      if msg.content and not msg.author.bot and not is_command(msg):
        if user_param and not msg.author.name == user_param:
          continue
        prediction, score = get_sentiment(msg.content, os.getenv("MODEL_PATH"), os.getenv("TRAINING_DATASET_PATH"), rating_column=1, text_column=2)
        details.append({"content": msg.content, "author": msg.author.name, "prediction": prediction, "score": score})
        if   prediction == "positive": overall_score += score
        elif prediction == "negative": overall_score -= score
        message_count += 1

    if not "details" in params:
      if message_count:
        await response_message.edit(
          content=f"\tOverall Score for {user_param if user_param else 'channel'}: {to_percent(overall_score / message_count)}%"
        )
      else:
        await response_message.edit(content="There are no messages to analyze!")

    elif "details" in params:
      details_message = ""
      details.reverse()
      for detail in details:
        details_message += f"Message: {detail['content']} \tAuthor: {detail['author']} \tPrediction: {detail['prediction']} \tScore: {to_percent(detail['score'])}%\n"
      if message_count:
        details_message += f"\nOverall Score: {to_percent(overall_score / message_count)}%"
      await message.author.send(details_message if details_message else f"{user_param} has no messages in this channel.")
      await response_message.edit(content="Details have been sent to your DM", delete_after=30.0)


if __name__ == "__main__":
  client.run(os.getenv("DISCORD_TOKEN"))