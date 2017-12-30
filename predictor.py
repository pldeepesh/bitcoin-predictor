#!/usr/bin/python
import json
import requests as re
from datetime import datetime
import psycopg2 as con



if __name__ == '__main__':
	url = 'https://blockchain.info/ticker'
	headers = {'User-agent':'Mozilla 5.0'}
	creds = json.load(open('/Users/lakshmanadeepesh/Desktop/bitcoin_predictor/config.json'))

	resp = re.get(url,headers=headers)
	data = json.loads(resp.text)
	conn = con.connect(user=creds['redshift']['user'],host=creds['redshift']['host'],port=creds['redshift']['port'],password=creds['redshift']
		['password'],database=creds['redshift']['database'])
	cursor = conn.cursor()
	cursor.execute("insert into bitcoin_15(date,price,buy,sell) values(now(),%s,%s,%s);",(data['INR']['last'],data['INR']['buy'],data['INR']['sell']) )
	conn.commit()
	conn.close()


