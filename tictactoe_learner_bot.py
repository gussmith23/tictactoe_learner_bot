import telebot
from telebot import types
import configparser
from game import Game
from random import choice
import time

since = int(time.time())

# get config
config = configparser.ConfigParser()
config.read("tictactoe_learner_bot.cfg")

games = {}
moves = {}

locs = [(0,0), (1,0), (2,0),
				(0,1), (1,1), (2,1),
				(0,2), (1,2), (2,2)]

# get bot
bot = telebot.TeleBot(config['telegram_bot_api']['telegram_token'])

markup = types.InlineKeyboardMarkup()
markup.row(types.InlineKeyboardButton(callback_data="0", text="."),
						types.InlineKeyboardButton(callback_data="1", text="."),
						types.InlineKeyboardButton(callback_data="2", text="."))
markup.row(types.InlineKeyboardButton(callback_data="3", text="."),
						types.InlineKeyboardButton(callback_data="4", text="."),
						types.InlineKeyboardButton(callback_data="5", text="."))
markup.row(types.InlineKeyboardButton(callback_data="6", text="."),
						types.InlineKeyboardButton(callback_data="7", text="."),
						types.InlineKeyboardButton(callback_data="8", text="."))
						
@bot.message_handler(commands=['playttt'], func=lambda m: m.date>since)
def new_game(message):
	chat_id = message.chat.id
	new_game = Game()
	out = bot.send_message(chat_id, "```\n" + new_game.to_string() + "```", 
			reply_markup=markup, parse_mode="Markdown")
	
	games[out.message_id] = new_game

@bot.callback_query_handler(func=lambda call: call.message.date>since and call.message.message_id in games)
def call(call):
	game = games[call.message.message_id]
	success = game.make_move(locs[int(call.data)], 0)
	if success is None:
		del games[call.message.message_id]
		return
	elif success is False:
		bot.edit_message_text("```\n" + game.to_string() + "```\nInvalid move. Please choose again.",
						message_id=call.message.message_id, chat_id=call.message.chat.id,
						parse_mode='Markdown', reply_markup=markup)
		return
	elif success == 0:
		bot.edit_message_text("```\n" + game.to_string() + "```\nYou won!",
						message_id=call.message.message_id, chat_id=call.message.chat.id,
						parse_mode='Markdown')
		del games[call.message.message_id]
		return
	elif success is True:
		bot_made_move = game.make_move(choice(locs), 1)
		while bot_made_move is False:
			bot_made_move = game.make_move(choice(locs), 1)
		if bot_made_move is None:
			bot.edit_message_text("```\n" + game.to_string() + "```\n?",
							message_id=call.message.message_id, chat_id=call.message.chat.id,
							parse_mode='Markdown')
			del games[call.message.message_id]
		elif bot_made_move is True:
			bot.edit_message_text("```\n" + game.to_string() + "```\n",
							message_id=call.message.message_id, chat_id=call.message.chat.id,
							parse_mode='Markdown', reply_markup=markup)
		elif bot_made_move == 1:
			bot.edit_message_text("```\n" + game.to_string() + "```\n( ͡° ͜ʖ ͡°)",
							message_id=call.message.message_id, chat_id=call.message.chat.id,
							parse_mode='Markdown')
			del games[call.message.message_id]
	
	

bot.polling()