import sys
import imports as pkg
import yfinance as yf

import functions as fn
import algos



def main():
    tickerArr = []
    winnerArr = []
    tickersToDelete = []

    #if cmd-line arguments/Users/seunomonije/Desktop/Trading/py-trading-tool/python/main.py
    if (len(sys.argv) > 1):

        #copy the cmd-line arguments
        tickerArr = sys.argv
        
        #pop the filename
        tickerArr.pop(0)
    else:
        tickerArr = fn.stdinRead()
        

    for i in range(len(tickerArr)):
        
        data = None
        current_ticker = tickerArr[i]

        # First, let's get the data
        try: 
            #download the data for each ticker
            data = yf.download(current_ticker, period = "1y", interval = "1d")
        except:
            print('There was an error downloading ticker: ', current_ticker)
            tickersToDelete.append(current_ticker)
            continue

        try:
            #run all my algorithms
            threeDayEma = algos.threeDayEMAHelper(current_ticker, 0, data)
            if (threeDayEma != 1):
                winnerArr.append((threeDayEma, '3EMA'))
                
            swingRSI = algos.swingRSIHelper(current_ticker, 0, data)
            if (swingRSI != 1):
                winnerArr.append((swingRSI, 'SWNG'))
        except:
            print('There was an error running algorithms with ticker: ' + current_ticker)
            tickersToDelete.append(current_ticker)
            continue
        
    print("Get these stocks out of here")
    print(tickersToDelete)

    print("These are the winning stocks:")
    print(winnerArr)
    print("\n")

if __name__ == '__main__':
    main()
