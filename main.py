import os
import csv
import random
import discord
import spacy
from spacy.util import minibatch, compounding
import pandas as pd
from dotenv import load_dotenv

nlp = spacy.load("en_core_web_sm")

load_dotenv()

client = discord.Client()

LIMIT = 100
# TODO: put ML functions in separate file
def load_training_data(
    training_csv: str = "dataset/train.csv",
    split: float = 0.8,
    limit: int = 0
) -> tuple:
  messages = []
  with open(training_csv, encoding='latin-1') as f:
    csv_data = csv.reader(f, delimiter = ",")
    line_count = 0
    for row in csv_data:
      if line_count == 0: line_count += 1
      else: messages.append((row[2], { "cats": { "pos": row[1] == '1', "neg": row[1] == '0' } }))
  random.shuffle(messages)
  if limit:
    messages = messages[:limit]
  split = int(len(messages) * split)
  return messages[:split], messages[split:]

def train_model(
  training_data: list,
  test_data: list,
  iterations: int = 20
) -> None:
  nlp = spacy.load("en_core_web_sm")
  if "textcat" not in nlp.pipe_names:
    textcat = nlp.create_pipe( "textcat", config={"architecture": "simple_cnn"} )
    nlp.add_pipe(textcat, last=True)
  else:
    textcat = nlp.get_pipe("textcat")
  textcat.add_label("pos")
  textcat.add_label("neg")

  training_excluded_pipes = [ pipe for pipe in nlp.pipe_names if pipe != "textcat" ]
  with nlp.disable_pipes(training_excluded_pipes):
    optimizer = nlp.begin_training()
    #Training loop
    print("Begin training")
    print("Loss\tPrecision\tRecall\tF-score")
    batch_sizes = compounding(4.0, 32.0, 1.001)
    for i in range(iterations):
      loss = {}
      random.shuffle(training_data)
      batches = minibatch(training_data, size=batch_sizes)
      for batch in batches:
        text, labels = zip(*batch)
        nlp.update(
          text,
          labels,
          drop=0.2,
          sgd=optimizer,
          losses=loss
        )
      with textcat.model.use_params(optimizer.averages):
        evaluation_results = evaluate_model(
          tokenizer=nlp.tokenizer,
          textcat=textcat,
          test_data=test_data
        )
        print(
            f"{loss['textcat']}\t{evaluation_results['precision']}"
            f"\t{evaluation_results['recall']}"
            f"\t{evaluation_results['f-score']}"
        )

  with nlp.use_params(optimizer.averages):
      nlp.to_disk("model_artifacts")

def evaluate_model( tokenizer, textcat, test_data: list ) -> list:
  messages, labels = zip(*test_data)
  messages = (tokenizer(message) for message in messages)
  true_positives = 0
  false_positives = 1e-8
  true_negatives = 0
  false_negatives = 1e-8
  for i, message in enumerate(textcat.pipe(messages)):
    for predicted_label, score in message.cats.items():
      if   predicted_label == "neg": continue
      if   score >= 0.5 and labels[i]["cats"]["pos"]: true_positives  += 1
      elif score >= 0.5 and labels[i]["cats"]["neg"]: false_positives += 1
      elif score <  0.5 and labels[i]["cats"]["neg"]: true_negatives  += 1
      elif score <  0.5 and labels[i]["cats"]["pos"]: false_negatives += 1
  precision = true_positives / (true_positives + false_positives)
  recall = true_positives / (true_positives + false_negatives)

  if precision + recall == 0: f_score = 0
  else: f_score = 2 * (precision * recall) / (precision + recall)
  return {"precision": precision, "recall": recall, "f-score": f_score}

def test_model(input_data, model_directory: str) -> tuple:
  loaded_model = spacy.load(model_directory)
  #Generate Prediction
  parsed_text = loaded_model(input_data)
  #Determine prediction to return
  if parsed_text.cats["pos"] > parsed_text.cats["neg"]:
    prediction = "positive"
    score = parsed_text.cats["pos"]
  else:
    prediction = "negative"
    score = parsed_text.cats["neg"] # TODO: should return score and prediction instead of printing
  return (prediction, score)

def get_sentiment(text: str, model_directory, limit = 2500) -> tuple:
  score = 0
  prediction = None

  while not score or not prediction:
    try:
      (score, prediction) = test_model(text, model_directory)
    except (OSError, FileNotFoundError):
      train, test = load_training_data(limit=limit)
      train_model(train, test)
    if score and prediction:
      return (score, prediction)

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
  else: return

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

(score, prediction) = get_sentiment("Transcendently beautiful in moments outside the office, it seems almost sitcom-like in those scenes. When Toni Colette walks out and ponders life silently, it's gorgeous.", "model_artifacts")

print(
  f"Predicted sentiment: {prediction}"
  f"\tScore: {score}"
)

  
client.run(os.getenv("DISCORD_TOKEN"))