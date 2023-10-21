import aiohttp
import asyncio
import time
from threading import Thread
import requests
import asyncio
import os
from ..exceptions import check_exceptions
async def checker(headers, id, data, func):
	os.environ['PYTHONWARNINGS'] = "ignore::RuntimeWarning"
	x = 0
	flag = False
	result = 0
	if 60 > int(data.get("expiredIn")):
		flag = "Error"

	while x < int(data.get("expiredIn")):
		if flag == "Error":
			break
		x = x + 1
		time.sleep(1)
		response_data = requests.get(f"https://pay.ton-rocket.com/tg-invoices/{id}", headers=headers).json()
		if response_data.get("data").get("status") == "paid":
			flag = True
			break
	if flag == False:
		result = await func(api_key=headers.get("Rocket-Pay-Key"), status=False)
		return result
	elif flag == True:
		result = await func(api_key=headers.get("Rocket-Pay-Key"), status=response_data.get("data").get("status"), user_id=response_data.get("data").get("payments")[0].get("userId"))
		return result
	else:
		requests.delete(f"https://pay.ton-rocket.com/tg-invoices/{id}", headers=headers)
		check_exceptions(code=60)
		
class Donate_init:
	def __init__(self, api_key, data):
		self.headers = {
			"accept": "application/json",
			"Rocket-Pay-Key": api_key,
			"Content-Type": "application/json",
		}
		self.data = data
		self.api_key = api_key

	def __call__(self, func):
		async def wrapper(*args, **kwargs):
			loop = asyncio.get_event_loop()
			async with aiohttp.ClientSession() as session:
				async with session.post("https://pay.ton-rocket.com/tg-invoices", headers=self.headers, json=self.data) as response:
					get_data_invoice = await response.json()

			result = await func(*args, **kwargs, api_key=self.api_key, data=self.data, new_data=get_data_invoice)  # Передать аргументы в функцию
			loop.create_task(checker(self.headers,get_data_invoice.get("data").get("id"), self.data, func))
			return result
		return wrapper