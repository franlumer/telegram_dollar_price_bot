import telebot
import messages as msg
import dolar_scrape as ds

token = "8093397130:AAFehKhYsn7duX78MkOBhIqpJdl4a237Tbc"
print("...")

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, msg.start)
	bot.send_message(message.chat.id, msg.info)
	print(message.chat.id)
	
@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, msg.help)

@bot.message_handler(func=lambda message: True)
def echo_all(message):

	print(message.text)

	match message.text:
		case msg if msg in ds.coins:
			response = ds.search(message.text)
			bot.reply_to(message, response)

		case "todo":
			response = ds.search("everyone")
			bot.reply_to(message, response)

		case _: 
			bot.reply_to(message, "comando no reconocido")
    
bot.infinity_polling()