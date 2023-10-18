import requests
import random
from .exceptions import check_exceptions
class Test_Client:
	def __init__(self, api_key: str = None):
		self.headers = {
			"accept": "application/json",
			"Rocket-Pay-Key": api_key,
			"Content-Type": "application/json",
		}
	def version(self, dict_mode: bool = True):
		response = requests.get("https://dev-pay.ton-rocket.com/version", headers=self.headers).json()
		if dict_mode:
			return response
		else:
			return response.get("version")
	def info(self,):
		response = requests.get("https://dev-pay.ton-rocket.com/app/info", headers=self.headers)
		if response.status_code not in [200, 201]:
			check_exceptions(code=response.status_code)
		else:
			return response.json()

	def transfer(self, data: dict = {}):
		"""
		options in data:
			{
			"tgUserId": 5968878656,
			"currency": "TONCOIN",
			"amount": 1.23,
			"description": "test"
			}
		"""
		data["transferId"] = str(random.randint(1000000000000, 9000000000000))
		response = requests.post("https://dev-pay.ton-rocket.com/app/transfer", headers=self.headers, json=data).json()
		return response

	def withdrawal(self, data: dict = {}):
		"""
		options in data:
			{
				"network": "TON",
				"address": "EQB1cmpxb3R-YLA3HLDV01Rx6OHpMQA_7MOglhqL2CwJx_dz",
				"currency": "TONCOIN",
				"amount": 1.23,
				"withdrawalId": "abc-def",
				"comment": "You are awesome!"
			}
		"""
		data["withdrawalId"] = str(random.randint(1000000000000, 9000000000000))
		response = requests.post("https://dev-pay.ton-rocket.com/app/withdrawal", headers=self.headers, json=data).json()
		return response