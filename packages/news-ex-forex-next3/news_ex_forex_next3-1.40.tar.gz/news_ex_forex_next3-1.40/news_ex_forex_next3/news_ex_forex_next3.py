import json
from datetime import datetime
import pandas as pd


class NEWS:
         
         def __init__(self):
             fileObject = open("login.json", "r")
             jsonContent = fileObject.read()
             aList = json.loads(jsonContent)

             fileObject = open("news.json", "r")
             jsonContent = fileObject.read()
             self.List_news = json.loads(jsonContent)
             
             self.login = int (aList['login'])
             self.Server = aList['Server'] 
             self.Password = aList['Password'] 
             self.symbol_EURUSD = aList['symbol_EURUSD'] 
             self.decimal_sambol = int (aList['decimal_sambol'] )
             self.symbol_news = aList['symbol_news'] 
             
       
         def cal_mount_day(index_mount , index_day):
                 list_mount = ["Jan" , "Feb" , "Mar" , "Apr" , "May" , "Jun" , "Jul" , "Aug" , "Sep" , "Oct" , "Nov" , "Dec"]
                 
                 if index_mount == 1:
                        mount = list_mount[0]
                     #    print("mount:" , mount)
                        return f'{mount}'+ ' ' +f'{index_day}'
                 
                 elif index_mount == 2:
                        mount = list_mount[1]
                     #    print("mount:" , mount)
                        return f'{mount}'+ ' ' +f'{index_day}'
                 
                 elif index_mount == 3:
                        mount = list_mount[2]
                     #    print("mount:" , mount)
                        return f'{mount}'+ ' ' +f'{index_day}'
         
                 elif index_mount == 4:
                        mount = list_mount[3]
                     #    print("mount:" , mount)
                        return f'{mount}'+ ' ' +f'{index_day}'
         
                 elif index_mount == 5:
                        mount = list_mount[4]
                     #    print("mount:" , mount)
                        return f'{mount}'+ ' ' +f'{index_day}'  
         
                 elif index_mount == 6:
                        mount = list_mount[5]
                     #    print("mount:" , mount)
                        return f'{mount}'+ ' ' +f'{index_day}'
                  
                 elif index_mount == 7:
                        mount = list_mount[6]
                     #    print("mount:" , mount)
                        return f'{mount}'+ ' ' +f'{index_day}'
                 
                 elif index_mount == 8:
                        mount = list_mount[7]
                     #    print("mount:" , mount)
                        return f'{mount}'+ ' ' +f'{index_day}'
                 
                 elif index_mount == 9:
                        mount = list_mount[8]
                     #    print("mount:" , mount)
                        return f'{mount}'+ ' ' +f'{index_day}'
                 
                 elif index_mount == 10:
                        mount = list_mount[9]
                     #    print("mount:" , mount)
                        return f'{mount}'+ ' ' +f'{index_day}'
                 
                 elif index_mount == 11:
                        mount = list_mount[10]
                     #    print("mount:" , mount)
                        return f'{mount}'+ ' ' +f'{index_day}'
                 
                 elif index_mount == 12:
                        mount = list_mount[11]
                     #    print("mount:" , mount)
                        return f'{mount}'+ ' ' +f'{index_day}'
         
         def time():
                 today = datetime.now()
                 date_time = today.strftime("%H:%M:%S")
               #   print("date_time:" , date_time)
                 month = '{:02d}'.format(today.month)
                 day = '{:02d}'.format(today.day)
                 return [ month , day]
         
         def time_now(input_minute):
            today = datetime.now()
            date_time = today.strftime("%H:%M:%S")
            # print("date_time:" , date_time)

            start_datetime = pd.to_datetime(date_time)
       #      print(start_datetime)
            
       #      p_time = start_datetime + pd.to_timedelta(input_minute, unit = 'm')
       #      print("p_time:" , p_time)

       #      n_time = start_datetime - pd.to_timedelta(input_minute  , unit = 'm')
       #      print("n_time:" , n_time)
       
           
            return start_datetime

         def cal_time(input_minute):
                 
                x_time = NEWS.time()
              #   print("xtime:" , x_time)
                index_mount = int(x_time[0])
                index_day = int(x_time[1])
                
                rec_time = NEWS.cal_mount_day(index_mount , index_day)
                
              #   print(rec_time)
                
                list_time = []
                list_currency = []
                list_total = []

                for index in NEWS().List_news:
              #       print (index['date'])
                    
                    if rec_time == index["date"] and index["impact"] == 'red':
                           list_time.append(index['time'])
                           list_currency.append(index['currency'])
                           
                list_total.append(list_time)
                list_total.append(list_currency)  
                # print("list_time:" , list_time)
                # print("list_currency:" , list_currency )
                # print("list_total:" , list_total )

                list_timenews = []
                for index , xx in enumerate(list_total[1]):
                     # print(xx)
                
                     if f'{xx}' in NEWS().symbol_news:
                     #     print ("xx:" , xx)
                        #  print("index:" , index)
                         time_news = list_total[0][index]
                        #  time_news = float (time_news)
                        #  minute = '{:02d}'.format(time_news.minute)
                        #  hour = '{:02d}'.format(time_news.hour)
                     #     print("time_news:" , time_news)
                         list_timenews.append(time_news)
                     #     print("")
                
               #  print ("list_timenews:" , list_timenews)

                today_time_now = NEWS.time_now(input_minute)
              #   print("today_time_now:" , today_time_now)
             
                minute = '{:02d}'.format(today_time_now.minute)
                hour = '{:02d}'.format(today_time_now.hour)
                time_now = f'{hour}' + '.' + f'{minute}'
                time_now = float (time_now)
               #  print("time_now:" , time_now)

                out_time = False


                for index , indext_time in enumerate(list_timenews):
                    
                  #   print("index:" , index)
                    
                    time_news = pd.to_datetime(indext_time)

                    p_time = time_news - pd.to_timedelta(input_minute, unit = 'm')
              #       print("p_time:" , p_time)
                    minute_p = '{:02d}'.format(p_time.minute)
                    hour_p = '{:02d}'.format(p_time.hour)
                    hour_news_p = f'{hour_p}' + '.' + f'{minute_p}'
                    hour_news_p = float (hour_news_p)
                  #   print("hour_news_p:" , hour_news_p)
                    

                    n_time = time_news + pd.to_timedelta(input_minute  , unit = 'm')
              #       print("n_time:" , n_time)
                    minute_n = '{:02d}'.format(n_time.minute)
                    hour_n = '{:02d}'.format(n_time.hour)
                    hour_news_n = f'{hour_n}' + '.' + f'{minute_n}'
                    hour_news_n = float (hour_news_n)
                  #   print("hour_news_n:" , hour_news_n)
              
              #       print('')

                    if time_now >= hour_news_p and time_now <= hour_news_n:
                        #   print('11111111111111111111111111')
                          out_time = True
                    
       
                if out_time == True:
                     today = datetime.now()
                     date_time = today.strftime("%H:%M:%S")
                     return [True , date_time]
                
                elif out_time == False:
                     return [False]
       
         
                
