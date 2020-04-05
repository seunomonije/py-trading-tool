import imports as pkg

# threeDayEMA(ticker, displayGraph)
#    prints the three day winning percentage for the given stock, my first and probably most simple algorithm
#        PARAMETERS:
#            ticker -> the ticker name
#            displayGraph -> if 1, displays graph

#        GRABS FROM INTERNET EVERY TIME -- EXPLORING BETTER OPTIONS

def threeDayEMA(ticker, displayGraph):

    #downloading stock data with yfinance
    data = pkg.yf.download(ticker, period = "1y")

    #taking out the closing price for each day
    closeArr = data['Close'].to_numpy()

    #uses talib to calculate the SMA and EMA
    smaArr = pkg.talib.SMA(closeArr, timeperiod = 10)
    emaArr = pkg.talib.EMA(closeArr, timeperiod = 20)
    
    ##initialize the counters
    winners = 0
    losers = 0

    #for each EMA value
    for i in range(len(emaArr)):
        
        #if the closing price surpasses the EMA over a 2 day period
        if closeArr[i-1] < emaArr[i-1]:
            if closeArr[i] > emaArr[i]:
                
                #first make sure you're not at the end of the data set
                if (i+3 >= len(closeArr)):
                    break
                
                #if the price at the crossing point is less than the price after 3 days
                if closeArr[i] < closeArr[i+3]:
                    #print("Uptrend predicted at x = %d, three day winner" % i)
                    
                    #this is a winner
                    winners+=1
                    
                    #fast forward 3 days since that's how long I would've held the stock
                    i+=3
                    
                    #continue to the next day
                    continue
                
                #if the price at the crossing line is more than the price after 3 days
                if closeArr[i] > closeArr[i+3]:
                    #print("Uptrend predicted at x = %d, three day loser" % i)
                    
                    #this is a loser
                    losers+=1
                    
                    #fast forward 3 days since that's how long I would've held the stock
                    i+=3
                    
                    #continue to the next day
                    continue
    
    #if there is a data
    if winners+losers != 0:
        
        #print the winning percentage
        print("%s winning percentage: %s" % (ticker, winners/(winners+losers)))
    
    #if displayGraph is toggled
    if displayGraph == 1:
        
        #tell the graph to keep the days in integer format
        xi = list(range(len(close)))
        pkg.plt.xticks(xi, xi)
        
        #plot the closing prices
        pkg.plt.plot(close, 'o-', label = "Close" )
        
        #plot the EMA
        pkg.plt.plot(emaArr, 'o-', label = "EMA")
        
        #plot the SMA
        pkg.plt.plot(smaArr, 'o-', label = "SMA")
        
        #display a legend
        pkg.plt.legend()
        
        #display the graph
        pkg.plt.show()


