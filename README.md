# itsah-bot

A sentiment analysis bot for Discord using python and machine learning.

## Setup

### Register bot

Every Discord bot must be registered with Discord itself, so in order to do so to go the [Discord Developer Portal](https://discord.com/login?redirect_to=%2Fdevelopers%2Fapplications) and register your bot.

After following the link, login or register to your account. Once you have done that, you should see a "New Application" button in the top right corner of your screen. Clicking this will prompt you to enter a name (any name is fine, even itsah-bot) then allow you to create your application by pressing the "Create" button.

Click on the "Bot" tab on the left sidebar than click the "Add Bot" button. This will create your bot add generate a token that can be copied to your clipboard using the "Copy" button. This will be needed later for the API client, so either keep this page open or save it in a save place.

### Add Bot to a server

If you want to try this bot out on a server, make sure you have created and logged into the server you want to add it to. Back in the Discord Developer Portal, go to the "OAuth2" tab on the left sidebar. Scroll down to "SCOPES" and click the "bot" checkbox. Then scroll down to "BOT PERMISSIONS" and click "View Channels", "Send Messages", "Manage Messages" and "Read Message History" permissions. Above, there is a URL and a "Copy" button next to it. Click that button and paste the URL in your browser in a new tab or window. Choose a server to add the bot to and click "Authorize". You will need permissions to the server to add the bot.

### Clone Repo

In your terminal, navigate to the folder where you wish to add this project then paste:

`git clone https://github.com/isfopo/itsah-bot.git`

### Setup Virtual Environment

After the repo has been cloned, open the folder with the command

`cd itsah-bot`

To setup the virtual environment, type

`python3 -m venv env`

Windows users should use `python` instead of `python3`.

Then, once the virtual environment is setup, use `source env/bin/activate` to start the virtual environment.

### Install Dependencies

To install all dependencies at once, use the command `pip3 install -r requirements.txt`.

Windows users should use `pip` instead of `pip3`.

### Create .env file

This project will need a .env file to hold the API and other variables. This file should be named ".env" and contain the following:

```sh
DISCORD_TOKEN=(the token for your bot from the Discord Developer Portal)

```

### Add Dataset

The language processor will need a dataset to train it's model on, so be sure to include one in your project, with the DATASET_PATH variable in your .env file pointing to it. This dataset must be in .csv form. Several examples are included in the "Links" section of this README.

## Usage

The istah bot responds to the **"--itsah"** command. Typing **"--itsah"** in the channel will result in a overall sentiment score of ranging from -100% to 100% where higher numbers are have a more positive sentiment and lower numbers have a more negative sentiment.

### Keywords

- **"details"** - the **"details"** keyword can be used to see details (content, author, prediction and score) about individual messages on the channel. These details will be sent to your DMs as opposed to the main channel. Example: "--itsah details"
- **"user=_name_"** - the **"user=_name_"** keyword will filter the messages to only return the score for the specified user. Example: "--itsah user=isfopo"

Note: these two keywords can be used together to give you detailed analysis of one user's messages sent to your DMs.

## Links

[Create a Discord Bot by Beau Carnes](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/)

[Gather message data using a bot by Thiago Rodrigues](https://levelup.gitconnected.com/how-to-gather-message-data-using-a-discord-bot-from-scratch-with-python-2fe239da3bcd)

[Sentiment Analysis - Real Python](https://realpython.com/sentiment-analysis-python/)

[Using .env file by Miguel Grinburg](https://www.twilio.com/blog/environment-variables-python)

[Reading and Writing .csv in Python - Real Python](https://realpython.com/python-csv/)

[Twitter Sentiment Analysis Dataset by Sami Belkacem](https://www.kaggle.com/sambelkacem/twitter-sentiment-analysis-data)
