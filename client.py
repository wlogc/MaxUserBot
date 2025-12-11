import json
import random
from websockets.sync.client import connect

class MaxClient:
	ws_url = "wss://ws-api.oneme.ru/websocket"
	websocket = None
	token = ""

	me = {}

	seq = 0

	def __init__(self, token):
		self.token = token

	def connect(self):
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 YaBrowser/25.8.0.0 Safari/537.36",
			"Origin": "https://web.max.ru",
			"Pragma": "no-cache",
			"Cache-Control": "no-cache",
			"Accept-Encoding": "gzip, deflate, br, zstd",
			"Accept-Language": "ru,en;q=0.9",
		}
		self.websocket = connect(self.ws_url,
				additional_headers=headers,
                origin="https://web.max.ru",
                ping_interval=20,
                ping_timeout=20)

	def auth(self):
		print("AUTH")
		connect_message = {
			"ver": 11,
			"cmd": 0,
			"seq": self.seq,
			"opcode": 6,
			"payload": {
				"userAgent": {
					"deviceType": "WEB",
					"locale": "ru",
					"deviceLocale": "ru",
					"osVersion": "Windows",
					"deviceName": "Yandex Browser",
					"headerUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 YaBrowser/25.6.0.0 Safari/537.36",
					"appVersion": "25.7.4",
					"screen": "1080x1920 1.0x",
					"timezone": "Asia/Yekaterinburg"
				},
				"deviceId": "c6267f5d-2c78-4d8f-95b5-8caa96c06df0"
			}
		}
		self.send(connect_message)
		response = self.recv()
		print("Connect MSG:", response)

		session_message = {

			"ver": 11,
			"cmd": 0,
			"seq": 1,
			"opcode": 19,
			"payload": {
				"interactive": True,
				"token": self.token,
				"chatsSync": 0,
				"contactsSync": 0,
				"presenceSync": 0,
				"draftsSync": 0,
				"chatsCount": 40
			}

		}
		self.send(session_message)
		response = json.loads(self.recv())
		self.me = response["payload"]
		print("Session MSG:", response)
		return response

	def send_message(self, chatId, text, notify=True):
		send_msg = {
			"ver": 11,
			"cmd": 0,
			"seq": self.seq,
			"opcode": 64,
			"payload": {
				"chatId": chatId,
				"message": {
					"text": text,
					"cid": random.randint(423232424, 3242533566365),
					"elements": [],
					"attaches": []
				},
				"notify": True
			}
		}
		self.send(send_msg)
		response = self.websocket.recv()
		response = json.loads(response)
		return response

	def get_user(self, id):
		j = {
			"ver": 11,
			"cmd": 0,
			"seq": 3,
			"opcode": 32,
			"payload": {
				"contactIds": id if type(id) == list else [id],
			}
		}
		self.send(j)
		response = json.loads(self.recv())
		return response

	def delete_message(self, chatId, id, forMe=False):
		j = {
			"ver": 11,
			"cmd": 0,
			"seq": self.seq,
			"opcode": 66,
			"payload": {
				"chatId": chatId,
				"messageIds": id if type(id) == list else [id],
				"forMe": forMe
			}
		}
		self.send(j)
		response = json.loads(self.recv())
		return response

	def upload_image(self, image):
		j = {
			"ver": 11,
			"cmd": 0,
			"seq": self.seq,
			"opcode": 80,
			"payload": {
				"count": 1
			}
		}
		self.send(j)
		response = json.loads(self.recv())
		return response
	def disconnect(self):
		self.websocket.close()

	def send(self, data):
		self.websocket.send(json.dumps(data))
		self.seq += 1

	def recv(self):
		try:
			response = self.websocket.recv(timeout=5)
		except:
			response = None
		return response
