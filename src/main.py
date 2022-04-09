import array as arr
from data import Data
from statistics import Statistics
import random
from machine import Pin
from button import Button
import urequests
import ujson
led_red = Pin(21,Pin.OUT)
led_green = Pin(19,Pin.OUT)
led_yellow = Pin(22,Pin.OUT)
led_red.value(False)
led_yellow.value(False)
led_green.value(False)
stocks= { 'Apple': 'AAPL', 'Microsoft':'MSFT','Progenity':'PROG','Tesla':'TSLA'}
print ('Left Button -- Switch the Stock')
print ('Right Button -- Select the Stock\n')
for h in list(stocks.keys()):
    if h==list(stocks.keys())[0]:
        print ('->',h)
    else:
        print ('  ',h)
i=0
def menu(state):
    global i
    if state== True:
        led_red.value(False)
        led_yellow.value(False)
        led_green.value(False)
        i=i-1
        print (15*'\n')
        print ('Left Button -- Switch the Stock')
        print ('Right Button -- Select the Stock \n')
        if i <-len(stocks):
            i=len(stocks)-1
        for h in list(stocks.keys()):
            if h==list(stocks.keys())[i]:
                print ('->',h)
            else:
                print ('  ',h)   
def veri(state):
    global i
    if state==True:
        led_red.value(False)
        led_yellow.value(False)
        led_green.value(False)
        stock=Stocks[i]
        url = "http://api.marketstack.com/v1/eod?access_key={0}&symbols={1}&limit={2}" \
            .format('46f6b6128834b932b1409596c72350eb',stocks[list(stocks.keys())[i]],'1')
        rawdata= urequests.get(url).json()
        newdata=rawdata['data']
        for finaldata in newdata:
            last_stock_value=finaldata['adj_close']
            if stock[-1]!=last_stock_value:
                stock.append(last_stock_value)
            else:
                pass
        avg=arr.array('f')
        for j in range(20):
            tlc=arr.array('f')
        for k in range(15):
            tlc.append(random.choice(Data.cwgr(stock)))
        avg.append(Statistics.mean(tlc))
        r_values=arr.array('f')
        Msim=2000
        for m in range(Msim):
            ult_price=stock[-1]
            r=random.uniform(min(avg),max(avg))
            r_values.append(ult_price + (ult_price*r))
        print ('\n')
        print ('Valor atual: {0}'.format(ult_price))
        print ('Próximo valor semanal esperado: {0}'.format(Statistics.mean(r_values)))
        media=Statistics.mean(r_values)
        if (media/ult_price -1)*100 >0.8:
                led_green.value(True)
        elif (media/ult_price -1)*100 <-0.5:
            led_red.value(True)
        else:
            led_yellow.value(True)
        print ('\n')
        print ('Left Button -- Pick a New Stock')
        print ('Right Butoon -- Resimulate The Current Stock')
        
        

button_left=Button(23,menu)
button_right=Button(18,veri)
while True:
    button_right.proc()
    button_left.proc()









