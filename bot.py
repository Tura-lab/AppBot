from telegram.ext import Updater, CommandHandler
import logging
import os, sys, re
import string
import random
import requests
from functools import partial
import time
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)
from telegram.ext import MessageHandler, Filters
import requests
from bs4 import BeautifulSoup as bs

updater = Updater(token= '943716178:AAGZ1O-X1EBqzF250jmf2ibGOZlE323Gq-A', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' ,level=logging.INFO)

def start(update, context):
	context.bot.send_message(chat_id=update.message.chat_id, text="Welcome to The_APKs_Bot \nAll you need to do is send me the name of the app.. I will Take care of the rest!!")

def send(update, context):
    final = ""
    
    USER_AGENT = 'Chrome'
    headers = { 'User-Agent': USER_AGENT }
    
    app = update.message.text
    app = app.replace(' ', '+')
    
    url = 'https://m.apkpure.com/search?q={}'.format(app)
    r = requests.get(url, headers = headers)

    soup = bs(r.text, 'html.parser')
    divs = soup.findAll( "a" , { "class" : "dd" })
    i=1
    context.bot.send_message(chat_id=update.message.chat_id, text = "Give me a second.. Im searching")
    
    for di in divs:
        web_site = 'https://m.apkpure.com'
        title = di.find(class_='p1').contents[0]
        link = di['href']
        link = web_site+link
        r = requests.get(link, headers = headers)
        s = bs(r.text, "html.parser")
        dwnl = s.findAll( "a" , { "class" : "da" })[0]
        dwn = web_site+dwnl['href']
        size = dwnl.find_all('span')[-1].contents[0]

        tell_title = "{}){}".format(i, title) + "\n"
        tell_size = "Size --> {}".format(size) + "\n"
        tell_link = "Download --> {}".format(dwn) + "\n"
        lines = "*"*5 + "\n" + "*"*5 + "\n"
        final += str(tell_title)
        final += str(tell_size)
        final += str(tell_link)
        final += str(lines)

        i+=1
    
    if len(divs) is not 0:
    	context.bot.send_message(chat_id=update.message.chat_id, text = final)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text = "No apps for your search.. please try again with a more general search.. Thank you!!")

send_handler = MessageHandler(Filters.text, send)
dispatcher.add_handler(send_handler)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()


