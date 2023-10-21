import MetaTrader5 as mt5
import json


from database_ex_forex_next3 import Database

class REP_POS:
   
   
   def __init__(self):
       fileObject = open("login.json", "r")
       jsonContent = fileObject.read()
       aList = json.loads(jsonContent)
       
       self.login = int (aList['login'])
       self.Server = aList['Server'] 
       self.Password = aList['Password'] 
       self.symbol_EURUSD = aList['symbol_EURUSD'] 
       self.decimal_sambol = int (aList['decimal_sambol'] )
       self.repetition_index = int (aList['repetition_index'] )

   def repetition_pos(status_rep):
     
   #   print("status_rep:" , status_rep)
        
     if status_rep == "true":   

        data_all = Database.select_table_All()
        select_all_len = len(data_all)
        print("select_all_len:" , select_all_len)

        if select_all_len > 0:
             
             positions = mt5.positions_get(symbol = REP_POS().symbol_EURUSD)
            #  print(positions)  
        
             if positions == None:
                 print("No positions on EURUSD, error code={}".format(mt5.last_error()))
             elif len(positions)>0:
                 print("Total positions on EURUSD =", len(positions))
                # display all open positions
              
             len_positions = len(positions)
            #  print ("len_positions:" , len_positions)
            #  print("")
        
             list_ticket_POS = []
        
             for position in positions:
                 
                 list_ticket_POS.append(position[0])
                 
             list_ticket_DB = []
             list_rep_patern = []

             for i in range(select_all_len):
                                  
                     data_one_DB = data_all[i]
                     repetition_candel = data_one_DB[24]
                     if repetition_candel:
                        list_rep_patern.append(repetition_candel)


             from collections import Counter
             print("list_rep_patern:" , list_rep_patern)
             freq_dict = Counter(list_rep_patern)
             sorted_freq = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
 
             # Print the sorted frequency
             print(sorted_freq)

             list_rep_sorted = []
             for index_rep in sorted_freq:
                  print("index_rep:" , index_rep)
                  if index_rep[1] > REP_POS().repetition_index:
                       list_rep_sorted.append(index_rep[0])
                       
             print("list_rep_sorted:" , list_rep_sorted)
             for index , index_patern in enumerate(data_all): 
                                  
                #    print("index_patern:" , index_patern)
                   candel_num = index_patern[1]
                   status = index_patern[15]
                   chek = index_patern[16]
                   ticket = index_patern[21]
                   repetition_pos = index_patern[23]
                   repetion_candel_num = index_patern[24]
                   Trust_patern_full = index_patern[26]
                   Layout_patern = index_patern [27]

                   chek_ticket = None
                   
                   if ticket:
                       ticket = int(ticket)
                     #   list_ticket_DB.append(ticket)
        
                #    print("candel_num:" , candel_num)
                #    print("chek:" , chek)
                #    print("status:" , status)
                  #  print("ticket:" , ticket)
                #    print("repetition_pos:" , repetition_pos)
                  #  print("list_ticket_POS:" , list_ticket_POS)



                   for ticket_pos in list_ticket_POS:
                       #    print("ticket_pos:" , ticket_pos)
   
                          ticket_pos = int (ticket_pos)
                          ticket = int (ticket)
                          
                          if ticket == ticket_pos:
                               chek_ticket = True

                   if chek_ticket == True:
                        chek_ticket = True
                   else:
                        chek_ticket = False   

                  #  print("chek:" , chek)
                  #  print("status:" , status)
                  #  print("ticket:" , ticket)
                  #  print("repetition_pos:" , repetition_pos)
                  #  print("Trust_patern:" , Trust_patern)
                  #  print("Layout_patern:" , Layout_patern)    
                  #  print("chek_ticket:" , chek_ticket)   

                   chek_rep = False
                   print("repetion_candel_num:" , repetion_candel_num) 
                   for index_search_rep in list_rep_sorted:
                        if repetion_candel_num == index_search_rep:
                           #   print("11111111111111333333333333")
                             chek_rep = True

                  #  print("chek_rep:" , chek_rep)          
                    

                   if chek_ticket == False  and chek == "true" and status =="true" and repetition_pos == "false" and ticket != 0 and Trust_patern_full == "true" and Layout_patern == "true" and chek_rep == False:

                           candel_num_rep = index_patern[1]
                           type = index_patern[2]
                           point_patern = index_patern[3]
                           point_5 = index_patern[4]
                           point_5_time = index_patern[5]
                           command = index_patern[6]
                           candel_color = index_patern[7]
                           price_candel_open = index_patern[8]
                           price_candel_close = index_patern[9]
                           gap_point = index_patern[10]
                           gap_amount = index_patern[11]
                           gap_pip = index_patern[12]
                           gap_word = index_patern[13]
                           tension = index_patern[14]
                           status = index_patern[15]
                           chek = index_patern[16]
                           time_start_search = index_patern[17]
                           time_end_patern = index_patern[18]
                           timepstamp = index_patern[19] 
                           times = index_patern[20]
                           ticket = index_patern[21]
                           line_POS = index_patern[22]
                           repetition_pos = index_patern[23]
                           rep_candel_num = index_patern[24]
                           Trust_patern = index_patern[25]
                           Trust_patern_full = index_patern[26]
                           Layout_patern = index_patern [27]
                           Jump_patern = index_patern [28]
                           news = index_patern [29]
                           jump_1mine = index_patern [30]
                           
                        #    print("status:" , status)
                        #    print("chek:" , chek)
                        #    print("repetition_pos:" , repetition_pos)

                           rep_candel_num_algo = 0

                           if rep_candel_num:
                               rep_candel_num_algo = rep_candel_num
                            #    print("111111111111111")
        
                           else:
                               rep_candel_num_algo =  candel_num_rep 
                            #    print("222222222222222")

                           print("ticket:" , ticket)
                          
                        #    print("11111111111111111111111111111111111111111111111111111")  

                           data_all = Database.select_table_All()
                           select_all_len = len(data_all)
                        #    print("select_all_len:" , select_all_len)
                           rec = data_all[select_all_len - 1]
                        #    print("select_all:" , rec)
                           candel_num = int (rec[1])
                        #    print("rec:" , rec)
                           candel_num = candel_num + 1
                        #    print("candel_num:" , candel_num)
                           value = (candel_num , type , point_patern , "" , "" , ""  , candel_color , price_candel_open , price_candel_close , gap_point , gap_amount , gap_pip ,gap_word , tension, status , "false" , time_start_search , time_end_patern , timepstamp , times , 0 , line_POS , "false" , rep_candel_num_algo , Trust_patern , Trust_patern_full , Layout_patern , Jump_patern , news , jump_1mine)
                           Database.insert_table(value)
                           Database.update_table_repetition_pos("true" , candel_num_rep ) 

                           break
 
     elif status_rep == "false":
          
          print("status_rep: False")
         
   