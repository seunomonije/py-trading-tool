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
    algos.threeDayEMA(tickerArr[i], 0)

print("Let's see if this works!")
