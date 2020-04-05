import imports as pkg

# threeDayPercentage(ticker, displayGraph)
#    prints the three day winning percentage for the given stock
#        PARAMETERS:
#            ticker -> the ticker name
#            displayGraph -> if 1, displays graph

def threeDayPercentage(ticker, displayGraph):

    ##downloading stock data with yfinance
    data = pkg.yf.download(ticker, period = "1y")

    ##taking out the closing price for each day
    closeArr = data['Close'].to_numpy()

    ##calculations
    rsiArr = pkg.talib.RSI(closeArr)
    smaArr = pkg.talib.SMA(closeArr, timeperiod = 10)
    emaArr = pkg.talib.EMA(closeArr, timeperiod = 20)

    winners = 0
    losers = 0

    for i in range(len(emaArr)):
        if closeArr[i-1] < emaArr[i-1]:
            if closeArr[i] > emaArr[i]:
            
                if (i+3 >= len(closeArr)):
                    break
                    
                if closeArr[i] < closeArr[i+3]:
                    #print("Uptrend predicted at x = %d, three day winner" % i)
                    i+=3
                    winners+=1
                    continue
                    
#                if closeArr[i] < closeArr[i+1]:
#
#                    if closeArr[i] < closeArr[i+2]:
#                        print("Uptrend predicted at x = %d, two day winner" % i)
#                        winners+=1
#                        continue
#
#                    print("Uptrend predicted at x = %d, one day winner" % i)
#                    winners+=1
#                    continue
                
                if closeArr[i] > closeArr[i+3]:
                    #print("Uptrend predicted at x = %d, three day loser" % i)
                    i+=3
                    losers+=1
                    continue
#        if abs(emaArr[i] - closeArr[i]) < 3:
#            continue

    if winners+losers != 0:
        print("%s winning percentage: %s" % (ticker, winners/(winners+losers)))
    
    if displayGraph == 1:
    
        xi = list(range(len(close)))
        pkg.plt.plot(close, 'o-', label = "Close" )

        pkg.plt.plot(rsiArr, 'o-', label = "RSI")

        pkg.plt.plot(emaArr, 'o-', label = "EMA")

        pkg.plt.plot(smaArr, 'o-', label = "SMA")

        pkg.plt.xticks(xi, xi)
        pkg.plt.legend()
        pkg.plt.show()


