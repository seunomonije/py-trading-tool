import imports as pkg
import functions as fn

#    threeDayEMAHelper(ticker)
#        helper function to consolidate buyAlertEMA and threeDayEMAbacktester
#        mainly created for download optimization

def threeDayEMAHelper(ticker, displayGraph, data):
    
    if (buyAlertEMA(ticker, data) == True):
        threeDayEMAbacktester(ticker, displayGraph, data)
    else:
        print("%s is not a stock of interest for today" % (ticker))


#    buyAlertEMA(ticker)
#        signals if the given ticker is on buy alert for this day

def buyAlertEMA(ticker, data):
    
    #download the data
    #data = pkg.yf.download(ticker, period = "1y", interval = "1d")
    
    #take out the closing price for each day
    closeArr = data['Close'].to_numpy()
    
    #talib calculations
    emaArr = pkg.talib.EMA(closeArr, timeperiod = 20)
    
    if (emaArr[-1] - closeArr[-1] > -1) and (emaArr[-1] - closeArr[-1] < 0):
        print("\nALERT! %s is a potential purchase according to threeDayEMA. Here is some more info about the stock\n" % (ticker))
        return True
    

#   threeDayEMAbacktester(ticker, displayGraph)
#       prints the three day winning percentage for the given stock, my first and probably most simple algorithm
#           PARAMETERS:
#               ticker -> the ticker name
#               displayGraph -> if 1, displays graph

def threeDayEMAbacktester(ticker, displayGraph, data):
    
    #downloading stock data with yfinance
    #data = pkg.yf.download(ticker, period = "1y")

    #taking out the closing price for each day
    closeArr = data['Close'].to_numpy()

    #uses talib to calculate the SMA and EMA
    smaArr = pkg.talib.SMA(closeArr, timeperiod = 10)
    emaArr = pkg.talib.EMA(closeArr, timeperiod = 20)
    
    ##initialize the counters
    winners = 0
    losers = 0
    streak = 0
    highestStreak = 0
    
    #for each EMA value
    it = iter(range(len(emaArr)))
    for i in it:
        
        #if the closing price surpasses the EMA over a 2 day period
        if closeArr[i-1] < emaArr[i-1]:
            if closeArr[i] > emaArr[i]:
                    
                    
                #first make sure you're not at the end of the data set
                if (i+3 >= len(closeArr)):
                    break
                    
                if (i+1 >= len(closeArr)):
                    break
                
                #if I make money one day after the crossing point
                if (closeArr[i] < closeArr[i+1]):
                    
                    print("Uptrend predicted at x = %d, one day winner" % i)
                    
                    #i'm selling the stock
                    winners+=1
                    
                    #add to the streak
                    streak +=1
                    
                    #fastforward to the next day, python is so extra in C this would be just i+=1
                    for j in range(0, 1):
                         i = next(it)
                    
                    #continue
                    continue
                
                #if I don't make money the first day I'm entering the 3 day mode
                else:
        
                    #if the price at the crossing point is less than the price after 3 days
                    if closeArr[i] < closeArr[i+3]:
                        print("Uptrend predicted at x = %d, three day winner" % i)
                        
                        #this is a winner
                        winners+=1
                        
                        #add to the streak
                        streak+=1
                        
                        #fast forward 3 days since that's how long I would've held the stock
                        for j in range(0, 3):
                            i = next(it)
                        
                        #continue to the next day
                        continue
                    
                    #if the price at the crossing line is more than the price after 3 days
                    if closeArr[i] > closeArr[i+3]:
                        print("Uptrend predicted at x = %d, three day loser" % i)
                        
                        #this is a loser get out of my sight
                        losers+=1
                        
                        #set highest streak
                        highestStreak = streak
                        
                        #reset the streak
                        streak = 0
                        
                        #fast forward 3 days since that's how long I would've held the stock
                        for j in range(0, 3):
                            i = next(it)
                        
                        #continue to the next day
                        continue
    
    #if there is a data
    if winners+losers != 0:
    
        #calculate the rate
        rate = fn.truncate(winners/(winners+losers), 4)
        
        #print the winning percentage
        print("\nthreeDayEMA wins for %s with a rate of %s in the past year.\n" % (ticker, rate))
        
#        #print the current winning streak and highest win streak
#        if (highestStreak == 0):
#            if (streak > 0):
#                print("threeDayEMA is currently on a %s win streak for %s\n" % (streak, ticker))
#            else:
#                print("threeDayEMA has either never won or never lost for %s.\n" % (ticker))
#        else:
#            print("threeDayEMA is currently on a %s win streak for %s\n" % (streak, ticker))
#            print("Year to date, threeDayEMA's highest win streak is %s" % (highestStreak))
            

    
    #if displayGraph is toggled
    if displayGraph == 1:
        
        #tell the graph to keep the days in integer format
        xi = list(range(len(closeArr)))
        pkg.plt.xticks(xi, xi)
        
        #plot the closing prices
        pkg.plt.plot(closeArr, 'o-', label = "Close" )
        
        #plot the EMA
        pkg.plt.plot(emaArr, 'o-', label = "EMA")
        
        #plot the SMA
        pkg.plt.plot(smaArr, 'o-', label = "SMA")
        
        #display a legend
        pkg.plt.legend()
        
        #display the graph
        pkg.plt.show()


