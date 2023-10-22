import pandas as pd
import numpy as np
import datetime as dt
import json
import time
import websocket  # You can use either "python3 setup.py install" or "pip3 install websocket-client"
from threading import Lock
from dhanhq import *
from enum import Enum
try:
	import thread
except ImportError:
	import _thread as thread

# rigs 
class rigs:
	# class ticks
	class ticks:
		def trend(self):
			return list(self.f.up)
			pass
	
		def fastm(self):
			return list(self.f.fasttm)
			pass
		
		def slotm(self):
			return list(self.f.slowtm)
			pass
			
		def getdf(self):
		    	return self.f
		    	pass	
		    
		def getindex(self):
		    	return self.f.index
		    	pass	
		    
		def getopen(self):
		    	return self.f.o
		    	pass	
		    
		def gethigh(self):
		    	return self.f.h
		    	pass	
		    
		def getlow(self):
		    	return self.f.l
		    	pass	
		    
		def getclose(self):
		    	return self.f.c
		    	pass	
		    
		def getavg(self):
		    	return self.f.avg
		    	pass
		pass
		
		def __init__(self,f,p):
			ohlc = {'Open':'first',
				'High':'max',
				'Low':'min',
				'Close':'last'}
			self.f = f.resample(p,offset='15min').apply(ohlc)
			self.f['avg']=(self.f.iloc[:,0:4]).mean(axis=1)
			self.f['c'] = self.f.avg.ewm(alpha=0.5,adjust=False).mean()
			self.f['o'] = (
					(
						self.f.Open.shift(1) + self.f.c.shift(1)
					)/2
				).ewm(alpha=0.5,adjust=False).mean()

			#t = np.maximum(self.f.High,self.f.o)
			self.f['h'] = (np.maximum(
						np.maximum(
							self.f.High,
							self.f.o
							),
							self.f.c
						)
					).ewm(alpha=0.5,adjust=False).mean()

			#t = np.minimum(self.f.Low,self.f.o)
			self.f['l'] = (np.minimum(
						np.minimum(
							self.f.Low,
							self.f.o
							),
							self.f.c
						)
					).ewm(alpha=0.5,adjust=False).mean()
					
			def getsma(N):
	    			return (self.f.avg.rolling(N).mean()).fillna(0)
	    			pass
	
			def getema(s,N):
			    	k=2/(1+N)
			    	return s.ewm(alpha=k,adjust=False).mean()
			    	pass
			
			def gettma(s,N):
			    	k=2/(1+N)
			    	e1 = getema(s,N)
			    	e2 = getema(e1,N)
			    	e3 = getema(e2,N)
			    	return (3*e1) - (3*e2) + e3
			    	pass	
									
			self.f['fasttm'] = gettma(self.f.avg,12)
			
			self.f['slowtm'] = gettma(self.f.avg,24)
			
			def vals():
				if(list(self.f.o) > list(self.f.c)):
					return True
				else:
					return False			
			
			self.f['up']=vals()
			#print(self.f.shape)
			pass
		pass

	# enum type nest fix
	class nest(Enum):
		me_	= '1101194979'
	
	class fix(Enum):
		one 	= '1Min'
		fiv 	= '5Min'
		ten 	= '10Min'
		pass
	"""
	def __new__(cls,s,secid,token):
			
		return instance(cls)	
		pass
	"""
	def __init__(self,s,secid,token):
		self.s=s
		self.endpoint=str((self.s.snaps()).endpoint.value)
		self.apikey=str((self.s.snaps()).apikey.value)
		self.brokey=str((self.s.snaps()).brokey.value)
		self.secid=secid
		self.token=token
		try: # dhn connection	
			self.dhn=self.s.enter(self.nest.me_.value,self.brokey)
			funds_=self.s.funds(self.dhn)
			if(funds_>float(3000)): 
				print('Much more...')
			else: print('No more...')
		except:
			self.s.logevent('Error: dhn-con-rigs')
		# initial structure of data 
		d=[{
			"Exchange":"NFO",
			"InstrumentIdentifier":"NIFTY-I",
			"LastTradeTime":1669262572,
			"ServerTime":1669262572,
			"AverageTradedPrice":18309.69,
			"BuyPrice":18323.9,
			"BuyQty":50,
			"Close":18286.75,
			"High":18329.35,
			"Low":18297.15,
			"LastTradePrice":18325.0,
			"LastTradeQty":750,
			"Open":18310.0,
			"OpenInterest":5657350,
			"QuotationLot":50.0,
			"SellPrice":18325.1,
			"SellQty":100,
			"TotalQtyTraded":681250,
			"Value":12473476312.5,
			"PreOpen":False,
			"PriceChange":38.25,
			"PriceChangePercentage":0.21,
			"OpenInterestChange":-98200,
			"MessageType":"RealtimeResult"
		}]
		# create structure for data 
		self.f=pd.DataFrame(d)
		self.f.set_index(pd.to_datetime(self.f.LastTradeTime.apply(lambda a:dt.datetime.fromtimestamp(a))),inplace=True)
		# self.u.logevent(str(self.f))
		# delte or dro the row
		self.f=self.f.drop(self.f.index[0])
		self.start=False
		self.lockbuy=Lock()
		self.locksel=Lock()
		print(self.f)
		pass
		
	def try_(self):
		# to install this library.
		
		def Authenticate(ws):
			#print('Authenticate   -----------------------------------------------------------------------------------------------')
			print("Authenticating...")
			ws.send('{"MessageType":"Authenticate","Password":"' + self.apikey + '"}')
			
		def SubscribeRealtime(ws):
			#print('SubscribeRealtime   -----------------------------------------------------------------------------------------------')
			Exchange = "NFO"  # GFDL : Supported Values: NFO, NSE, NSE_IDX, CDS, MCX. Mandatory Parameter
			InstIdentifier = self.token  # GFDL : String of symbol name : NIFTY-I, RELIANCE, NIFTY 50, NATURALGAS-I, USDINR-I
			Unsubscribe = "false"  # GFDL : To stop data subscription for this symbol, send this value as "true"
			strMessage = '{"MessageType":"SubscribeRealtime","Exchange":"' + Exchange + '","Unsubscribe":"' + Unsubscribe + '","InstrumentIdentifier":"' + InstIdentifier + '"}'
			#print('Message : ' + strMessage)
			ws.send(strMessage)
			
		def on_message(ws, message):
			#print('on_message   -----------------------------------------------------------------------------------------------')
			#print("Response : " + message)
			m=json.loads(message)
			#print('on_message   +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
			if(m.get('MessageType')=='RealtimeResult'):
				self.f.loc[len(self.f)]=m
				self.f.set_index(pd.to_datetime(self.f.LastTradeTime.apply(lambda a:dt.datetime.fromtimestamp(a))),inplace=True)
			#print('on_message   +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
			print((self.f).shape)
			self.omnt=self.ticks(self.f.LastTradePrice,self.fix.one.value)
			print((self.omnt.getdf()).shape)
			self.fmnt=self.ticks(self.f.LastTradePrice,self.fix.fiv.value)
			print((self.fmnt.getdf()).shape)
			if (dt.time(9,30,00) < dt.datetime.now().time() < dt.time(15,30,00)):
				if((self.omnt.trend())[-1] == True and (self.fmnt.trend())[-1] == True): 
					if(self.lockbuy.locked()==False):
						self.lockbuy.acquire()
						self.s.logevent('buy fut')
						"""
						self.s.bye(self.dhn,
							self.secid,
							self.quantity,
							self.f.LastTradePrice
							)
						"""
						if(self.locksel.locked==True):
							self.locksel.release()
				if((self.omnt.trend())[-1] == False ):
		     			if(self.locksel.locked()==False):
		     				self.locksel.acquire()
		     				self.s.logevent('sell fut')
		     				"""
		     				self.s.sel(self.dhn,
		     					self.secid,
		     					self.quantity,
		     					self.f.LastTradePrice
		     					)
		     				"""	
		     				if(self.lockbuy.locked()==True):
		     					self.lockbuy.release()	     					
							
			# Authenticate : {"Complete":true,"Message":"Welcome!","MessageType":"AuthenticateResult"}
			allures = message.split(',')
			strComplete = allures[0].split(':')
			result = str(strComplete[1])
			# print('Response : ' + result)
			if result == "true":
				print('AUTHENTICATED!!!')
				SubscribeRealtime(ws)  # GFDL : Subscribes to realtime data (server will push new data whenever available)

		def on_error(ws, error):
			#print('on_error   -----------------------------------------------------------------------------------------------')
			print("Error")

		def on_close(ws):
			#print('on_close   -----------------------------------------------------------------------------------------------')
			print("Reconnecting...")
			websocket.setdefaulttimeout(30)
			ws.connect(self.endpoint)

		def on_open(ws):
			#print('on_open   -----------------------------------------------------------------------------------------------')
			# print("Connected...")
			def run(*args):
				time.sleep(1)
				Authenticate(ws)
			thread.start_new_thread(run, ())

		if __name__ == "__main__":
			print('__name__   -----------------------------------------------------------------------------------------------')
			websocket.enableTrace(False)
			ws = websocket.WebSocketApp(self.endpoint,
					on_open=on_open,
					on_message=on_message,
					on_error=on_error,
					on_close=on_close)
			ws.run_forever()
		else:
			print('__name__   -----------------------------------------------------------------------------------------------')
			websocket.enableTrace(False)
			ws = websocket.WebSocketApp(self.endpoint,
					on_open=on_open,
					on_message=on_message,
					on_error=on_error,
					on_close=on_close)
			ws.run_forever()	
		pass

	def savetofile(self):
		if(dt.datetime.now().time() >= dt.time(15,30,00)):
			self.s.logevent('saving to file')
			self.s.savetofile(self.f,'lonesec.csv')
			self.s.savetofile(self.omnt.getdf(),'lonemin.csv')
			self.s.savetofile(self.fmnt.getdf(),'lfivmin.csv')
		pass
	pass


# scrips
class scrips:
	
	### time now and preset date today
	def timenow(self):
	    	return dt.datetime.now()
	    	pass
	
	def todey(self):
	    	return (dt.datetime.now()).date()
	    	pass

	### dhn operations
	def enter(self,i,k):
		try:
			d=dhanhq(i,k)
		except:
			self.u.logeevent('Error: broker connection ')
		finally:
			return d
		pass
	    
	def funds(self,d):
	    	return (
			(
				d.get_fund_limits()
			).get('data')).get('availabelBalance')
	    	pass
			
	def getorderid(self,d,pos):
	    	return (
			(
				d.get_order_list()
		    	).get('data')[pos]).get('orderId')
	    	pass
	    
	def getsecurityid(self,d,pos):
	    	return (
			(
				d.get_order_list()).get('data')[pos]).get('securityId')
	    	pass
	
	def getorderstatus(self,d,pos):
	    	return (
			(
				d.get_order_list()
			).get('data')[pos]).get('orderStatus')
	
	def cancelorder(self,d,oid):
	    	return d.cancel_order(oid)
	    	pass
	
	def cancelall(self,d):
		k=d.get_order_list()
		for i in range(0, len(k.get('data'))):
			d.cancel_order(self.getorderid(d,i))
		pass

	def sel(self,d,secid,q,p):
		try:
			soi = d.place_order(
				    security_id=secid,   
				    exchange_segment=d.FNO,
				    transaction_type=d.SELL,
				    quantity=q,
				    order_type=d.MARKET,
				    product_type=d.INTRA,
				    price=p
				    )
		except:
			self.logevent('Error: sell order')
		finally:
			self.logevent('buy order id'+str(soi))
			return soi
		pass

	def bye(self,d,secid,q,p):
		try:
			boi = d.place_order(
				    security_id=secid,
				    exchange_segment=d.FNO,
				    transaction_type=d.BUY,
				    quantity=q,
				    order_type=d.MARKET,
				    product_type=d.INTRA,
				    price=p
				    )
		except:
			self.logevent('Error: buy order')
		finally:
			self.logevent('buy order id'+str(boi))
			return boi
		pass
	
	### epoh conversions
	def toepoch(self,yr,mo,da,ho,mi,se):
	    	return dt.datetime(yr,mo,da,ho,mi,se).timestamp()
	    	pass
	    
	def fromepoch(self,ep):
	    	return dt.datetime.fromtimestamp(ep)
	    	pass		

	### save df to csv file
	def savetofile(self,dataframe,csvfilename):
		dataframe.to_csv(csvfilename)
		print('printing file... '+csvfilename)
		pass
		
	### event log, file read write
	def logevent(self,msg):
		try:
			with open(self.i,'a') as f:
				f.write(str(self.timenow())+" "+msg+'\n')
		except:
			print('Error: logevent file open-close')
		pass

	def readevents(self):
		try:
			with open(self.i,'r') as f:
				print(f.read())
		except:
			print('Error: readevent file open-close')
		pass
	
	def printline(self,s):
		l=''
		for i in range(0,25):
	    		l+=s
		try:
			with open(self.i, 'a') as f:
				f.write(l+'\n') #msg='Error: File open-close@ {0}'.format(dt.datetime.now()) #print(msg)
		except:
			msg='Error: printline file open-close'
			print(msg)
		pass
	
	### gdfl operations 
	def gdflindex(self):
	    	return 'NIFTY&50.NSE_IDX' # 'NIFTY&BANK.NSE_IDX'
	    	pass
	    	
	# getsnaps
	def snaps(self):
	    	return self.snap
	    	pass
	
	# enum type fix
	class nest(Enum):
		me_	= '1101194979'
	def __init__(self, snap, apps): #
		self.snap=snap
		self.brokey=snap.brokey.value
		self.path=apps.path.value 
		self.ltp=apps.spotprice.value 
		self.optexpiryon=apps.optexpiryon.value 
		self.month=apps.month.value
		self.year=apps.year.value
		self.futexpiryon=apps.futexpiryon.value
		self.symbol=apps.futsymbol.value	
		self.i='log.txt'
		try: # dhn connection	
			self.dhn=self.enter(self.nest.me_.value,self.brokey)
			funds_=self.funds(self.dhn)
			if(funds_>float(3000)): 
				print('Much more...')
			else: print('No more...')
		except:
			self.logevent('Error: dhn-conn-scr')
		above=float(self.ltp+300)
		below=float(self.ltp-300)
		df=pd.read_csv(self.path)
		# NIFTY 27 JUN 72000 CALL OR, NIFTY 26 OCT
		targetday='NIFTY'+' '+self.optexpiryon+' '+self.month
		# get exchange
		exdf=df.loc[df.SEM_EXM_EXCH_ID.str.contains('NSE'),:]
		# get options
		oidf=exdf.loc[df.SEM_INSTRUMENT_NAME.str.contains('OPTI\w+'),:]
		# get all futs        
		self.fidf=exdf.loc[exdf.SEM_INSTRUMENT_NAME.str.contains('FUTI\w+'),:]
		# get options for given strike
		tddf=oidf.loc[oidf.SEM_CUSTOM_SYMBOL.str.startswith(targetday),:]
		# get withn strikes
		oit=tddf.query('SEM_STRIKE_PRICE < @above & SEM_STRIKE_PRICE > @below')
		# get all calls
		self.ces=oit.loc[oit.SEM_OPTION_TYPE.str.contains('CE'),:]
		# get all puts
		self.pes=oit.loc[oit.SEM_OPTION_TYPE.str.contains('PE'),:]
		#print(self.fidf)
		# validate in expiry is today 
		if(str((dt.datetime.now()).date()) in str(list(self.pes.SEM_EXPIRY_DATE)[0])):
			self.isexpiryday=True
		else:
		    	self.isexpiryday=False
		    	
		if(self.isexpiryday): #ltp=19667.4
			self.strike_below 	= (int((self.ltp+50)/50)*50)-50
			self.strikece 		= str(self.strike_below)+"-CE"
			self.strike_above 	= int((self.ltp+50)/50)*50
			self.strikepe 		= str(self.strike_above)+"-PE"
			self.gdfce		= self.strike_below
			self.gdfpe		= self.strike_above
			self.pes		= self.pes.loc[self.pes.SEM_TRADING_SYMBOL.str.endswith(self.strikepe),:]
			self.ces		= self.ces.loc[self.ces.SEM_TRADING_SYMBOL.str.endswith(self.strikece),:]
		else:
	    		self.strike_above 	= int((self.ltp+50)/50)*50
	    		self.strikece 		= str(self.strike_above)+"-CE"
	    		self.strike_below 	= (int((self.ltp+50)/50)*50)-50
	    		self.strikepe		= str(self.strike_below)+"-PE"
	    		self.gdfce		= self.strike_above
	    		self.gdfpe		= self.strike_below
	    		self.pes		= self.pes.loc[self.pes.SEM_TRADING_SYMBOL.str.endswith(self.strikepe),:]
	    		self.ces		= self.ces.loc[self.ces.SEM_TRADING_SYMBOL.str.endswith(self.strikece),:]
	    	# gdfl fut token
		if(self.month=='JAN'): m='Jan'
		if(self.month=='FEB'): m='Feb'
		if(self.month=='MAR'): m='Mar'
		if(self.month=='APR'): m='Apr'
		if(self.month=='MAY'): m='May'
		if(self.month=='JUN'): m='Jun'
		if(self.month=='JUL'): m='Jul'
		if(self.month=='AUG'): m='Aug'
		if(self.month=='SEP'): m='Sep'
		if(self.month=='OCT'): m='Oct'
		if(self.month=='NOV'): m='Nov'
		if(self.month=='DEC'): m='Dec'
		y = self.year[-2]+self.year[-1]
		self.niftyfut= 'NIFTY'+self.futexpiryon+self.month+y+'FUT'		# NIFTY06JAN2217200CE - NIFTY 06 JAN 22 17200 FUT
		self.gcal='NIFTY'+self.optexpiryon+self.month+y+str(self.gdfce)+'CE' 	# NIFTY06JAN2217200CE - BASE+EXPDATE(2DIGIT)-MON(3CHAR)-EXPYR(2-DIGIT)-STRIKE-CE/PE				
		self.gput='NIFTY'+self.optexpiryon+self.month+y+str(self.gdfpe)+'PE'
		#print(self.gcal)
		#print(self.gput)
		pass

	def isexpiry(self): 
		return self.isexpiryday
		pass
	
	# futs
	def gdflniftyfut(self):
		return self.niftyfut
		pass
	
	def brofutid(self): 
		t=self.fidf.loc[self.fidf.SEM_TRADING_SYMBOL.str.startswith(self.symbol),:]
		return (t.iloc[0,2:3]).to_numpy()[0]
		pass
	# calls
	def gdflcal(self):
		return self.gcal
		pass
	 
	def broceid(self): 
		return (self.ces.iloc[0,2:3]).to_numpy()[0]
		pass
	# puts     	    
	def gdflput(self):
	    	return self.gput
	    	pass
		
	def bropeid(self): 
		return (self.pes.iloc[0,2:3]).to_numpy()[0]
		pass
	pass
