import pandas as pd
from enum import Enum
from dhanhq import *
import datetime as dt
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
