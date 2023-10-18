import requests
from .exceptions import check_exceptions

class Client:
	def __init__(self, api_key: str = None):
		self.headers = {
			"accept": "application/json",
			"Rocket-Pay-Key": api_key,
		}

	def version(self, dict_mode: bool = True, testnet: bool = False):
		response = requests.get("https://pay.ton-rocket.com/version", headers=self.headers).json()
		if dict_mode:
			return response
		else:
			return response.get("version")


	def info(self,):
		response = requests.get("https://pay.ton-rocket.com/app/info", headers=self.headers)
		if response.status_code not in [200, 201]:
			check_exceptions(code=response.status_code)
		else:
			return response.json()