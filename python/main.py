import sys
import imports as pkg
import functions as fn
import algos

tickerArr = []
winnerArr = []
tickersToDelete = []
#if cmd-line arguments/Users/seunomonije/Desktop/Trading/py-trading-tool/python/main.py
if (len(sys.argv) > 1):

    #copy the cmd-line arguments
    tickerArr = sys.argv
    
    #pop the filename
    tickerArr.pop(0)
   uuh7468790-=-065 
else:
    tickerArr = fn.stdinRead()
    

for i in range(len(tickerArr)):
    
    try:
        #download the data for each ticker
        data = pkg.yf.download(tickerArr[i], period = "1y", interval = "1d")
        
        #run all my algorithms
        threeDayEma = algos.threeDayEMAHelper(tickerArr[i], 0, data)
        if (threeDayEma != 1):
            winnerArr.append((threeDayEma, '3EMA'))
            
        swingRSI = algos.swingRSIHelper(tickerArr[i], 0, data)
        if (swingRSI != 1):
            winnerArr.append((swingRSI, 'SWNG'))
    except:
        tickersToDelete.append(tickerArr[i])
        continue
    
print("Get these stocks out of here")
print(tickersToDelete)

print("These are the winning stocks:")
print(winnerArr)
print("\n")
