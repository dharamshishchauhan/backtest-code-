
import pandas as pd
import talib as tb
import copy
import datetime
from datetime import date
import zerodha as th
#for buy swing risk reward 1/15 for sellin best is intraday sl=atr and target is leaved or 1/20 riskreward for selling swing.


obj1=th.Tradehull("api key"," api secret key",'yes')
kite=obj1.kite
y=0
x=0
z=2
a=2
b=2
c=2
buy_price=0
sl=0
sell_price=0
tr=0
tr1=0
trs=0
tr12=0
#watchlist =['ASIANPAINT', 'AUROPHARMA', 'BALKRISIND', 'BERGEPAINT', 'BHARTIARTL', 'BIOCON', 'BRITANNIA', 'CIPLA', 'COLPAL', 'DABUR', 'DIVISLAB', 'DRREDDY', 'ESCORTS', 'GMRINFRA', 'HINDUNILVR', 'IGL', 'NAUKRI', 'JUBLFOOD', 'LUPIN', 'MGL', 'MUTHOOTFIN', 'NESTLEIND', 'PIDILITIND', 'RELIANCE', 'SRF', 'SHREECEM', 'TATACONSUM', 'TORNTPHARM', 'TORNTPOWER']
'''for item in watchlist:
    M=item+'-EQ'
    name1.append(M)'''
watchlist=['ASIANPAINT','HDFCBANK','TATASTEEL','RELIANCE']    
watchlist=['NIFTY BANK','NIFTY 50']   
watchlist = ['ADANIPORTS', 'TATAMOTORS', 'SBIN', 'NATIONALUM', 'RECLTD', 'TATAPOWER', 'ASHOKLEY','CANBK','JSWENERGY','TORNTPHARM','GRASIM','INDUSINDBK','TCS','TITAN','TATASTEEL','HINDALCO','BPCL','TVSMOTOR','ADANIENT','PNB','BAJAJFINSV','DLF','HAVELLS','JSWSTEEL','VEDL','INDIGO','BHEL','HAL','ADANIPOWER']
'''watchlist2=['JSWENERGY','TORNTPHARM','GRASIM','INDUSINDBK','TCS','TITAN','TATASTEEL','HINDALCO','BPCL','TVSMOTOR']
watchlist4=['ADANIENT','PNB','BAJAJFINSV','DLF','HAVELLS','JSWSTEEL','VEDL','INDIGO','BHEL','HAL','ADANIPOWER']
watchlist=['NIFTY 50']'''
watchlist=['ADANIENT','BHEL','SBIN','HAL','DLF']
watchlist=['ADANIENT','BHEL','SBIN','DLF']


'''fut_watchlist=[]
for item in watchlist:
    data = obj1.get_fut_scripts(item)[0]
    fut_watchlist.append(data)'''
#name1 = ['ADANIPORTS-EQ','COALINDIA-EQ', 'TATAMOTORS-EQ', 'SBIN-EQ', 'NATIONALUM-EQ', 'RECLTD-EQ', 'TATAPOWER-EQ', 'TATAMOTORS-EQ', 'NTPC-EQ', 'ASHOKLEY-EQ','CANBK-EQ']

all_trade1=[]
order_dict1={'script':None,'buy/sell':None,'date':None,'entry':None,'exit':None,'stoploss':None ,'exit_time':None,'lot_size':25,'percent_return':None,'gap':None,'can_color':None, 'ema200':None,'ema150':None,'tade_and_ema':None,'number_lopp':None,'high_from_entry':None,'low_from_entry':None}
high1=0
low1=0
m=0
multi=0.20
time_entr='09:15:00'
upside=0
dwside=0
b=0
s=0
ad=0
riskre=10
num_trade=0
lp=0
upside5=0
dwside5=0
test_high=0
test_low=50000000
total_stock=0
l1=[]
loop=0
loop2=0

for name in watchlist:
    if y==10:
        all_trade1.append(copy.deepcopy(order_dict1))
        y=0
      
    try:
        data2=obj1.get_long_length_hist_data_specific_dur(name=name,exchange="NSE",interval="15minute",from_date='2017-01-01',download_till_date='2018-12-31',oi=False)
    except Exception as e:
        print('problem  ',e)
    #data4=obj1.get_long_length_hist_data_specific_dur(name=name,exchange="NSE",interval="day",from_date='2019-01-01',download_till_date='2024-08-31',oi=False)
    data2['atr(14)'] = tb.ATR(data2['high'], data2['low'], data2['close'], timeperiod=50)
    data2['ema200']= tb.EMA(data2['close'], timeperiod=200)
    data2['ema150']= tb.EMA(data2['close'], timeperiod=150)
   
    total_len=len(data2)
    #total_len2=len(data4)
    if name=='NIFTY 50':
        multi=0.31
    for i in range (201,total_len):
        test_data=data2.iloc[i]
        if test_data['ema200']>test_data['high'] and test_data['ema150']>test_data['high'] and dwside==0 :
            dwside=10
            upside=0
    
        if test_data['ema200']<test_data['low'] and test_data['ema150']<test_data['low'] and upside==0 :
            upside=10
            dwside=0

        if y==0 and (upside==10 or dwside==10):
            order_dict1['script']=name
            if upside==10:
                order_dict1['buy/sell']='buy'
                b=10
                s=0
            if dwside==10:
                order_dict1['buy/sell']='sell'
                s=10
                b=0
            order_dict1['date']=test_data['date']
            loop=1
            order_dict1['entry']=test_data['close']
            sell_price=test_data['close']
            sl=test_data['atr(14)']
            order_dict1['ema200']=test_data['ema200']
            order_dict1['ema150']=test_data['ema150']
            #order_dict1['can_color']=(sell_price-test_data['open'])/test_data['open']*100
            '''if (sl/sell_price)*100<multi:
                sl=(multi/100)*sell_price'''

            order_dict1['stoploss']=(sl/sell_price)*100
            order_dict1['tade_and_ema']=(abs(test_data['ema200']-sell_price)/sell_price)*100
            lp=i-125
            for t in range (lp,i):
                test_data5=data2.iloc[t]
                if test_data5['high']>test_high:
                    test_high=test_data5['high']
                if test_data5['low']<test_low:
                    test_low=test_data5['low']

                if test_data5['ema200']>test_data5['high'] and test_data5['ema150']>test_data5['high'] and dwside5==0 :
                    dwside5=10
                    upside5=0
                    num_trade=num_trade+1
    
                if test_data5['ema200']<test_data5['low'] and test_data5['ema150']<test_data5['low'] and upside5==0 :
                    upside5=10
                    dwside5=0
                    num_trade=num_trade+1
            order_dict1['number_lopp']=num_trade-1
            order_dict1['high_from_entry']=-(test_high-test_data['close'])/test_high*100
            order_dict1['low_from_entry']=-(test_low-test_data['close'])/test_low*100
            low_e=-(test_low-test_data['close'])/test_low*100

            num_trade=0
            upside5=0
            dwside5=0
            test_high=0
            test_low=50000000

            y=10
            ad=0
            continue
        

        if y==10 and (str(test_data['date'])[11:19]=='09:15:00' or loop==1) and b==10 and sl>0.5 and 20>low_e>3 :
            entry1=test_data['close']
            loop=0
        if (y==10 or loop2==1) and (str(test_data['date'])[11:19]=='15:15:00' or loop2==1) and b==10 and sl>0.5 and 20>low_e>3:
            exit1=test_data['close']
            final_move=((exit1-entry1)/entry1)*100
            l1.append(final_move)
            loop2=0

            
        if y==10 and dwside==10 and upside==0 and b==10:
            order_dict1['exit']=test_data['close']
            order_dict1['exit_time']=test_data['date']
            order_dict1['percent_return']=((test_data['close']-sell_price)/sell_price)*100
            all_trade1.append(copy.deepcopy(order_dict1))
            y=0
            loop2=1
        if y==10 and test_data['low']<(sell_price-sl) and b==10 :
            order_dict1['exit']=test_data['close']
            order_dict1['exit_time']=test_data['date']
            order_dict1['percent_return']=((test_data['close']-sell_price)/sell_price)*100
            all_trade1.append(copy.deepcopy(order_dict1))
            y=0   
            upside=11
            loop2=1
        if y==11 and test_data['high']>(sell_price+(riskre*sl)) and b==10:
            order_dict1['exit']=test_data['close']
            order_dict1['exit_time']=test_data['date']
            exit_price=test_data['close']-sell_price
            if b==10:
                order_dict1['percent_return']=(exit_price/sell_price)*100
            if s==10:
                order_dict1['percent_return']=-(exit_price/test_data['close'])*100
            all_trade1.append(copy.deepcopy(order_dict1))
            y=0
            loop2=1
            if b==10:
                upside=11
            if s==10:
                dwside=11
        


        if y==10 and dwside==0 and upside==10 and s==10:
            order_dict1['exit']=test_data['close']
            order_dict1['exit_time']=test_data['date']
            order_dict1['percent_return']=-((test_data['close']-sell_price)/sell_price)*100
            all_trade1.append(copy.deepcopy(order_dict1))
            y=0
            loop2=1
        if y==10 and test_data['high']>(sell_price+sl) and s==10 :
            order_dict1['exit']=test_data['close']
            order_dict1['exit_time']=test_data['date']
            order_dict1['percent_return']=-((test_data['close']-sell_price)/sell_price)*100
            all_trade1.append(copy.deepcopy(order_dict1))
            y=0 
            dwside=11
            loop2=1
        if y==11 and test_data['low']<(sell_price-(riskre*sl)) and s==10:
            order_dict1['exit']=test_data['close']
            order_dict1['exit_time']=test_data['date']
            exit_price=test_data['close']-sell_price
            if b==10:
                order_dict1['percent_return']=(exit_price/test_data['close'])*100
            if s==10:
                order_dict1['percent_return']=-(exit_price/sell_price)*100
            all_trade1.append(copy.deepcopy(order_dict1))
            y=0
            if b==10:
                upside=11
            if s==10:
                dwside=11
        

        if str(test_data['date'])[11:19]=='15:15:00' and y==10 :
            ad=ad+1
        if str(test_data['date'])[11:19]=='15:15:00' and y==10 and ad==7 :
            order_dict1['exit']=test_data['close']
            order_dict1['exit_time']=test_data['date']
            exit_price=test_data['close']-sell_price
            if b==10:
                order_dict1['percent_return']=(exit_price/sell_price)*100
            if s==10:
                order_dict1['percent_return']=-(exit_price/sell_price)*100
            all_trade1.append(copy.deepcopy(order_dict1))
            y=0
            loop2=1
            if b==10:
                upside=11
            if s==10:
                dwside=11
                
        


k=pd.DataFrame(all_trade1)
k.to_csv('all buy and sell ema 200 15 min cae market backtest.csv')
