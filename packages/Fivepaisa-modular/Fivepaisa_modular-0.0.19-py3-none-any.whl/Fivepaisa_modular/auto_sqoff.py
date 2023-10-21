from py5paisa.order import Order, OrderType, Exchange
import pandas as pd
import time as tym
from datetime import datetime, date, time
import pytz # for timezone

def sqoff_place(client, iDict, rec, attempts):
    
    same_day_sqoff=iDict['same_day_sqoff']
    squareoff_time=iDict['squareoff_time']

    ############## SAME DAY SL and AUTOSQUAREOFF CODE###########
    if same_day_sqoff=="E":
        if squareoff_time<datetime.now(pytz.timezone('Asia/Kolkata')).time():
            print("Autosquareoff started at=",datetime.now(pytz.timezone('Asia/Kolkata')).time())
            i=attempts
            while i>0:
                client.squareoff_all()
                tym.sleep(2)
                client.squareoff_all()
                i=i-1
            print("square off all completed")
    
            df_order=pd.json_normalize(client.order_book())
            df_order=df_order[(df_order.OrderStatus == "Pending")]
            df_order.reset_index(inplace=True)
            if df_order.empty==1:
                print("No pending orders exist for cancellation")
                return rec

            i=attempts
            while i>0:
                for j in range(len(df_order.index)):
                    client.cancel_order(exch_order_id=df_order.loc[j,'ExchOrderID'])
                df_order=pd.json_normalize(client.order_book())
                df_order=df_order[(df_order.OrderStatus == "Pending")]
                df_order.reset_index(inplace=True)
                if df_order.empty==1:
                    print("All pending orders cancelled")
                    return rec
                i=i-1
            print("Issue with Order cancellation")
        else:
            print("Auto square off time not reached")
    else:
        print("auto_squareoff disabled")

    return rec

