import pandas as pd
import numpy as np
from datetime import datetime, date, time
import time as tym
import pytz # for timezone
from py5paisa.order import Order, OrderType, Exchange
from IPython.display import clear_output

def buy_sqoff(client, iDict, rec):
    
    df_pos=pd.json_normalize(client.positions())

    if df_pos.empty!=1:
        df_pos['ScripName']=df_pos['ScripName'].astype(str)
        df_pos['CEPE']=df_pos['ScripName'].str[-11:]
        df_pos['CEPE']=df_pos['CEPE'].str[0:2]
        sell_pos=df_pos[(df_pos.NetQty<0)]
        sell_pos.reset_index(inplace=True)
        df_pos.reset_index(inplace=True)

    sell_pe_buy="DO NOT SELL PE BUY"
    sell_ce_buy="DO NOT SELL CE BUY"

    try:
        sell_pe_buy="SELL PE BUY"
        sell_ce_buy="SELL CE BUY"
        for i in range(len(sell_pos.index)):
            if sell_pos.loc[i,'CEPE']=="PE":
                sell_pe_buy="DO NOT SELL PE BUY"
            if sell_pos.loc[i,'CEPE']=="CE":
                sell_ce_buy="DO NOT SELL CE BUY"
    except:
        tym.sleep(1)
        
    if sell_pe_buy!="DO NOT SELL PE BUY":
        df_pos=df_pos[(df_pos.NetQty>0)&(df_pos.CEPE=="PE")]
        df_pos.reset_index(inplace=True)
        for i in range(len(df_pos.index)):
            print("Squaring OFF PE BUY SIDE: ",df_pos.loc[i,'ScripName'])
            r=client.place_order(OrderType='S',Exchange='N',ExchangeType='D',
                ScripCode = int(abs(df_pos.loc[i,'ScripCode'])),
                Qty=int(abs(df_pos.loc[i,'NetQty'])), DisQty=int(abs(df_pos.loc[i,'NetQty'])), IsIntraday= False, IsStopLossOrder= False,
                    StopLossPrice=0, Price= 0, AHPlaced='N') ## To place PE Sell
            
    if sell_ce_buy!="DO NOT SELL CE BUY":
        df_pos=df_pos[(df_pos.NetQty>0)&(df_pos.CEPE=="CE")]
        df_pos.reset_index(inplace=True)
        for i in range(len(df_pos.index)):
            print("Squaring OFF CE BUY SIDE: ",df_pos.loc[i,'ScripName'])
            r=client.place_order(OrderType='S',Exchange='N',ExchangeType='D',
                ScripCode = int(abs(df_pos.loc[i,'ScripCode'])),
                Qty=int(abs(df_pos.loc[i,'NetQty'])), DisQty=int(abs(df_pos.loc[i,'NetQty'])), IsIntraday= False, IsStopLossOrder= False,
                    StopLossPrice=0, Price= 0, AHPlaced='N') ## To place PE Sell
    print("buyside monitoring ok")
    return rec