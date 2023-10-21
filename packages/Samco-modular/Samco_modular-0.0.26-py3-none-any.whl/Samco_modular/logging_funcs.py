import logging
from datetime import datetime, date, time
import os

def save_to_text(message,folder,function_type):
    if function_type=="df":
        outdir = folder
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        f = open(folder+'\log.txt', 'w')
        f.write(message)
        f.close()

def df_strike_logging(oDict, iDict, logging_en):
    
    if logging_en=="E":
        outdir = 'logging'
        if not os.path.exists(outdir):
            os.mkdir(outdir)

        logging.basicConfig(level=logging.INFO, filename='file.log', filemode='w', 
                    format='%(message)s') 
        logging.disable(0)
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

        CE_Scripcode_SELL=oDict['CE_Scripcode_SELL']
        CE_Scripcode_BUY=oDict['CE_Scripcode_BUY']
        PE_Scripcode_SELL=oDict['PE_Scripcode_SELL']
        PE_Scripcode_BUY=oDict['PE_Scripcode_BUY']


        logging.info("Script= "+str(underlying_print))
        logging.info("Expiry date= "+str(expiry))
        logging.info("No of lots= "+ str(lots))
        logging.info("SELL BUY TYPE= "+ str(buy_sell_print[buy_sell_order]))
        logging.info("Same day SQOFF= "+ str(same_day_sqoff))
        logging.info("Code completion time="+str(datetime.now(pytz.timezone('Asia/Kolkata')).time()))
        logging.info("Code Execution time="+str(code_completion-start))
        logging.info("Strike SELL CE="+str(int(df_strikeprice.loc[CE_indx_SELL,'Strike_Selection']))+
            "  Price="+str(df_strikeprice.loc[CE_indx_SELL,'CE_LTP'])+
            "   Scripcode="+str(CE_Scripcode_SELL))
        logging.info("Strike SELL PE="+str(int(df_strikeprice.loc[PE_indx_SELL,'Strike_Selection']))+
        "  Price="+str(df_strikeprice.loc[PE_indx_SELL,'PE_LTP'])+
        "   Scripcode="+str(PE_Scripcode_SELL))
        logging.info("Strike BUY CE="+str(int(df_strikeprice.loc[CE_indx_BUY,'Strike_Selection']))+
        "  Price="+str(df_strikeprice.loc[CE_indx_BUY,'CE_LTP'])+
        "   Scripcode="+str(CE_Scripcode_BUY))
        logging.info("Strike BUY PE="+str(int(df_strikeprice.loc[PE_indx_BUY,'Strike_Selection']))+
            "  Price="+str(df_strikeprice.loc[PE_indx_BUY,'PE_LTP'])+
            "   Scripcode="+str(PE_Scripcode_BUY))
    else:
        logging.disable()


    return

def sl_mon_logging(logging_en):



    if logging_en=="E":
        outdir = 'logging'
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        logging.basicConfig(level=logging.INFO, filename='file.log', filemode='w', 
                    format='%(message)s') 
        logging.disable(0)
        logging.info("At time="+str(datetime.now(pytz.timezone('Asia/Kolkata')).time()))
        logging.info("SL monitoring & buyside monitoring running ok")
    else:
        logging.disable()



