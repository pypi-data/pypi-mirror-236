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

def sl_place(samco, token, iDict, oDict, rec):
    
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
    lpp_factor=iDict['lpp_factor']
    token=token
    samco=samco

    ############ Placing Stoploss Order ######################
    df_pos=samco.get_positions_data(position_type=samco.POSITION_TYPE_NET)
    df_pos=json.loads(df_pos)
    if df_pos['statusMessage']== 'No Positions found ! ':
        print("NO POSITIONS FOR SL")
    else:
        print("SL PLACEMENT INITIATED")
        df_pos=pd.json_normalize(data=df_pos['positionDetails'])
        for i in range(len(df_pos.index)):
            if float(df_pos['calculatedNetQuantity'][i])<0:
                print("SL order placed")
                requestBody={
                "symbolName": df_pos['tradingSymbol'][i],
                "exchange": "NFO",
                "transactionType": "BUY",
                "orderType": samco.ORDER_TYPE_SL,
                "quantity": int(abs(float(df_pos['calculatedNetQuantity'][i]))),
                "disclosedQuantity": int(abs(float(df_pos['calculatedNetQuantity'][i]))),
                "price": str(int(abs(float(df_pos['averagePrice'][i])*Stop_loss*1.1))),
                "priceType": "LTP",
                "marketProtection": "0",
                "orderValidity": "DAY",
                "afterMarketOrderFlag": "NO",
                "productType": samco.PRODUCT_NRML,
                "triggerPrice": str(int(abs(float(df_pos['averagePrice'][i])*Stop_loss)))
                }
                headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'x-session-token': token
                }
                r = requests.post('https://api.stocknote.com/order/placeOrder'
                , data=json.dumps(requestBody)
                , headers = headers)

                rec1=pd.json_normalize(r.json())
                rec=pd.concat([rec,rec1])
                tym.sleep(Delay_buy)
    return rec