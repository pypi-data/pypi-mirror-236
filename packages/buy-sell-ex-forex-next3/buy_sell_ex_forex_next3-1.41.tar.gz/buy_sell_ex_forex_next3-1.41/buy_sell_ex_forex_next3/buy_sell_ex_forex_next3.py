import MetaTrader5 as mt5

import json
import time
from database_ex_forex_next3 import Database
from tick_ex_forex_next3 import Tick
from decimal import Decimal


class BUY_SELL:
    
    def __init__(self):
       fileObject = open("login.json", "r")
       jsonContent = fileObject.read()
       aList = json.loads(jsonContent)
       
       self.login = int (aList['login'])
       self.Server = aList['Server'] 
       self.Password = aList['Password'] 
       self.symbol_EURUSD = aList['symbol_EURUSD'] 
       self.decimal_sambol = int (aList['decimal_sambol'] )
    

    def decimal(num , decimal_sambol):
        telo = '0.0'
        for i in range(decimal_sambol - 2):  
          telo = telo + "0"
        telo = telo + "1" 
        telo = float (telo)
        decimal_num = Decimal(str(num))
        rounded_num = decimal_num.quantize(Decimal(f'{telo}'))
        return rounded_num  

   
    def buy(symbol, lot, price , tp , deviation, magic , comment):

        return {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            # "sl": sl,
            "tp": tp,
            "deviation": deviation,
            "comment": comment,
            "magic": magic,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK

        }

    def sell(symbol, lot, price, tp , deviation, magic, comment):

        return {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            # "sl": sl,
            "tp": tp,
            "deviation": deviation,
            "comment": comment,
            "magic": magic,
            "type_time": mt5.ORDER_TIME_GTC,  
            "type_filling": mt5.ORDER_FILLING_FOK

        }

    async def close(action, symbol, lot, position_id, comment):

        if action == 'buy':
            type = mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(symbol).ask
    
        elif action == 'sell':
            type = mt5.ORDER_TYPE_SELL
            price = mt5.symbol_info_tick(symbol).bid
    
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": type,
            "price": price,
            "position": position_id,
            "deviation": 10,
            "magic": 0,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_DAY,
            "type_filling": mt5.ORDER_FILLING_FOK
    
        }
    
        # send a trading request
        result = mt5.order_send(request)
        print(result)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Order closing failed: {}".format(result.retcode))
            return False
        else:
            print("closed correctly")
            return True
    
    async def pos_buy(tp , lot , symbol_EURUSD , command):

      # try:

             ask = Tick(symbol_EURUSD).ask
            #  x = Login(BUY_SELL().login, BUY_SELL().Server, BUY_SELL().Password)
            #  infologin = x.infologin(symbol_EURUSD) 
            #  ask = infologin[3]
             ask = BUY_SELL.decimal(ask , BUY_SELL().decimal_sambol)
             ask = float(ask)
             print("ask:" , ask)
            #  point = mt5.symbol_info(symbol_EURUSD).point
             # sl = mt5.symbol_info_tick("EURUSD").ask - 1000 * point
            #  tp = price_signal + (shakhes * point)
            #  tp = BUY_SELL.decimal(tp , BUY_SELL().decimal_sambol)
            #  tp = float(tp)
             
           #   filling_type = mt5.symbol_info(symbol_EURUSD).filling_mode
             request = BUY_SELL.buy(symbol_EURUSD , lot , ask , tp , 10 , 0  , command)
             result = mt5.order_send(request)
             # check the execution result
            #  print("result:" , result)
             execution = result.comment
             # position_ticket = result.order
     
             if execution == 'Request executed':
                 print("execution: buy true")


             return result    

          
      # except:
      #    print("error buy")
 
    async def pos_sell( tp , lot , symbol_EURUSD , command ):

      # try:
        
          #  x = Login(BUY_SELL().login, BUY_SELL().Server, BUY_SELL().Password)
          #  infologin = x.infologin(symbol_EURUSD) 
          #  bid = infologin[4]

           bid = Tick(symbol_EURUSD).bid
           bid = BUY_SELL.decimal(bid , BUY_SELL().decimal_sambol)
           bid = float(bid)
           print("bid:" , bid)
   
          #  point = mt5.symbol_info(symbol_EURUSD).point
   
           # sl = mt5.symbol_info_tick("EURUSD").ask - 100 * point

          #  tp = price_signal - (shakhes * point)
          #  tp = BUY_SELL.decimal(tp , BUY_SELL().decimal_sambol)
          #  tp = float(tp)
           
           request = BUY_SELL.sell(symbol_EURUSD, lot , bid , tp , 10 , 0, command )
           result = mt5.order_send(request)
           # check the execution result
           execution = result.comment
           # position_ticket = result.order
   
           if execution == 'Request executed':
               print("execution: sell true")

           return result      

      # except:
      #   print("error sell") 

    async def update_buy(symbol_EURUSD , lot , ticket , tp):
        req = {
          "action": mt5.TRADE_ACTION_SLTP,
          "symbol": symbol_EURUSD,
          "volume": lot,
          "type": mt5.ORDER_TYPE_BUY,
          "position":ticket,
          "tp": tp,
          "deviation": 10,
          "comment": "BUY_ASlah",
          "magic": 234000,
          "type_time": mt5.ORDER_TIME_GTC,
          "type_filling": mt5.ORDER_FILLING_FOK
        }
        result = mt5.order_send(req)
        execution = result.comment
             # position_ticket = result.order
     
        if execution == 'Request executed':
              print("execution: Update_buy true")
              return True
        else:
             return execution

    async def update_sell(symbol_EURUSD , lot , ticket , tp):
        req = {
          "action": mt5.TRADE_ACTION_SLTP,
          "symbol": symbol_EURUSD,
          "volume": lot,
          "type": mt5.ORDER_TYPE_SELL,
          "position":ticket,
          "tp": tp,
          "deviation": 10,
          "comment": "Sell_ASlah",
          "magic": 234000,
          "type_time": mt5.ORDER_TIME_GTC,
          "type_filling": mt5.ORDER_FILLING_FOK
        }
        result = mt5.order_send(req)
        execution = result.comment
             # position_ticket = result.order
     
        if execution == 'Request executed':
              print("execution: Update_sell true")
              return True

    async def pos_close(timestamp_now , input_type):
       print("timestamp_now:",timestamp_now)
       
       timestamp_next = timestamp_now + 60
       print("timestamp_next:",timestamp_next)

       positions = mt5.positions_get(symbol = BUY_SELL().symbol_EURUSD)

       if positions:
           

           for index , index_pos in enumerate(positions):    
               print("index:" , index)  
            #    print("index_pos:" , index_pos)
            
               timestamp_position = index_pos.time
               print("timestamp_position:", timestamp_position)
               
               if timestamp_position >= timestamp_now and timestamp_position < timestamp_next:
                   print("1111111111111111111111")
                   ticket_pos = index_pos.ticket
                   profit = index_pos.profit
                   type = index_pos.type
                   
                   lot = index_pos.volume
                   
                   print("ticket_pos:" , ticket_pos)
                   print("profit:" , profit)
                   # print("timestamp_position:" , timestamp_position)
                   print("type:" , type)
                   print("lot:" , lot)
                   
                   action = ''
                   index_type = ''

                   if input_type == "buy" :
                       index_type = 0
                   elif input_type == "sell":
                       index_type = 1   

                   print("index_type:" , index_type)  
                   print("type:" , type)   

                   if index_type == type:   
                   
                          if type == 1:
                              action = "buy"
                          elif type == 0:
                              action = "sell" 
          
                          print("action:" , action)      
                          async def x_run():
                              rec_pos = await BUY_SELL.close(action , BUY_SELL().symbol_EURUSD , lot , ticket_pos , "close pos")
                              print("rec_pos:" ,rec_pos )
                              return True
                          
                          for i in range(5):
                              print("i:" , i)
                              x = await x_run()   
                              if x == True:
                                  data_all_DB = Database.select_table_All()
                                  len_data_all = len(data_all_DB)
                                     #  print("len_data_all:" , len_data_all)
                                  if len_data_all > 0:
                                        for i in range(len_data_all):
                                  
                                            data_one_DB = data_all_DB[i]
                                            candel_num = data_one_DB[1]
                                            ticket = data_one_DB[21]
                                            ticket = int(ticket)
                                          #   print("ticket:" , ticket)
                                    
                                            if ticket == ticket_pos:
                                                Database.update_jamp_1mine_manage("true" , candel_num)

                                  
                                  break
                              time.sleep(1)
                   
