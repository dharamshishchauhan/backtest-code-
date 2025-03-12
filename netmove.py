
import pandas as pd
import talib as tb
import copy
import datetime
from datetime import date
import zerodha as th
#for buy swing risk reward 1/15 for sellin best is intraday sl=atr and target is leaved or 1/20 riskreward for selling swing.


obj1=th.Tradehull("api key","secret key",'yes')
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
watchlist=['NIFTY 50']   
'''fut_watchlist=[]
for item in watchlist:
    data = obj1.get_fut_scripts(item)[0]
    fut_watchlist.append(data)'''
#name1 = ['ADANIPORTS-EQ','COALINDIA-EQ', 'TATAMOTORS-EQ', 'SBIN-EQ', 'NATIONALUM-EQ', 'RECLTD-EQ', 'TATAPOWER-EQ', 'TATAMOTORS-EQ', 'NTPC-EQ', 'ASHOKLEY-EQ','CANBK-EQ']

all_trade1=[]
order_dict1={'script':None,'buy/sell':None,'date':None,'entry':None,'exit':None,'stoploss':None,'stoploss2': None ,'exit_time':None,'lot_size':25,'percent_return':None,'gap':None,'gap_3pm':None,'net_change':None,'can_color':None, 'high1':None,'low1':None,'pre_day_move':None,'preday22':None,'day':None}
high1=0
low1=0
m=0
multi=0.15
time_entr='09:15:00'
tra1=0
tra2=0
sell_price2=18000
from datetime import datetime
def date_to_day(date_str):
    # Convert the string date to a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    # Get the day of the week
    day_of_week = date_obj.strftime("%A")
    return day_of_week

for name in watchlist:
    data2=obj1.get_long_length_hist_data_specific_dur(name=name,exchange="NSE",interval="5minute",from_date='2019-01-01',download_till_date='2024-08-31',oi=False)
    data4=obj1.get_long_length_hist_data_specific_dur(name=name,exchange="NSE",interval="day",from_date='2019-01-01',download_till_date='2024-08-31',oi=False)
    data2['atr(14)'] = tb.ATR(data2['high'], data2['low'], data2['close'], timeperiod=14)
   
    total_len=len(data2)
    total_len2=len(data4)
    if name=='NIFTY 50':
        multi=0.25
    for i in range (15,total_len):
        test_data=data2.iloc[i]
        if str(test_data['date'])[11:19]==time_entr:

            sl=test_data['atr(14)']
            sell_price=test_data['close']
            sell_price2=test_data['close']
            order_dict1['stoploss']=(sl/sell_price)*100
            #order_dict1['can_color']=(sell_price-test_data['open'])/test_data['open']*100
            if (sl/sell_price)*100<multi:
                sl=(multi/100)*sell_price
            

            test_data2=data2.iloc[i-1]
            test_data4=data2.iloc[i-7]
            order_dict1['gap']=-((test_data2['close']-test_data['close'])/test_data2['close'])*100
            order_dict1['gap_3pm']=-((test_data4['close']-test_data['close'])/test_data4['close'])*100
            date_today=str(test_data['date'])[0:10]
            order_dict1['day']=date_to_day(date_today)
            order_dict1['stoploss2']=(test_data2['atr(14)']/test_data2['close'])*100
            #order_dict1['lot_size']=obj1.get_lot_size(fut_watchlist[ty])
            trade_date=str(test_data2['date'])[0:10]
            for p in range (1,total_len2):
                test_data5=data4.iloc[p]
                if trade_date==str(test_data5['date'])[0:10]:
                    open_day=test_data5['open']
                    close_day=test_data5['close']
                    percent_move=-(open_day-close_day)/open_day*100
                    order_dict1['pre_day_move']=percent_move
                    open2=data4.iloc[p-1]['open']
                    close2=data4.iloc[p-1]['close']
                    order_dict1['preday22']=(close2-open2)/open2*100  
                    break
        if str(test_data['date'])[11:19]==time_entr and y==0:
            order_dict1['script']=name
            order_dict1['buy/sell']='sell'
            order_dict1['date']=test_data['date']
            order_dict1['entry']=test_data['close']
            sell_price=test_data['close']
            order_dict1['net_change']=(test_data['close']-sell_price2)/sell_price2*100

            
            y=10
            x=0
            m=0
            high1=0
            low1=80000
            tra1=0
        

        if y==10 and str(test_data['date'])[11:19]!=time_entr and test_data['high']>high1:
            high1=test_data['high']
        if y==10 and str(test_data['date'])[11:19]!=time_entr and test_data['low']<low1:
            low1=test_data['low']
        
        #trailing
        if y==11 and test_data['low']<(sell_price-sl*1) and str(test_data['date'])[11:19]!=time_entr and tra1==0:
            sl=0
            tra1=10

        if y==11 and test_data['high']>(sell_price+sl) and str(test_data['date'])[11:19]!=time_entr and m==0:
           exit_p=sell_price+sl
           exit_t=test_data['date']
           pnlper=-(sl/test_data['close'])*100
           m=10
           
        if y==10 and str(test_data['date'])[11:19]=='15:20:00' and m==10:
            order_dict1['exit']=exit_p
            order_dict1['exit_time']=exit_t
            exit_price=exit_p
            order_dict1['percent_return']=pnlper
            order_dict1['high1']=high1
            order_dict1['low1']=low1
            all_trade1.append(copy.deepcopy(order_dict1))
            y=0
            x=10

        if str(test_data['date'])[11:19]=='15:20:00' and y==10 and x==0:
            order_dict1['exit']=test_data['close']
            order_dict1['exit_time']=test_data['date']
            exit_price=sell_price-test_data['close']
            order_dict1['percent_return']=(exit_price/test_data['close'])*100
            order_dict1['high1']=high1
            order_dict1['low1']=low1
            all_trade1.append(copy.deepcopy(order_dict1))
            y=0
        


k=pd.DataFrame(all_trade1)
k.to_csv('all  sell market two pm backtest.csv')