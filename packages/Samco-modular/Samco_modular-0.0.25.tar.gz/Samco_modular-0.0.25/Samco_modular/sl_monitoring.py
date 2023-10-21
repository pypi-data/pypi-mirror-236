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

def sl_monitor(samco, token, iDict, rec):
    df_pos=samco.get_positions_data(position_type=samco.POSITION_TYPE_NET)
    df_pos=json.loads(df_pos)
    if df_pos['statusMessage']!="No Positions found ! ":
        expiry=iDict['expiry']
        underlying_print=iDict['underlying_print']
        entry_time=iDict['entry_time']
        num_strikes=iDict['num_strikes']
        Buy_prm_closest=iDict['Buy_prm_closest']
        Delay_buy=iDict['Delay_buy']
        Sell_prm_closest=iDict['Sell_prm_closest']
        Stop_loss=iDict['Stop_loss']
        buy_sell_order=iDict['buy_sell_order']
        same_day_sqoff=iDict['same_day_sqoff']
        squareoff_time=iDict['squareoff_time'] 
        underlying_samco_index=iDict['underlying_samco_index']
        strike_step=iDict['strike_step']
        qty=iDict['qty'] 
        lots=iDict['lots']
        buy_sell_print=iDict['buy_sell_print']

        rec=rec

        today=datetime.now(pytz.timezone('Asia/Kolkata')).date()
        temp_dataframe=pd.DataFrame()
        clear_dataframe=pd.DataFrame()

        df_order=samco.get_order_book()
        df_order=json.loads(df_order)
        if df_order['status']!='Failure':
            df_order=pd.json_normalize(data=df_order['orderBookDetails'])
        #     df_order=pd.read_pickle("df_orders_samco2.pkl")
            df_order=df_order[(df_order.orderStatus == "Trigger Pending")]
            df_order=df_order[['orderNumber','orderStatus','triggerPrice','tradingSymbol','displayStrikePrice','optionType','pendingQuantity']]
            df_order.reset_index(inplace=True)
        # df_order

        df_pos=samco.get_positions_data(position_type=samco.POSITION_TYPE_NET)
        df_pos=json.loads(df_pos)
        df_pos=pd.json_normalize(data=df_pos['positionDetails'])
        #     df_pos=pd.read_pickle("df_pos_samco1.pkl")
        df_pos['calculatedNetQuantity']=df_pos['calculatedNetQuantity'].astype(float)
        df_pos=df_pos[(df_pos.calculatedNetQuantity<0)]
        df_pos.reset_index(inplace=True)
        # df_pos

        prices_dataframe1=pd.DataFrame(index=range(len(df_pos.index)))
        prices_dataframe1['Close']='NaN'
        prices_dataframe1['tradingSymbol']='NaN'
        prices_dataframe1['strikePrice']='NaN'
        prices_dataframe1['optionType']='NaN'
        prices_dataframe1['orderNumber']='NaN'
        prices_dataframe1['SLTriggerRate']='NaN'
        prices_dataframe1['Qty']='NaN'
        prices_dataframe1['Sell_Price']='NaN'


        for i in range(len(df_pos.index)):
            prices_dataframe1.loc[i,'tradingSymbol']=df_pos.iloc[i]['tradingSymbol']
            prices_dataframe1.loc[i,'strikePrice']=df_pos.iloc[i]['strikePrice']
            prices_dataframe1.loc[i,'optionType']=df_pos.iloc[i]['optionType']
            prices_dataframe1.loc[i,'Qty']=df_pos.iloc[i]['netQuantity']
            prices_dataframe1.loc[i,'Sell_Price']=df_pos.iloc[i]['averageSellPrice']

            prices_dataframe1['Close']=df_pos['lastTradedPrice']

        for i in range(len(prices_dataframe1.index)):
            for j in range(len(df_order.index)):
                if df_order.loc[j,'tradingSymbol']==prices_dataframe1.loc[i,'tradingSymbol']:
                    prices_dataframe1.loc[i,'orderNumber']=df_order.loc[j,'orderNumber']
                    prices_dataframe1.loc[i,'SLTriggerRate']=df_order.loc[j,'triggerPrice']

        tym.sleep(10)
        ##############Position collection for second time####################
        df_pos=samco.get_positions_data(position_type=samco.POSITION_TYPE_NET)
        df_pos=json.loads(df_pos)
        df_pos=pd.json_normalize(data=df_pos['positionDetails'])
        #     df_pos=pd.read_pickle("df_pos_samco1.pkl")
        df_pos['calculatedNetQuantity']=df_pos['calculatedNetQuantity'].astype(float)
        df_pos=df_pos[(df_pos.calculatedNetQuantity<0)]
        df_pos.reset_index(inplace=True)
        # df_pos

        prices_dataframe2=pd.DataFrame(index=range(len(df_pos.index)))
        prices_dataframe2['Close']='NaN'
        prices_dataframe2['tradingSymbol']='NaN'
        prices_dataframe2['strikePrice']='NaN'
        prices_dataframe2['optionType']='NaN'
        prices_dataframe2['orderNumber']='NaN'
        prices_dataframe2['SLTriggerRate']='NaN'
        prices_dataframe2['Qty']='NaN'
        prices_dataframe2['Sell_Price']='NaN'


        for i in range(len(df_pos.index)):
            prices_dataframe2.loc[i,'tradingSymbol']=df_pos.iloc[i]['tradingSymbol']
            prices_dataframe2.loc[i,'strikePrice']=df_pos.iloc[i]['strikePrice']
            prices_dataframe2.loc[i,'optionType']=df_pos.iloc[i]['optionType']
            prices_dataframe2.loc[i,'Qty']=df_pos.iloc[i]['netQuantity']
            prices_dataframe2.loc[i,'Sell_Price']=df_pos.iloc[i]['averageSellPrice']

            prices_dataframe2['Close']=df_pos['lastTradedPrice']

        for i in range(len(prices_dataframe2.index)):
            for j in range(len(df_order.index)):
                if df_order.loc[j,'tradingSymbol']==prices_dataframe2.loc[i,'tradingSymbol']:
                    prices_dataframe2.loc[i,'orderNumber']=df_order.loc[j,'orderNumber']
                    prices_dataframe2.loc[i,'SLTriggerRate']=df_order.loc[j,'triggerPrice']

        ##################Comparison of dataframes for SL fail###############
        # prices_dataframe1.loc[1,'Close']=1000 for testing
        # prices_dataframe2.loc[1,'Close']=1000 for testing
        if(len(prices_dataframe2.index))==0:
            print("NO sell positions for SL monitoring at: ",datetime.now(pytz.timezone('Asia/Kolkata')))

        for i in range(len(prices_dataframe1.index)):
            for j in range(len(prices_dataframe2.index)):
                if prices_dataframe2.loc[j,'tradingSymbol']==prices_dataframe1.loc[i,'tradingSymbol']:
                    if (float(prices_dataframe2.loc[j,'Close'])>Stop_loss*float(prices_dataframe2.loc[j,'Sell_Price']))&(float(prices_dataframe1.loc[i,'Close'])>Stop_loss*float(prices_dataframe1.loc[i,'Sell_Price'])):
                    # if (float(prices_dataframe2.loc[j,'Close'])>-1)&(float(prices_dataframe1.loc[i,'Close'])>-1):
                        print("At time:",datetime.now(pytz.timezone('Asia/Kolkata')),", Price at ",prices_dataframe2.loc[j,'Close'],", beyond SL for: ",prices_dataframe2.loc[j,'tradingSymbol'])
                        if prices_dataframe1.loc[i,'orderNumber']!='NaN':
                            samco.cancel_order(order_number=prices_dataframe1.loc[i,'orderNumber'])
                            print("Existing SL order cancelled, carrying one more SELL QTY check")
                            ##############rechecking quantities################
                            tym.sleep(2)
                            df_pos1=samco.get_positions_data(position_type=samco.POSITION_TYPE_NET)
                            df_pos1=json.loads(df_pos1)
                            df_pos1=pd.json_normalize(data=df_pos1['positionDetails'])
                            #     df_pos=pd.read_pickle("df_pos_samco1.pkl")
                            df_pos1['calculatedNetQuantity']=df_pos1['calculatedNetQuantity'].astype(float)
                            df_pos1=df_pos1[(df_pos1.calculatedNetQuantity<0)]
                            df_pos1.reset_index(inplace=True)
                            df_pos1=df_pos1[(df_pos1.tradingSymbol==prices_dataframe2.loc[j,'tradingSymbol'])]
                            
                            print("Squaring OFF")
                            requestBody={
                            "symbolName": prices_dataframe2.loc[j,'tradingSymbol'],
                            "exchange": "NFO",
                            "transactionType": "BUY",
                            "orderType": samco.ORDER_TYPE_MARKET,
                            "quantity": df_pos1.loc[0,'netQuantity'],
                            "disclosedQuantity": df_pos1.loc[0,'netQuantity'],
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
        
                        else:
                            print("No existing SL detected")
                            print("Squaring OFF")
                            requestBody={
                            "symbolName": prices_dataframe2.loc[j,'tradingSymbol'],
                            "exchange": "NFO",
                            "transactionType": "BUY",
                            "orderType": samco.ORDER_TYPE_MARKET,
                            "quantity": prices_dataframe1.loc[i,'Qty'],
                            "disclosedQuantity": prices_dataframe1.loc[i,'Qty'],
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
                    else:
                        print("At time:",datetime.now(pytz.timezone('Asia/Kolkata')),", SL monitoring OK for: ",prices_dataframe2.loc[j,'tradingSymbol'])

    else:
        print("No positions for sl monitoring")        
        
    return rec