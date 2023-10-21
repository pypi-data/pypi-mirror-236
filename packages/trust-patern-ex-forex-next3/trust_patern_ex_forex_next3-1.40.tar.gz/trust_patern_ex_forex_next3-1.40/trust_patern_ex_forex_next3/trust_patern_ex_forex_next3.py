import MetaTrader5 as mt5
import pandas as pd
import json


from database_ex_forex_next3 import Database
from decimal import Decimal
from line_ex_forex_next3 import LINE

class Trust_Patern:
        
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

        def candelstate(listOpen , listClose):
                 candel_open = listOpen
                 candel_close = listClose
                #  candel_open = Candel.decimal(candel_open)
                #  candel_close = Candel.decimal(candel_close)
                #  print("candel_open" , candel_open) 
                #  print("candel_close" , candel_close) 
                 if candel_open > candel_close:
                     candel_state = "red"
             
                 elif candel_open < candel_close:
                     candel_state = "green"
                         
                 elif candel_open == candel_close:
                     candel_state = "doji"
             
                 return candel_state     
          
        def patern_true(candel_num ,  timestamp):
            
                timestamp_pulback = timestamp
              #   print("timestamp_pulback:" , pd.to_datetime( timestamp_pulback , unit='s'))
                utc_from = pd.to_datetime( timestamp_pulback , unit='s') 
                utc_to = pd.to_datetime( timestamp_pulback + 60 , unit='s')
                ticks = mt5.copy_ticks_range(Trust_Patern().symbol_EURUSD , utc_from, utc_to , mt5.COPY_TICKS_ALL)
              #   print("ticks:" , ticks)
                list_pullback3 = []
                for lists in ticks:
                    xx = Trust_Patern.decimal(lists[1] , Trust_Patern().decimal_sambol)
                   #  print(xx)
                    xx = float(xx)
                    list_pullback3.append(xx)
                
              #   print("list_pullback3:" , list_pullback3)
                
                cal_line_rec =  LINE.line_run(candel_num , Trust_Patern().symbol_EURUSD , timestamp_pulback )
                cal_line = cal_line_rec[0]
                # print("cal_line:" , cal_line)
        
                return cal_line
        
        def trust_patern(candel_num):
             rec = Database.select_table_One(candel_num)
             timepstamp = rec[0][19]
             timepstamp = json.loads(timepstamp)
             timestamp_point3 = int(timepstamp[2]) + 840
             # print("timestamp_point3:" , timestamp_point3)
             
             timecandel_patern = mt5.copy_rates_from(Trust_Patern().symbol_EURUSD , mt5.TIMEFRAME_M1 , timestamp_point3 , 360)
             # print("timecandel_1mine:" , timecandel_patern)
             
             status_trust_patern = False
             exit = 0

        
             for index , index_patern in enumerate(timecandel_patern): 
                   
                   timestamp_patern = index_patern[0]
             
                   close_patern = index_patern[4]
                   close_patern = Trust_Patern.decimal(close_patern ,Trust_Patern().decimal_sambol)
                   close_patern = float(close_patern)
             
                   open_patern = index_patern[1]
                   close_patern = Trust_Patern.decimal(close_patern , Trust_Patern().decimal_sambol)
                   open_patern = float(open_patern)
                   
                   # print("timestamp_patern:" , timestamp_patern)
                   # print("timestamp_patern:" , pd.to_datetime( timestamp_patern , unit='s'))
                   # print("close_patern:" , close_patern)
                   # print("open_patern:" , open_patern)
             
                   color_candel = Trust_Patern.candelstate(open_patern , close_patern)
                   # print("color_candel:" , color_candel)
             
                   rec_line = Trust_Patern.patern_true(candel_num , timestamp_patern)
             
                   if (color_candel == "green"):
                        
                        for index_line in rec_line:
                             
                             index_line = Trust_Patern.decimal(index_line , Trust_Patern().decimal_sambol)
                             index_line = float(index_line) - 0.00001 
                             
                             if index_line > open_patern and index_line < close_patern:
                                  Database.update_table_trust_patern( "true" , candel_num)
                                  print("timestamp_patern:" , pd.to_datetime( timestamp_patern , unit='s'))
                                  print("1111111111111111111111111111111111111111111")
                                  print("close_patern:" , close_patern)
                                  print("open_patern:" , open_patern)
                                  print("index_line:" , index_line)
                                  status_trust_patern = True

                                  exit = 1
                                  break
                            
                         #     else:
                         #          print("Trust_patern fault")
                         #          Database.update_table_trust_patern("false" , "false" , candel_num)

                             
                   elif (color_candel == "red"):
                        
                        for index_line in rec_line:
                             
                             index_line = Trust_Patern.decimal(index_line , Trust_Patern().decimal_sambol)
                             index_line = float(index_line) - 0.00001 
                             
                             if index_line  < open_patern and index_line > close_patern:
                                  Database.update_table_trust_patern( "true" , candel_num)
                                  print("timestamp_patern:" , pd.to_datetime( timestamp_patern , unit='s'))
                                  print("close_patern:" , close_patern)
                                  print("open_patern:" , open_patern)
                                  print("index_line:" , index_line)
                                  print("2222222222222222222222222222222222222222222")   
                                  status_trust_patern = True
                                  exit = 1
                                  break
                             
                         #     else:
                         #          print("Trust_patern fault")
                         #          Database.update_table_trust_patern("false" , "false" , candel_num)
             
                   if exit == 1:
                        break
         
             if status_trust_patern == False:
                  print("Trust_patern fault")
                  Database.update_table_trust_patern( "false" , candel_num) 

             return True
   