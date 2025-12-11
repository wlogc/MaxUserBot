import json
import os

import config
from client import MaxClient

from telebot import TeleBot

bot = TeleBot(config.BOT_TOKEN)
bot_send_id = config.TG_SEND_ID

client = MaxClient(config.MAX_TOKEN)
client.connect()
client.auth()

my_id = client.me["profile"]["contact"]["id"]

detect_chat = config.MAX_CHAT_ID

while True:
	recv = client.recv()
	if recv:
		recv = json.loads(recv)

		if recv['opcode'] == 128 and not recv["payload"] is None:
			sender = recv["payload"]["message"]["sender"]
			chatId = recv["payload"]['chatId']

			if 'status' in recv["payload"]['message'].keys():
				if recv["payload"]["message"]["status"] == 'REMOVED':
					continue

			if sender == my_id:
				msg = recv["payload"]["message"]["text"].split()
				if len(msg) != 0:
					msg_id = recv["payload"]["message"]["id"]
					if msg[0] == ".ping":
						client.send_message(chatId,"PONG")
						client.delete_message(chatId, msg_id)

					if msg[0] == ".calc":
						try:
							client.send_message(chatId,eval(" ".join(msg[1:])))
						except:
							pass
						client.delete_message(chatId, msg_id)
					if msg[0] == ".run":
						try:
							exec(" ".join(msg[1:]))
						except:
							pass
						client.delete_message(chatId, msg_id)
					if msg[0] == ".setMax":
						m = bot.send_message(bot_send_id, f"Чат в Max с id: {chatId} установлен как основа!")
						detect_chat = chatId
						client.delete_message(chatId,msg_id)
						continue

					if msg[0] == ".setTg":
						m = bot.send_message(bot_send_id, f"Чат в Тг с id: {msg[1]} установлен как основа!")
						bot_send_id = msg[1]
						client.delete_message(chatId, msg_id)
						continue

			if chatId != detect_chat:
				continue

			try:
				user = client.get_user(sender)

				nickname = user['payload']['contacts'][0]['names'][0]['firstName'] + " " + \
						   user['payload']['contacts'][0]['names'][0]['lastName']

				if recv["payload"]["message"]["text"] != '':
					bot.send_message(bot_send_id, f"[{nickname}]: {recv['payload']['message']['text']}")

				for i in recv["payload"]["message"]["attaches"]:
					if i["_type"] == "PHOTO":
						bot.send_photo(bot_send_id, i['baseUrl'], caption=f"[{nickname}]: ")
			except:
				pass

	else:
		j = {
			"ver": 11,
			"cmd": 0,
			"seq": client.seq,
			"opcode": 1,
			"payload": {
				"interactive": False
			}
		}
		client.send(j)
