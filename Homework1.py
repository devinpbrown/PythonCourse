import traceback
import random
stockrandom = random.uniform(0.5, 1.5) #generated for selling stock
mfrandom = random.uniform(0.9, 1.2) #generated for selling mf

class customException(Exception): #for raising exceptions throughout
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return self.value

class Portfolio(object):

	def __init__(self):
		self.id = dict({'Cash': float(0), 'Stocks': {}, 'Mutual Funds': {}})
		self.log = []

	def __str__(self): #print function
		return "Cash: $%.2f \nStocks: %s \nMutual Funds: %s" %(self.id['Cash'], self.id['Stocks'], self.id['Mutual Funds'])

	def history(self): #view log of transactions
		print(*self.log, sep = "\n")

	def addCash(self, amount):
		try:
			if amount >= 0: #prevents negative values from being added
				self.id['Cash'] += amount #adding to cash account
			else:
				return print("You cannot add a negative amount to your 'Cash' account.")
		except: #catches random errors like entering strings
			print("Make sure you entered your number correctly.")
			return None
		else:
			self.log.append(f"Added ${amount} to 'Cash'.") #adds cash deposit to log

	def withdrawCash(self, amount):
		try:
			if amount > self.id['Cash']: #prevents overdraft
				raise customException("Insufficient Funds.")
			elif amount < 0:
				raise customException("You cannot withdraw a negative value.")
		except customException as inst:
			print(inst.value)
			return None
		except: #catches random errors like entering strings
			print("Make sure you entered your number correctly.")
			return None
		else:
			self.id['Cash'] -= amount #withdrawing from Cash
			self.log.append(f"Withdrew ${amount} from 'Cash'.") #adding transaction to log

	def buyStock(self, asset, shares):
		try:
			if shares*asset.price > self.id['Cash']: #prevents overdraw
				raise customException("Insufficient Funds.")
			elif shares%1 != 0: #prevents buying fractions of stocks
				raise customException("Stocks can only be purchased in whole quantities.")
			else:
				self.withdrawCash(shares*asset.price) #takes money from cash account
				self.log.pop() #takes off the log addition from withdrawCash function
				self.log.append(f"Purchased {shares} shares of stock {asset.ticker} for ${shares*asset.price}.") #adds transaction to log
		except customException as inst:
			print(inst.value)
			return None
		except: #catches random errors like entering non-assets or strings
			print("Please re-enter your values.")
			return None
		try:
			self.id['Stocks'][asset.ticker] += shares #checks if stock already owned, if so, adds shares, if not spits error
		except KeyError:
			self.id['Stocks'][asset.ticker] = shares #creates new entry for the new stock


	def sellStock(self, asset, shares):
		try:
			if shares > self.id['Stocks'][asset.ticker]: #preventing overdraft
				raise customException("Insufficient stock.")
			if shares %1 != 0: #makes sure you only sell whole number values of stock
				raise customException("Stocks can only be sold in whole quantities.")
			else:
				x = int(shares*asset.price*stockrandom*100)/100.0 #generates the selling price for stock, rounded to 2 decimal places
				self.addCash(x)
				self.log.pop() #takes off the log addition from addCash function
				self.log.append(f"Sold {shares} shares of stock {asset.ticker} for ${x}.") #adds transaction to log
		except customException as inst:
			print(inst.value)
			return None
		except KeyError: #prevents selling stock not in portfolio
			print("Stock not found in portfolio.")
			return None
		except: #catches random errors like entering strings or non-stocks etc.
			print("Please re-enter your values")
			return None

		if shares == self.id['Stocks'][asset.ticker]: #if all shares sold, deletes entry
			del self.id['Stocks'][asset.ticker]
		else:
			self.id['Stocks'][asset.ticker] -= shares

	def buyMutualFund(self, asset, shares):
		try:
			if shares > self.id['Cash']: #prevent overdraft
				raise customException("Insufficient Funds.")
			elif asset.price != 1:
				raise customException("Make sure you entered a mutual fund, not a stock.")
			else:
				self.withdrawCash(shares) #takes cash
				self.log.pop() #removes log entry from withdrawCash function
				self.log.append(f"Purchased {shares} shares of mutual fund {asset.ticker} for ${shares}.") #adds tranasction to log
		except customException as inst:
			print(inst.value)
			return None
		except: #catches random errors like entering non-asset objects
			print("Please re-enter your values.")
			return None
		try:
			self.id['Mutual Funds'][asset.ticker] += shares #checks for mutual fund in portfolio and adds shares, if not spits KeyError
		except KeyError:
			self.id['Mutual Funds'][asset.ticker] = shares #creates new entry for the new Mutual Fund


	def sellMutualFund(self, asset, shares):
		try:
			if shares > self.id['Mutual Funds'][asset.ticker]: #prevents overdraft
				raise customException("Insufficient shares of mutual fund.")
			else:
				y = int(shares*mfrandom*100)/100.0 #generates sell price for mf rounded to 2 decimal places
				self.addCash(y)
				self.log.pop() #takes off the log addition from addCash function
				self.log.append(f"Sold {shares} shares of mutual fund {asset.ticker} for ${y}.") #adds transaction to log
		except customException as inst:
			print(inst.value)
			return None
		except KeyError: #prevents selling mf not in port
			print("Mutual fund not found in portfolio.")
			return None
		except: #random errors
			print("Please re-enter your values.")
			return None

		if shares == self.id['Mutual Funds'][asset.ticker]: #if all shares sold, deletes entry from port
			del self.id['Mutual Funds'][asset.ticker]
		else:
			self.id['Mutual Funds'][asset.ticker] -= shares #subrtracts shares from portfolio


class Asset(object):
	def __init__(self, ticker, price=1):
		self.ticker = ticker
		self.price = price

class Stock(Asset):
	pass
#s1 = Stock('Stock1', 20)
#s2 = Stock ('Stock2', 10)

class MutualFund(Asset):
	pass
mf1 = MutualFund('MF1')
#mf2 = MutualFund('MF2')

#a=Portfolio()
#a.addCash(100)
#a.buyMutualFund(mf1, 50)
#a.history()
