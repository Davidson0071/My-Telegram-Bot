import requests

import praw

import random

import telebot

import io

TOKEN = '6203076475:AAGI6QCkSmEVJH5sPsiWa5IL1PNnSZ38thI'

OPENAI_API_KEY = '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'

# Initialize Telegram bot

bot = telebot.TeleBot(TOKEN)

# Initialize Reddit instance

reddit = praw.Reddit(client_id='3desIAbTGOb7Q3xYTicmrw',

                     client_secret='i9YnNSVI8RaJ7p4d0FtlCAPpxu7D6g',

                     user_agent='memmer')

# Define subreddit name

subreddit_names = ["memes", "dankmemes", "funny"]

# Define command to generate random meme

@bot.message_handler(commands=['meme'])

def send_random_meme(message):

    subreddit_name = random.choice(subreddit_names)

    subreddit = reddit.subreddit(subreddit_name)

    memes = subreddit.hot(limit=500)

    random_meme = random.choice(list(memes))

    response = requests.get(random_meme.url)

    if response.status_code == 200:

        photo = io.BytesIO(response.content)

        bot.send_photo(chat_id=message.chat.id, photo=photo)

    else:

        bot.reply_to(message, "Sorry, I could not retrieve the meme at this time.")

# Define function to get a joke

def get_joke():

    response = requests.get("https://v2.jokeapi.dev/joke/Any")

    data = response.json()

    if data["type"] == "single":

        return data["joke"]

    else:

        return f"{data['setup']} \n {data['delivery']}"

# Define command to start the bot and send a welcome message

@bot.message_handler(commands=['start'])

def send_welcome(message):

    bot.reply_to(message, "Hi! I am Memmer, the bot that can send you random memes and jokes. Use /meme to get a meme, /joke to get a joke, and /ask followed by a question or statement to chat with ChatGPT and receive an AI-generated response. 😜")

# Define command to get a joke

@bot.message_handler(commands=['joke'])

def send_joke(message):

    joke = get_joke()

    bot.send_message(chat_id=message.chat.id, text=joke)

# Run the bot

bot.polling()
