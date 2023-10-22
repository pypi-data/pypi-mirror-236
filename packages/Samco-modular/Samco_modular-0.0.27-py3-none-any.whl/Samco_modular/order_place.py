import websockets
from websocket import WebSocket
import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime, date, time
import time as tym
import pytz # for timezone
from IPython.display import clear_output
from snapi_py_client.snapi_bridge import StocknoteAPIPythonBridge

def order_place(samco, token, iDict, oDict):
    
    CE_Scripcode_SELL=oDict['CE_Scripcode_SELL']
    CE_Scripcode_BUY=oDict['CE_Scripcode_BUY']
    PE_Scripcode_SELL=oDict['PE_Scripcode_SELL']
    PE_Scripcode_BUY=oDict['PE_Scripcode_BUY']

    qty=iDict['qty']
    buy_sell_order=iDict['buy_sell_order']
    same_day_sqoff=iDict['same_day_sqoff']
    Delay_buy=iDict['Delay_buy']
    Stop_loss=iDict['Stop_loss']
    squareoff_time=iDict['squareoff_time']
    token=token
    samco=samco

    ############################## ORDER PLACEMENT BUY/SELL AND STOPLOSS#############################
    rec=pd.DataFrame()

    if buy_sell_order=="BS":
    ########################### BUY CE ######################
        print("CE BUY order placed")
        requestBody={
        "symbolName": CE_Scripcode_BUY,
        "exchange": "NFO",
        "transactionType": "BUY",
        "orderType": samco.ORDER_TYPE_MARKET,
        "quantity": qty,
        "disclosedQuantity": qty,
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

    ########################### BUY PE ######################
        print("PE BUY order placed")
        requestBody={
        "symbolName": PE_Scripcode_BUY,
        "exchange": "NFO",
        "transactionType": "BUY",
        "orderType": samco.ORDER_TYPE_MARKET,
        "quantity": qty,
        "disclosedQuantity": qty,
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
            print("BAD RESPONSE 400 /n")


    if buy_sell_order=="SO":
        print("SELL ONLY")
    ######################### SELL CE ######################
    print("CE SELL order placed")

    requestBody={
    "symbolName": CE_Scripcode_SELL,
    "exchange": "NFO",
    "transactionType": "SELL",
    "orderType": samco.ORDER_TYPE_MARKET,
    "quantity": qty,
    "disclosedQuantity": qty,
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
        print("BAD RESPONSE 400 /n")

    ######################### SELL PE #########################
    print("PE SELL order placed")

    requestBody={
    "symbolName": PE_Scripcode_SELL,
    "exchange": "NFO",
    "transactionType": "SELL",
    "orderType": samco.ORDER_TYPE_MARKET,
    "quantity": qty,
    "disclosedQuantity": qty,
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
        print("BAD RESPONSE 400 /n")
