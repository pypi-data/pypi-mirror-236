import requests

class Client:
	def __init__(self, api_key):
		self.headers = {
			"accept": "application/json",
			"Crypto-Pay-API-Token": api_key,
			"Content-Type": "application/json",
		}
	def get_me(self):
		response = requests.get("https://pay.crypt.bot/api/getMe", headers=self.headers).json()
		rework = dict(response)
		response_balance = requests.get("https://pay.crypt.bot/api/getBalance", headers=self.headers).json()
		rework["balance"] = response_balance.get("result")
		return rework

	def create(self, data):
		"""
		options in data:
			"asset": "TON",
			"amount": 0.01,
			"description": "test",
			"hidden_message": "test",
			"paid_btn_name": "viewItem",
			"paid_btn_url": "https://help.crypt.bot/crypto-pay-api#Invoice",
			"allow_comments": False,
			"allow_anonymous": False,
			"expires_in": 60
		"""
		response = requests.post("https://pay.crypt.bot/api/createInvoice", headers=self.headers, json=data).json()
		return response

	def transfer(self, data):
		"""
			"user_id": 5968878656,
			"asset": "TON",
			"amount": 1,
			"spend_id": 623482423712389,
			"comment": "Hello",
			"disable_send_notification": False
		"""
		response = requests.post("https://pay.crypt.bot/api/transfer", headers=self.headers, json=data).json()
		return response

	def get_invoices(self, data):
		"""
			"asset": "TON",
			"status": "paid",
			"invoice_ids": [3891640],
			"offset": 0,
			"count": 1
		"""
		response = requests.get("https://pay.crypt.bot/api/getInvoices", headers=self.headers, params=data).json()
		return response

	def rates(self):
		response = requests.get("https://pay.crypt.bot/api/getExchangeRates", headers=self.headers).json()
		return response

	def currencies(self):
		response = requests.get("https://pay.crypt.bot/api/getCurrencies", headers=self.headers).json()
		return response