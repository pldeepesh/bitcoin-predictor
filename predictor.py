import json
import requests as re
from datetime import datetime


if __name__ == '__main__':
	url = 'https://blockchain.info/tobtc'
	headers = {'User-agent':'Mozilla 5.0'}
	creds = json.load(open('config.json'))

	response = re.get(url,headers=headers)
	data = json.loads(response.text)
	print(data)


