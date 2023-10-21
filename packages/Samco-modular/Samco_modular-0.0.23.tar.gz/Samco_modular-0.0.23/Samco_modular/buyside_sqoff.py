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


def buy_sqoff(samco, token, iDict, rec):
        
    df_pos=samco.get_positions_data(position_type=samco.POSITION_TYPE_NET)
    df_pos=json.loads(df_pos)
    if df_pos['status']!='Failure':
        df_pos=pd.json_normalize(data=df_pos['positionDetails'])
        df_pos['calculatedNetQuantity']=df_pos['calculatedNetQuantity'].astype(float)
        sell_pos=df_pos[(df_pos.calculatedNetQuantity<0)]
        df_pos.reset_index(inplace=True)
        sell_pos.reset_index(inplace=True)
        
    sell_pe_buy="DO NOT SELL PE BUY"
    sell_ce_buy="DO NOT SELL CE BUY"

    try:
        sell_pe_buy="SELL PE BUY"
        sell_ce_buy="SELL CE BUY"
        for i in range(len(sell_pos.index)):
            if sell_pos.loc[i,'optionType']=="PE":
                sell_pe_buy="DO NOT SELL PE BUY"
            if sell_pos.loc[i,'optionType']=="CE":
                sell_ce_buy="DO NOT SELL CE BUY"
    except:
        tym.sleep(1)

    if sell_pe_buy!="DO NOT SELL PE BUY":
        df_pos=df_pos[(df_pos.calculatedNetQuantity>0)&(df_pos.optionType=="PE")]
        df_pos.reset_index(inplace=True)
        for i in range(len(df_pos.index)):
            print("Squaring OFF PE BUY SIDE: ",df_pos.loc[i,'tradingSymbol'])
            requestBody={
            "symbolName": df_pos.loc[i,'tradingSymbol'],
            "exchange": "NFO",
            "transactionType": "SELL",
            "orderType": samco.ORDER_TYPE_MARKET,
            "quantity": df_pos.loc[i,'netQuantity'],
            "disclosedQuantity": df_pos.loc[i,'netQuantity'],
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
                
    if sell_ce_buy!="DO NOT SELL CE BUY":
        df_pos=df_pos[(df_pos.calculatedNetQuantity>0)&(df_pos.optionType=="CE")]
        for i in range(len(df_pos.index)):
            print("Squaring OFF CE BUY SIDE")
            requestBody={
            "symbolName": df_pos.loc[i,'tradingSymbol'],
            "exchange": "NFO",
            "transactionType": "SELL",
            "orderType": samco.ORDER_TYPE_MARKET,
            "quantity": df_pos.loc[i,'netQuantity'],
            "disclosedQuantity": df_pos.loc[i,'netQuantity'],
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
    print("buyside monitoring ok")
    return rec

