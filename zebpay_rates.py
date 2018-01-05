import requests as re
import json
from datetime import datetime
import psycopg2 as con
import smtplib as smtp


# this method sends email to the list of email_ids in config.json
def send_mail(todo):
	server = smtp.SMTP('smtp.gmail.com',587)
	server.starttls()
	server.login(creds['email_creds']['email'],creds['email_creds']['password'])
	server.sendmail(creds['email_creds']['email'],creds['email_creds']['sender_list'],'Subject :'+todo+' Bitcoin\n')
	server.quit()



if __name__ == '__main__':
	url = 'https://www.zebapi.com/api/v1/market/ticker/btc/inr'
	headers = {'User-agent':'Mozilla 5.0'}
	creds = json.load(open('/Users/lakshmanadeepesh/Desktop/bitcoin_predictor/config.json'))

	#database connection
	conn = con.connect(user=creds['redshift']['user'],host=creds['redshift']['host'],port=creds['redshift']['port'],password=creds['redshift']
		['password'],database=creds['redshift']['database'])
	cursor = conn.cursor()

	#getting data from the API endpoint
	response = re.get(url,headers=headers)
	response = json.loads(response.text)

	cursor.execute("insert into zebpay_rates(date,price,buy,sell) values(now(),%s,%s,%s);",(response['market'],response['buy'],response['sell']))
	conn.commit()

	# All the logics and communication happens through this part of the code

	# selling prices
	cursor.execute('select max(sell) from zebpay_rates;')
	sell = cursor.fetchall()
	conn.commit()
	if response['sell']>sell[0][0] :
		sendmail("sell - highest - "+str(response['sell']))
		cursor.execute('insert into email_sent(timestamp,subject) values(now(),%s);','Sell')
		conn.commit()
	elif response['sell']<sell[0][0]:
		pass

	# buying prices
	cursor.execute('select min(buy) from zebpay_rates;')
	conn.commit()
	buy = cursor.fetchall()
	if response['buy']<buy[0][0]:
		sendmail('Buy rate lowest - '+str(response['buy']))
		cursor.execute('insert into email_sent(timestamp,subject) values(now(),%s);','Buy')
		conn.commit()
	elif response['buy']>buy[0][0]:
		pass

	# other logics
	cursor.execute('select min(buy-sell) from zebpay_rates;')
	buy_sell_difference = cursor.fetchall()
	conn.commit()
	if response['buy']-response['sell'] < buy_sell_difference[0][0]:
		send_mail('plausible - difference is '+str(response['buy']-response['sell']))


	# ending the database connection
	conn.close()



	