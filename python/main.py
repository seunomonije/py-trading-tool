import sys
import imports as pkg
import functions as fn
import algos

tickerArr = []
#if cmd-line arguments
if (len(sys.argv) > 1):

    #copy the cmd-line arguments
    tickerArr = sys.argv
    
    #pop the filename
    tickerArr.pop(0)
    
else:
    tickerArr = fn.stdinRead()
    

for i in range(len(tickerArr)):

    #download the data for each ticker
    data = pkg.yf.download(tickerArr[i], period = "1y", interval = "1d")
    
    #run all my algorithms
    algos.threeDayEMAHelper(tickerArr[i], 1, data)

print("\nDone with analysis.\n")
