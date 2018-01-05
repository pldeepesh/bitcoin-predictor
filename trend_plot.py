import matplotlib.pyplot as plt
import psycopg2 as con
import json
import tkinter as tk

def rates(wise):
	# buying rates intl
	cursor.execute('select buy from '+ wise +';')
	buy_rates = cursor.fetchall()
	conn.commit()

	#sell rates intl
	cursor.execute('select sell from '+ wise +';')
	sell_rates = cursor.fetchall()
	conn.commit()


	#buying rates plot
	buy = []
	for i in buy_rates:
		buy.append(round(i[0],2))
	plt.plot(buy,label="buy_rates")
	
	# sell rates
	sell = []
	for i in sell_rates:
		sell.append(round(i[0],2))
	plt.plot(sell,label='sell_rates')

	plt.legend()
	plt.show()

def overall():
	cursor.execute('select buy from bitcoin_15;')
	buy_rates_intl = cursor.fetchall()
	conn.commit()

	cursor.execute('select sell from bitcoin_15;')
	sell_rates_intl = cursor.fetchall()
	conn.commit()

	cursor.execute('select buy from zebpay_rates;')
	buy_rates_z = cursor.fetchall()
	conn.commit()

	cursor.execute('select sell from zebpay_rates;')
	sell_rates_z = cursor.fetchall()
	conn.commit()

	plt.figure(1)
	plt.subplot(211)

	buy_intl = []
	for i in buy_rates_intl:
		buy_intl.append(round(i[0],2))
	plt.plot(buy_intl,label="buy_rates_intl")
	
	# sell rates
	sell_intl = []
	for i in sell_rates_intl:
		sell_intl.append(round(i[0],2))
	plt.plot(sell_intl,label='sell_rates_intl')

	plt.legend()
	plt.title("international bitcoin rates")

	plt.subplot(212)
	buy_z = []
	for i in buy_rates_z:
		buy_z.append(round(i[0],2))
	plt.plot(buy_z,label="buy_rates_z")
	
	# sell rates
	sell_z = []
	for i in sell_rates_z:
		sell_z.append(round(i[0],2))
	plt.plot(sell_z,label='sell_rates_z')

	plt.legend()
	plt.title("zebpay bitcoin rates")


	plt.show()

def buy_sell_difference():
	cursor.execute('select (buy-sell) as difference from zebpay_rates;' )
	difference = cursor.fetchall()
	diff = []
	for i in difference:
		diff.append(round(i[0],2))

	plt.plot(diff)
	plt.show()





if __name__ == '__main__':
	# getting credentials
	creds = json.load(open('/Users/lakshmanadeepesh/Desktop/bitcoin_predictor/config.json'))

	#connecting to the Databas
	conn = con.connect(user=creds['redshift']['user'],host=creds['redshift']['host'],port=creds['redshift']['port'],password=creds['redshift']
		['password'],database=creds['redshift']['database'])
	cursor = conn.cursor()

	# user message
	print('''select one in the two \n1.bitcoin international \n2.zebpay, india rates \n3.overall comparision chart \n4.buy,sell difference zebpay''')
	usr_input = input("enter your choice 1-4")

	if int(usr_input) == 1:
		rates('bitcoin_15')
	elif int(usr_input) == 2:
		rates('zebpay_rates')
	elif int(usr_input) == 3:
		overall()
	elif int(usr_input) == 4:
		buy_sell_difference()
	else:
		print("enter a valid number between 1 and 2")
	
	