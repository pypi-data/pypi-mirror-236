import websockets
from websocket import WebSocket
import requests
import pandas as pd
import numpy as np
from datetime import datetime, date, time
import time as tym
import pytz # for timezone
from IPython.display import clear_output
import json
from snapi_py_client.snapi_bridge import StocknoteAPIPythonBridge

def auto_sq(samco, token, rec, attempts):

    i=attempts

    while i>0:
        df_pos=samco.get_positions_data(position_type=samco.POSITION_TYPE_NET)
        df_pos=json.loads(df_pos)
        if df_pos['statusMessage']!="No Positions found !":
            i=3
            print("No Positions found ! ")
            break
        df_pos=pd.json_normalize(data=df_pos['positionDetails'])
        df_pos['calculatedNetQuantity']=df_pos['calculatedNetQuantity'].astype(float)

        if (len(df_pos[(df_pos.calculatedNetQuantity<0)])==0)&(len(df_pos[(df_pos.calculatedNetQuantity>0)])==0):
            if i==attempts:
                print("No Sell positions, No Buy positions")
                break
            else:
                break

    ############Sell side square off####################        
        if len(df_pos[(df_pos.calculatedNetQuantity<0)])>0:
            df_pos1=df_pos[(df_pos.calculatedNetQuantity<0)]
            df_pos1.reset_index(inplace=True)
            if 'level_0' in df_pos1.columns:
                df_pos1 = df_pos1.drop(columns=['level_0'])

            for j in range(len(df_pos1.index)):
                print("Autosquare OFF: ",df_pos1.loc[j,'tradingSymbol'])
                requestBody={
                "symbolName": df_pos1.loc[j,'tradingSymbol'],
                "exchange": "NFO",
                "transactionType": "BUY",
                "orderType": samco.ORDER_TYPE_MARKET,
                "quantity": df_pos1.loc[j,'netQuantity'],
                "disclosedQuantity": df_pos1.loc[j,'netQuantity'],
                "price": "0",
                "priceType": "LTP",
                "marketProtection": "0",
                "orderValidity": "DAY",
                "afterMarketOrderFlag": "NO",
                "productType": samco.PRODUCT_NRML,
                "triggerPrice": "0.00"
                }
                headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'x-session-token': token
                }
                r = requests.post('https://api.stocknote.com/order/placeOrder'
                , data=json.dumps(requestBody)
                , headers = headers)

                if r.status_code!=400:
                    rec1=pd.json_normalize(r.json())
                    rec=pd.concat([rec,rec1])
                    tym.sleep(Delay_buy)
                else:
                    print("BAD RESPONSE 400")

                if r!=None:
                    rec1=pd.json_normalize(r)
                    rec=pd.concat([rec,rec1])
                else:
                    print("NONE response")
                tym.sleep(1)

            print("sell side auto squareoff completed")
        else:
            print("No sell sides found for autosquareoff")
            tym.sleep(1)
        ################buy side square off loop#############

        if len(df_pos[(df_pos.calculatedNetQuantity>0)])>0:
            df_pos1=df_pos[(df_pos.calculatedNetQuantity<0)]
            df_pos1.reset_index(inplace=True)
            if 'level_0' in df_pos1.columns:
                df_pos1 = df_pos1.drop(columns=['level_0'])

            for j in range(len(df_pos1.index)):
                print("Autosquare OFF: ",df_pos1.loc[j,'tradingSymbol'])
                requestBody={
                "symbolName": df_pos1.loc[j,'tradingSymbol'],
                "exchange": "NFO",
                "transactionType": "BUY",
                "orderType": samco.ORDER_TYPE_MARKET,
                "quantity": df_pos1.loc[j,'netQuantity'],
                "disclosedQuantity": df_pos1.loc[j,'netQuantity'],
                "price": "0",
                "priceType": "LTP",
                "marketProtection": "0",
                "orderValidity": "DAY",
                "afterMarketOrderFlag": "NO",
                "productType": samco.PRODUCT_NRML,
                "triggerPrice": "0.00"
                }
                headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'x-session-token': token
                }
                r = requests.post('https://api.stocknote.com/order/placeOrder'
                , data=json.dumps(requestBody)
                , headers = headers)

                if r.status_code!=400:
                    rec1=pd.json_normalize(r.json())
                    rec=pd.concat([rec,rec1])
                    tym.sleep(Delay_buy)
                else:
                    print("BAD RESPONSE 400")

                if r!=None:
                    rec1=pd.json_normalize(r)
                    rec=pd.concat([rec,rec1])
                else:
                    print("NONE response")
                tym.sleep(1)

            print("buy side auto squareoff completed")
        else:
            print("no buy side found for autosquareoff")
        i=i-1

        
    ##############Order Cancellation#######################
    i=attempts
    while i>0:
        df_order=samco.get_order_book()
        df_order=json.loads(df_order)
        if df_order['status']!='Failure':
            df_order=pd.json_normalize(data=df_order['orderBookDetails'])
        #     df_order=pd.read_pickle("df_orders_samco2.pkl")
            df_order=df_order[(df_order.orderStatus == "Trigger Pending")]
            df_order.reset_index(inplace=True)

            if len(df_order.index)==0:
                if i==attempts:
                    print("No pending orders for cancellation")
                    i=3
                    break
                else:
                    print("All pending orders cancelled")
                    i=3
                    break
            for j in range(len(df_order.index)):
                samco.cancel_order(order_number=df_order.loc[j,'orderNumber'])
                print("Cancelled SL for: ",df_order.loc[j,'tradingSymbol'])
                tym.sleep(1)
        else:
            print("Order fetch failure")
        i=i-1
    return rec
